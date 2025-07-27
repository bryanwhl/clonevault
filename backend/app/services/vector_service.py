"""
Vector store service for embeddings and similarity search using Pinecone
"""

from typing import Dict, Any, List, Optional, Tuple
import uuid
import numpy as np

import structlog
import openai
import pinecone
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.models.embedding import Embedding
from app.core.exceptions import ExternalServiceError

logger = structlog.get_logger(__name__)


class VectorService:
    """Service for vector operations and similarity search"""
    
    def __init__(self):
        self.settings = get_settings()
        self.openai_client = None
        self.pinecone_index = None
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize OpenAI and Pinecone clients"""
        try:
            # Initialize OpenAI client
            self.openai_client = openai.OpenAI(api_key=self.settings.openai_api_key)
            
            # Initialize Pinecone
            pinecone.init(
                api_key=self.settings.pinecone_api_key,
                environment=self.settings.pinecone_environment
            )
            
            # Get or create index
            if self.settings.pinecone_index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=self.settings.pinecone_index_name,
                    dimension=1536,  # OpenAI ada-002 embedding dimension
                    metric="cosine"
                )
            
            self.pinecone_index = pinecone.Index(self.settings.pinecone_index_name)
            
            logger.info("Vector service clients initialized successfully")
            
        except Exception as e:
            logger.error("Failed to initialize vector service clients", error=str(e))
            raise ExternalServiceError("Vector Service", str(e))
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                model=self.settings.openai_embedding_model,
                input=text
            )
            
            embedding = response.data[0].embedding
            logger.debug("Generated embedding", text_length=len(text), embedding_dim=len(embedding))
            
            return embedding
            
        except Exception as e:
            logger.error("Failed to generate embedding", error=str(e))
            raise ExternalServiceError("OpenAI Embeddings", str(e))
    
    async def store_embedding(
        self, 
        db: AsyncSession,
        entity_type: str, 
        entity_id: str, 
        text: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Generate and store embedding for an entity"""
        try:
            # Generate embedding
            embedding_vector = await self.generate_embedding(text)
            
            # Store in database
            embedding = Embedding(
                entity_type=entity_type,
                entity_id=uuid.UUID(entity_id),
                embedding=embedding_vector,
                metadata=metadata or {}
            )
            
            db.add(embedding)
            await db.commit()
            await db.refresh(embedding)
            
            # Store in Pinecone
            vector_id = f"{entity_type}_{entity_id}"
            self.pinecone_index.upsert([
                {
                    "id": vector_id,
                    "values": embedding_vector,
                    "metadata": {
                        "entity_type": entity_type,
                        "entity_id": entity_id,
                        "db_embedding_id": str(embedding.id),
                        **(metadata or {})
                    }
                }
            ])
            
            logger.info("Embedding stored successfully", 
                       entity_type=entity_type, entity_id=entity_id, 
                       embedding_id=str(embedding.id))
            
            return str(embedding.id)
            
        except Exception as e:
            await db.rollback()
            logger.error("Failed to store embedding", 
                        entity_type=entity_type, entity_id=entity_id, error=str(e))
            raise
    
    async def update_embedding(
        self,
        db: AsyncSession,
        entity_type: str,
        entity_id: str,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Update existing embedding or create new one"""
        try:
            # Delete existing embedding if it exists
            await self.delete_embedding(db, entity_type, entity_id)
            
            # Create new embedding
            return await self.store_embedding(db, entity_type, entity_id, text, metadata)
            
        except Exception as e:
            logger.error("Failed to update embedding", 
                        entity_type=entity_type, entity_id=entity_id, error=str(e))
            raise
    
    async def delete_embedding(self, db: AsyncSession, entity_type: str, entity_id: str) -> bool:
        """Delete embedding for an entity"""
        try:
            # Delete from Pinecone
            vector_id = f"{entity_type}_{entity_id}"
            self.pinecone_index.delete(ids=[vector_id])
            
            # Delete from database
            from sqlalchemy import select, delete
            stmt = delete(Embedding).where(
                Embedding.entity_type == entity_type,
                Embedding.entity_id == uuid.UUID(entity_id)
            )
            await db.execute(stmt)
            await db.commit()
            
            logger.info("Embedding deleted successfully", 
                       entity_type=entity_type, entity_id=entity_id)
            
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error("Failed to delete embedding", 
                        entity_type=entity_type, entity_id=entity_id, error=str(e))
            return False
    
    async def similarity_search(
        self,
        query_text: str,
        entity_type: str = None,
        top_k: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Search for similar entities using vector similarity"""
        try:
            # Generate query embedding
            query_embedding = await self.generate_embedding(query_text)
            
            # Build filter
            filter_dict = {}
            if entity_type:
                filter_dict["entity_type"] = entity_type
            
            # Query Pinecone
            results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict if filter_dict else None
            )
            
            # Filter by similarity threshold and format results
            similar_items = []
            for match in results.matches:
                if match.score >= similarity_threshold:
                    similar_items.append({
                        "entity_type": match.metadata.get("entity_type"),
                        "entity_id": match.metadata.get("entity_id"),
                        "similarity_score": float(match.score),
                        "metadata": match.metadata
                    })
            
            logger.info("Similarity search completed", 
                       query_length=len(query_text), 
                       results_count=len(similar_items),
                       entity_type=entity_type)
            
            return similar_items
            
        except Exception as e:
            logger.error("Similarity search failed", error=str(e))
            raise ExternalServiceError("Pinecone Search", str(e))
    
    async def find_similar_agents(
        self,
        agent_id: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find agents similar to the given agent"""
        try:
            # Get agent's embedding vector
            vector_id = f"agent_{agent_id}"
            
            # Query for similar agents
            results = self.pinecone_index.query(
                id=vector_id,
                top_k=top_k + 1,  # +1 because the agent itself will be included
                include_metadata=True,
                filter={"entity_type": "agent"}
            )
            
            # Filter out the agent itself and apply threshold
            similar_agents = []
            for match in results.matches:
                if (match.metadata.get("entity_id") != agent_id and 
                    match.score >= similarity_threshold):
                    similar_agents.append({
                        "agent_id": match.metadata.get("entity_id"),
                        "similarity_score": float(match.score),
                        "metadata": match.metadata
                    })
            
            logger.info("Similar agents found", 
                       agent_id=agent_id, 
                       similar_count=len(similar_agents))
            
            return similar_agents
            
        except Exception as e:
            logger.error("Failed to find similar agents", 
                        agent_id=agent_id, error=str(e))
            raise ExternalServiceError("Agent Similarity Search", str(e))
    
    async def find_similar_users_by_interests(
        self,
        interests: List[str],
        top_k: int = 10,
        similarity_threshold: float = 0.6
    ) -> List[Dict[str, Any]]:
        """Find users with similar interests"""
        try:
            # Create query text from interests
            query_text = " ".join(interests)
            
            # Search for similar user profiles
            results = await self.similarity_search(
                query_text=query_text,
                entity_type="user_profile",
                top_k=top_k,
                similarity_threshold=similarity_threshold
            )
            
            logger.info("Similar users by interests found", 
                       interests=interests, 
                       results_count=len(results))
            
            return results
            
        except Exception as e:
            logger.error("Failed to find similar users by interests", 
                        interests=interests, error=str(e))
            raise
    
    async def calculate_compatibility_score(
        self,
        agent1_id: str,
        agent2_id: str
    ) -> float:
        """Calculate compatibility score between two agents"""
        try:
            # Get both agent vectors
            vector1_id = f"agent_{agent1_id}"
            vector2_id = f"agent_{agent2_id}"
            
            # Fetch vectors from Pinecone
            fetch_response = self.pinecone_index.fetch(ids=[vector1_id, vector2_id])
            
            if vector1_id not in fetch_response.vectors or vector2_id not in fetch_response.vectors:
                logger.warning("One or both agent vectors not found", 
                             agent1_id=agent1_id, agent2_id=agent2_id)
                return 0.0
            
            # Calculate cosine similarity
            vector1 = np.array(fetch_response.vectors[vector1_id].values)
            vector2 = np.array(fetch_response.vectors[vector2_id].values)
            
            # Cosine similarity calculation
            dot_product = np.dot(vector1, vector2)
            norm1 = np.linalg.norm(vector1)
            norm2 = np.linalg.norm(vector2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            similarity = dot_product / (norm1 * norm2)
            
            # Convert from [-1, 1] to [0, 1] range
            compatibility_score = (similarity + 1) / 2
            
            logger.info("Compatibility score calculated", 
                       agent1_id=agent1_id, agent2_id=agent2_id, 
                       score=compatibility_score)
            
            return float(compatibility_score)
            
        except Exception as e:
            logger.error("Failed to calculate compatibility score", 
                        agent1_id=agent1_id, agent2_id=agent2_id, error=str(e))
            return 0.0
    
    async def get_index_stats(self) -> Dict[str, Any]:
        """Get Pinecone index statistics"""
        try:
            stats = self.pinecone_index.describe_index_stats()
            
            return {
                "total_vectors": stats.total_vector_count,
                "dimension": stats.dimension,
                "index_fullness": stats.index_fullness,
                "namespaces": stats.namespaces
            }
            
        except Exception as e:
            logger.error("Failed to get index stats", error=str(e))
            raise ExternalServiceError("Pinecone Stats", str(e))