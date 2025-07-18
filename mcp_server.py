#!/usr/bin/env python3
"""
MCP Server for Resume Parsing
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List
import PyPDF2
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    CallToolResult,
    ListResourcesResult,
    ListToolsResult,
    ReadResourceResult,
)


class ResumeParserServer:
    def __init__(self):
        self.server = Server("resume-parser")
        self.resume_data = {}
        self._setup_handlers()

    def _setup_handlers(self):
        @self.server.list_resources()
        async def list_resources() -> ListResourcesResult:
            return ListResourcesResult(
                resources=[
                    Resource(
                        uri="resume://parsed-data",
                        name="Parsed Resume Data",
                        description="Structured data extracted from the resume",
                        mimeType="application/json",
                    )
                ]
            )

        @self.server.read_resource()
        async def read_resource(uri: str) -> ReadResourceResult:
            if uri == "resume://parsed-data":
                return ReadResourceResult(
                    contents=[
                        TextContent(
                            type="text",
                            text=json.dumps(self.resume_data, indent=2)
                        )
                    ]
                )
            else:
                raise ValueError(f"Unknown resource: {uri}")

        @self.server.list_tools()
        async def list_tools() -> ListToolsResult:
            return ListToolsResult(
                tools=[
                    Tool(
                        name="parse_resume",
                        description="Parse a PDF resume and extract structured information",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Path to the PDF resume file"
                                }
                            },
                            "required": ["file_path"]
                        }
                    ),
                    Tool(
                        name="get_resume_section",
                        description="Get a specific section from the parsed resume",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "section": {
                                    "type": "string",
                                    "description": "Section name (e.g., 'experience', 'education', 'skills')"
                                }
                            },
                            "required": ["section"]
                        }
                    )
                ]
            )

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
            if name == "parse_resume":
                return await self._parse_resume(arguments["file_path"])
            elif name == "get_resume_section":
                return await self._get_resume_section(arguments["section"])
            else:
                raise ValueError(f"Unknown tool: {name}")

    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

    def _parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Parse resume text into structured data"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        resume_data = {
            "personal_info": {},
            "experience": [],
            "education": [],
            "skills": [],
            "projects": [],
            "raw_text": text
        }

        current_section = None
        current_item = {}
        
        for line in lines:
            line_lower = line.lower()
            
            # Extract personal information from the first few lines
            if not resume_data["personal_info"].get("name") and len(line.split()) <= 4:
                if any(char.isupper() for char in line) and not line_lower.startswith(('email', 'phone', 'linkedin')):
                    resume_data["personal_info"]["name"] = line
                    continue
            
            # Detect email
            if '@' in line and not resume_data["personal_info"].get("email"):
                import re
                email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', line)
                if email_match:
                    resume_data["personal_info"]["email"] = email_match.group()
            
            # Detect phone
            if any(char.isdigit() for char in line) and ('phone' in line_lower or '(' in line or '-' in line):
                import re
                phone_match = re.search(r'[\+]?[1-9]?[\d\s\-\(\)]{10,}', line)
                if phone_match:
                    resume_data["personal_info"]["phone"] = phone_match.group().strip()
            
            # Detect LinkedIn
            if 'linkedin' in line_lower:
                resume_data["personal_info"]["linkedin"] = line
            
            # Section detection
            if any(keyword in line_lower for keyword in ['experience', 'work', 'employment']):
                current_section = 'experience'
                continue
            elif any(keyword in line_lower for keyword in ['education', 'academic']):
                current_section = 'education'
                continue
            elif any(keyword in line_lower for keyword in ['skills', 'technical', 'technologies']):
                current_section = 'skills'
                continue
            elif any(keyword in line_lower for keyword in ['projects', 'portfolio']):
                current_section = 'projects'
                continue
            
            # Parse content based on current section
            if current_section == 'experience':
                if any(keyword in line_lower for keyword in ['intern', 'engineer', 'developer', 'analyst', 'manager', 'specialist']):
                    if current_item:
                        resume_data["experience"].append(current_item)
                    current_item = {"title": line, "details": []}
                elif current_item:
                    current_item["details"].append(line)
            
            elif current_section == 'education':
                if any(keyword in line_lower for keyword in ['university', 'college', 'school', 'bachelor', 'master', 'phd']):
                    if current_item:
                        resume_data["education"].append(current_item)
                    current_item = {"institution": line, "details": []}
                elif current_item:
                    current_item["details"].append(line)
            
            elif current_section == 'skills':
                if line and not line.lower().startswith('skills'):
                    resume_data["skills"].append(line)
            
            elif current_section == 'projects':
                if current_item and line:
                    current_item["details"].append(line)
                elif line:
                    current_item = {"name": line, "details": []}
        
        # Add the last item if exists
        if current_item and current_section in ['experience', 'education', 'projects']:
            resume_data[current_section].append(current_item)
        
        return resume_data

    async def _parse_resume(self, file_path: str) -> CallToolResult:
        """Parse resume and store structured data"""
        try:
            if not Path(file_path).exists():
                raise FileNotFoundError(f"Resume file not found: {file_path}")
            
            text = self._extract_text_from_pdf(file_path)
            self.resume_data = self._parse_resume_text(text)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Successfully parsed resume from {file_path}. Found {len(self.resume_data.get('experience', []))} experience entries, {len(self.resume_data.get('education', []))} education entries, and {len(self.resume_data.get('skills', []))} skills."
                    )
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error parsing resume: {str(e)}"
                    )
                ],
                isError=True
            )

    async def _get_resume_section(self, section: str) -> CallToolResult:
        """Get specific section from parsed resume data"""
        try:
            if not self.resume_data:
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text="No resume data available. Please parse a resume first."
                        )
                    ],
                    isError=True
                )
            
            section_data = self.resume_data.get(section, [])
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=json.dumps(section_data, indent=2)
                    )
                ]
            )
        except Exception as e:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error getting resume section: {str(e)}"
                    )
                ],
                isError=True
            )

    async def run(self, read_stream, write_stream):
        """Run the MCP server"""
        await self.server.run(read_stream, write_stream)


async def main():
    """Main entry point for the MCP server"""
    import sys
    server = ResumeParserServer()
    await server.run(sys.stdin.buffer, sys.stdout.buffer)


if __name__ == "__main__":
    asyncio.run(main())