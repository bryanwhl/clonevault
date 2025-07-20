import React, { useState } from 'react';
import { TrendingUp, MessageSquare, ThumbsUp, Eye, ExternalLink, Bot, Filter, Search } from 'lucide-react';
import { Card, CardContent, CardHeader } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';

interface FeedProps {
  user: {
    name: string;
    agentActive: boolean;
  };
}

export function Feed({ user }: FeedProps) {
  const [selectedCategory, setSelectedCategory] = useState('all');
  
  const posts = [
    {
      id: 1,
      title: "The Future of AI in Healthcare: Revolutionizing Patient Care",
      url: "https://example.com/ai-healthcare",
      points: 342,
      author: "Dr. Sarah Chen",
      authorAvatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face",
      time: "3 hours ago",
      comments: 89,
      category: "AI",
      isRecommended: true,
      recommendationReason: "Based on your interest in healthcare technology and AI research",
      description: "Exploring how artificial intelligence is transforming diagnosis, treatment, and patient outcomes across medical institutions worldwide."
    },
    {
      id: 2,
      title: "Building Scalable Microservices with Kubernetes and Docker",
      url: "https://example.com/kubernetes-guide",
      points: 245,
      author: "Mike Torres",
      authorAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
      time: "5 hours ago",
      comments: 56,
      category: "Engineering",
      isRecommended: false,
      description: "A comprehensive guide to designing and implementing microservices architecture using modern containerization technologies."
    },
    {
      id: 3,
      title: "Remote Work Culture: Building Strong Teams Across Time Zones",
      url: "https://example.com/remote-work",
      points: 198,
      author: "Elena Rodriguez",
      authorAvatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop&crop=face",
      time: "8 hours ago",
      comments: 73,
      category: "Management",
      isRecommended: true,
      recommendationReason: "Your agent noticed you're interested in team management and remote collaboration",
      description: "Best practices for maintaining team cohesion, productivity, and company culture in distributed work environments."
    },
    {
      id: 4,
      title: "Blockchain Beyond Cryptocurrency: Real-World Applications",
      url: "https://example.com/blockchain-apps",
      points: 156,
      author: "James Kim",
      authorAvatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
      time: "12 hours ago",
      comments: 42,
      category: "Blockchain",
      isRecommended: false,
      description: "Examining practical implementations of blockchain technology in supply chain, healthcare, and digital identity verification."
    },
    {
      id: 5,
      title: "The Psychology of User Experience Design",
      url: "https://example.com/ux-psychology",
      points: 289,
      author: "Anna Park",
      authorAvatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face",
      time: "1 day ago",
      comments: 67,
      category: "Design",
      isRecommended: true,
      recommendationReason: "Matches your profile interests in user research and design thinking",
      description: "Understanding cognitive biases, user behavior patterns, and psychological principles that drive effective interface design."
    }
  ];

  const categories = ['all', 'AI', 'Engineering', 'Management', 'Blockchain', 'Design'];
  
  const filteredPosts = selectedCategory === 'all' 
    ? posts 
    : posts.filter(post => post.category === selectedCategory);

  const recommendedPosts = posts.filter(post => post.isRecommended);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Professional Feed</h1>
          <p className="text-muted-foreground">Discover trending posts and AI-curated recommendations</p>
        </div>
        <Button variant="outline">
          <Filter className="w-4 h-4 mr-2" />
          Filters
        </Button>
      </div>

      {/* AI Recommendations Banner */}
      {user.agentActive && recommendedPosts.length > 0 && (
        <Card className="border-blue-200 bg-blue-50/50 dark:bg-blue-950/20 dark:border-blue-800">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <Bot className="w-8 h-8 text-blue-600" />
              <div>
                <h3 className="text-blue-900 dark:text-blue-100">AI Recommendations Active</h3>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  Your Digital Twin agent has found {recommendedPosts.length} posts tailored to your interests and career goals.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Navigation Tabs */}
      <Tabs value={selectedCategory} onValueChange={setSelectedCategory}>
        <TabsList className="grid w-full grid-cols-6">
          {categories.map((category) => (
            <TabsTrigger key={category} value={category} className="capitalize">
              {category}
            </TabsTrigger>
          ))}
        </TabsList>

        <TabsContent value={selectedCategory} className="space-y-4 mt-6">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              placeholder="Search posts..."
              className="pl-10"
            />
          </div>

          {/* Posts */}
          <div className="space-y-4">
            {filteredPosts.map((post) => (
              <Card key={post.id} className={post.isRecommended ? "border-l-4 border-l-blue-500" : ""}>
                <CardContent className="p-6">
                  {/* Recommendation Badge */}
                  {post.isRecommended && (
                    <div className="flex items-center space-x-2 mb-3">
                      <Badge variant="secondary" className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                        <Bot className="w-3 h-3 mr-1" />
                        AI Recommended
                      </Badge>
                    </div>
                  )}

                  {/* Post Header */}
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg hover:text-blue-600 cursor-pointer">{post.title}</h3>
                      <p className="text-sm text-muted-foreground mt-1">{post.description}</p>
                    </div>
                    <ExternalLink className="w-4 h-4 text-muted-foreground ml-4 cursor-pointer hover:text-foreground" />
                  </div>

                  {/* Recommendation Reason */}
                  {post.isRecommended && post.recommendationReason && (
                    <div className="bg-blue-50 dark:bg-blue-950/30 p-3 rounded-lg mb-4">
                      <p className="text-sm text-blue-800 dark:text-blue-200">
                        💡 {post.recommendationReason}
                      </p>
                    </div>
                  )}

                  {/* Post Meta */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-2">
                        <Avatar className="w-6 h-6">
                          <AvatarImage src={post.authorAvatar} />
                          <AvatarFallback>{post.author[0]}</AvatarFallback>
                        </Avatar>
                        <span>{post.author}</span>
                      </div>
                      <span>•</span>
                      <span>{post.time}</span>
                      <Badge variant="outline" className="text-xs">
                        {post.category}
                      </Badge>
                    </div>

                    <div className="flex items-center space-x-4">
                      <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                        <TrendingUp className="w-4 h-4 mr-1" />
                        {post.points}
                      </Button>
                      <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                        <MessageSquare className="w-4 h-4 mr-1" />
                        {post.comments}
                      </Button>
                      <Button variant="ghost" size="sm" className="text-muted-foreground hover:text-foreground">
                        <ThumbsUp className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Load More */}
          <div className="text-center pt-6">
            <Button variant="outline">Load More Posts</Button>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}