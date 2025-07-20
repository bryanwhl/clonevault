import React, { useState } from 'react';
import { Bot, MessageSquare, Users, Clock, CheckCircle, XCircle, Filter, Search } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Button } from './ui/button';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Input } from './ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from './ui/dialog';

interface AgentNetworkProps {
  user: {
    name: string;
    agentActive: boolean;
  };
}

export function AgentNetwork({ user }: AgentNetworkProps) {
  const [selectedConversation, setSelectedConversation] = useState<number | null>(null);
  
  const agentConversations = [
    {
      id: 1,
      partnerName: "Dr. Sarah Chen",
      partnerTitle: "AI Research Scientist",
      partnerCompany: "Stanford Medical AI Lab",
      partnerAvatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face",
      status: "completed",
      matchScore: 89,
      interests: ["Machine Learning", "Healthcare AI", "Research Collaboration"],
      lastMessage: "Both agents found strong potential for collaboration on medical AI projects",
      timestamp: "2 hours ago",
      conversation: [
        {
          sender: "your_agent",
          message: "Hello! I represent Alex Johnson, a Senior Software Engineer with expertise in machine learning and healthcare technology. Alex is particularly interested in AI applications in medical diagnosis.",
          timestamp: "2:30 PM"
        },
        {
          sender: "partner_agent",
          message: "Greetings! I represent Dr. Sarah Chen, an AI Research Scientist specializing in medical AI at Stanford. Dr. Chen is actively seeking collaborators for healthcare AI research projects.",
          timestamp: "2:31 PM"
        },
        {
          sender: "your_agent",
          message: "Excellent match! Alex has experience with computer vision for medical imaging and natural language processing for clinical notes. He's looking for research opportunities in healthcare AI.",
          timestamp: "2:32 PM"
        },
        {
          sender: "partner_agent",
          message: "Perfect alignment! Dr. Chen is leading a project on AI-powered diagnostic imaging and could use someone with Alex's background. She's also interested in clinical NLP applications.",
          timestamp: "2:33 PM"
        }
      ]
    },
    {
      id: 2,
      partnerName: "Mike Torres",
      partnerTitle: "Product Manager",
      partnerCompany: "InnovateX",
      partnerAvatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
      status: "active",
      matchScore: 76,
      interests: ["Product Development", "Team Leadership", "Startup Experience"],
      lastMessage: "Discussing potential collaboration on fintech products",
      timestamp: "4 hours ago",
      conversation: [
        {
          sender: "partner_agent",
          message: "Hi there! I represent Mike Torres, a Product Manager at InnovateX. Mike is exploring opportunities to work with experienced engineers on fintech innovations.",
          timestamp: "10:15 AM"
        },
        {
          sender: "your_agent",
          message: "Hello! I represent Alex Johnson, a Senior Software Engineer with strong technical leadership experience. Alex has worked on financial technology projects and is open to product collaboration opportunities.",
          timestamp: "10:18 AM"
        }
      ]
    },
    {
      id: 3,
      partnerName: "Elena Rodriguez",
      partnerTitle: "Engineering Manager",
      partnerCompany: "CloudTech Solutions",
      partnerAvatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop&crop=face",
      status: "pending",
      matchScore: 82,
      interests: ["Engineering Management", "Remote Teams", "Mentorship"],
      lastMessage: "Initial introduction phase",
      timestamp: "1 day ago",
      conversation: [
        {
          sender: "your_agent",
          message: "Hello! I represent Alex Johnson, a Senior Software Engineer interested in transitioning into technical leadership roles. Alex values mentorship and team development.",
          timestamp: "Yesterday 3:45 PM"
        }
      ]
    }
  ];

  const pendingConnections = agentConversations.filter(conv => conv.status === 'pending');
  const activeConnections = agentConversations.filter(conv => conv.status === 'active');
  const completedConnections = agentConversations.filter(conv => conv.status === 'completed');

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'text-green-600';
      case 'active': return 'text-blue-600';
      case 'pending': return 'text-orange-600';
      default: return 'text-gray-600';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'active': return <Clock className="w-4 h-4" />;
      case 'pending': return <Clock className="w-4 h-4" />;
      default: return <XCircle className="w-4 h-4" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>Agent Network</h1>
          <p className="text-muted-foreground">Monitor your Digital Twin agent's networking activities and conversations</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant={user.agentActive ? "default" : "secondary"} className="flex items-center space-x-1">
            <Bot className="w-3 h-3" />
            <span>Agent {user.agentActive ? "Active" : "Inactive"}</span>
          </Badge>
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </Button>
        </div>
      </div>

      {/* Agent Status Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl">{agentConversations.length}</p>
              <p className="text-sm text-muted-foreground">Total Conversations</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl text-blue-600">{activeConnections.length}</p>
              <p className="text-sm text-muted-foreground">Active Discussions</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl text-green-600">{completedConnections.length}</p>
              <p className="text-sm text-muted-foreground">Successful Matches</p>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-center">
              <p className="text-2xl">78%</p>
              <p className="text-sm text-muted-foreground">Success Rate</p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Search and Filter */}
      <div className="flex items-center space-x-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
          <Input placeholder="Search conversations..." className="pl-10" />
        </div>
      </div>

      {/* Conversations Tabs */}
      <Tabs defaultValue="all" className="space-y-4">
        <TabsList>
          <TabsTrigger value="all">All ({agentConversations.length})</TabsTrigger>
          <TabsTrigger value="active">Active ({activeConnections.length})</TabsTrigger>
          <TabsTrigger value="completed">Completed ({completedConnections.length})</TabsTrigger>
          <TabsTrigger value="pending">Pending ({pendingConnections.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          {agentConversations.map((conversation) => (
            <Card key={conversation.id} className="hover:shadow-md transition-shadow">
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4 flex-1">
                    <Avatar className="w-12 h-12">
                      <AvatarImage src={conversation.partnerAvatar} />
                      <AvatarFallback>{conversation.partnerName.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-center space-x-3">
                        <h3>{conversation.partnerName}</h3>
                        <Badge variant="outline" className={getStatusColor(conversation.status)}>
                          {getStatusIcon(conversation.status)}
                          <span className="ml-1 capitalize">{conversation.status}</span>
                        </Badge>
                        <Badge variant="secondary">
                          {conversation.matchScore}% match
                        </Badge>
                      </div>
                      
                      <p className="text-sm text-muted-foreground">
                        {conversation.partnerTitle} at {conversation.partnerCompany}
                      </p>
                      
                      <div className="flex flex-wrap gap-2">
                        {conversation.interests.map((interest, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {interest}
                          </Badge>
                        ))}
                      </div>
                      
                      <p className="text-sm">{conversation.lastMessage}</p>
                      <p className="text-xs text-muted-foreground">{conversation.timestamp}</p>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Dialog>
                      <DialogTrigger asChild>
                        <Button variant="outline" size="sm">
                          <MessageSquare className="w-4 h-4 mr-2" />
                          View Chat
                        </Button>
                      </DialogTrigger>
                      <DialogContent className="max-w-2xl">
                        <DialogHeader>
                          <DialogTitle>Agent Conversation: {conversation.partnerName}</DialogTitle>
                        </DialogHeader>
                        <div className="space-y-4 max-h-96 overflow-y-auto">
                          {conversation.conversation.map((message, index) => (
                            <div key={index} className={`flex ${message.sender === 'your_agent' ? 'justify-end' : 'justify-start'}`}>
                              <div className={`max-w-sm p-3 rounded-lg ${
                                message.sender === 'your_agent' 
                                  ? 'bg-primary text-primary-foreground' 
                                  : 'bg-muted'
                              }`}>
                                <div className="flex items-center space-x-2 mb-2">
                                  <Bot className="w-4 h-4" />
                                  <span className="text-xs">
                                    {message.sender === 'your_agent' ? 'Your Agent' : `${conversation.partnerName}'s Agent`}
                                  </span>
                                </div>
                                <p className="text-sm">{message.message}</p>
                                <p className="text-xs opacity-70 mt-1">{message.timestamp}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                        {conversation.status === 'completed' && (
                          <div className="border-t pt-4">
                            <div className="flex items-center justify-between">
                              <p className="text-sm text-muted-foreground">
                                This conversation resulted in a {conversation.matchScore}% compatibility match.
                              </p>
                              <Button>Connect with {conversation.partnerName.split(' ')[0]}</Button>
                            </div>
                          </div>
                        )}
                      </DialogContent>
                    </Dialog>
                    
                    {conversation.status === 'completed' && (
                      <Button size="sm">
                        <Users className="w-4 h-4 mr-2" />
                        Connect
                      </Button>
                    )}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        {/* Other tab contents would follow the same pattern */}
        <TabsContent value="active">
          {/* Active conversations only */}
        </TabsContent>
        <TabsContent value="completed">
          {/* Completed conversations only */}
        </TabsContent>
        <TabsContent value="pending">
          {/* Pending conversations only */}
        </TabsContent>
      </Tabs>
    </div>
  );
}