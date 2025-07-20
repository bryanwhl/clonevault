import React, { useState } from 'react';
import { Users, MessageSquare, UserPlus, UserMinus, Search, Filter, MoreHorizontal, Mail, Phone, Globe } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from './ui/dropdown-menu';

interface ConnectionsProps {
  user: {
    name: string;
    connections: number;
  };
}

export function Connections({ user }: ConnectionsProps) {
  const [searchQuery, setSearchQuery] = useState('');
  
  const connections = [
    {
      id: 1,
      name: "Dr. Sarah Chen",
      title: "AI Research Scientist",
      company: "Stanford Medical AI Lab",
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face",
      location: "Palo Alto, CA",
      mutualConnections: 23,
      connectedDate: "2024-01-15",
      connectionSource: "agent_match",
      matchScore: 89,
      lastInteraction: "3 days ago",
      skills: ["Machine Learning", "Healthcare AI", "Research"],
      status: "connected"
    },
    {
      id: 2,
      name: "Mike Torres",
      title: "Product Manager",
      company: "InnovateX",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face",
      location: "San Francisco, CA",
      mutualConnections: 15,
      connectedDate: "2024-01-10",
      connectionSource: "agent_match",
      matchScore: 76,
      lastInteraction: "1 week ago",
      skills: ["Product Development", "Team Leadership", "Fintech"],
      status: "connected"
    },
    {
      id: 3,
      name: "Elena Rodriguez",
      title: "Engineering Manager",
      company: "CloudTech Solutions",
      avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=400&h=400&fit=crop&crop=face",
      location: "Austin, TX",
      mutualConnections: 8,
      connectedDate: "2024-01-08",
      connectionSource: "direct_request",
      matchScore: null,
      lastInteraction: "2 weeks ago",
      skills: ["Engineering Management", "Remote Teams", "Mentorship"],
      status: "connected"
    }
  ];

  const pendingRequests = [
    {
      id: 4,
      name: "James Kim",
      title: "Blockchain Developer",
      company: "CryptoSolutions Inc",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face",
      location: "Seattle, WA",
      mutualConnections: 5,
      requestDate: "2024-01-18",
      connectionSource: "agent_match",
      matchScore: 82,
      message: "Hi Alex, my Digital Twin agent had a great conversation with yours about blockchain applications in healthcare. I'd love to connect and explore potential collaboration opportunities.",
      skills: ["Blockchain", "Smart Contracts", "DeFi"],
      status: "pending_received"
    },
    {
      id: 5,
      name: "Anna Park",
      title: "UX Design Lead",
      company: "Design Studio Pro",
      avatar: "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=400&fit=crop&crop=face",
      location: "Los Angeles, CA",
      mutualConnections: 12,
      requestDate: "2024-01-17",
      connectionSource: "manual_request",
      matchScore: null,
      message: "I came across your profile and was impressed by your work in healthcare AI. I'm working on UX for medical applications and would love to connect.",
      skills: ["UX Design", "Healthcare UI", "User Research"],
      status: "pending_sent"
    }
  ];

  const suggestions = [
    {
      id: 6,
      name: "David Liu",
      title: "Data Scientist",
      company: "MedTech Analytics",
      avatar: "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=400&h=400&fit=crop&crop=face",
      location: "Boston, MA",
      mutualConnections: 18,
      connectionReason: "Works in healthcare data science with mutual connections",
      matchScore: 85,
      skills: ["Data Science", "Healthcare Analytics", "Python"],
      status: "suggested"
    },
    {
      id: 7,
      name: "Lisa Zhang",
      title: "VP of Engineering",
      company: "HealthTech Innovations",
      avatar: "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=400&h=400&fit=crop&crop=face",
      location: "New York, NY",
      mutualConnections: 31,
      connectionReason: "Senior leader in healthcare technology with similar background",
      matchScore: 78,
      skills: ["Engineering Leadership", "Healthcare Tech", "Team Scaling"],
      status: "suggested"
    }
  ];

  const handleAcceptRequest = (id: number) => {
    console.log("Accepting connection request:", id);
  };

  const handleDeclineRequest = (id: number) => {
    console.log("Declining connection request:", id);
  };

  const handleSendRequest = (id: number) => {
    console.log("Sending connection request:", id);
  };

  const filteredConnections = connections.filter(conn =>
    conn.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    conn.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
    conn.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1>My Network</h1>
          <p className="text-muted-foreground">Manage your professional connections and discover new opportunities</p>
        </div>
        <div className="flex items-center space-x-2">
          <Badge variant="secondary">{user.connections} connections</Badge>
          <Button variant="outline">
            <Filter className="w-4 h-4 mr-2" />
            Filter
          </Button>
        </div>
      </div>

      {/* Search */}
      <div className="relative max-w-md">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
        <Input
          placeholder="Search connections..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <Tabs defaultValue="connections" className="space-y-6">
        <TabsList>
          <TabsTrigger value="connections">
            Connections ({connections.length})
          </TabsTrigger>
          <TabsTrigger value="requests">
            Requests ({pendingRequests.length})
          </TabsTrigger>
          <TabsTrigger value="suggestions">
            Suggestions ({suggestions.length})
          </TabsTrigger>
        </TabsList>

        {/* Connections Tab */}
        <TabsContent value="connections" className="space-y-4">
          <div className="grid gap-4">
            {filteredConnections.map((connection) => (
              <Card key={connection.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <Avatar className="w-16 h-16">
                      <AvatarImage src={connection.avatar} alt={connection.name} />
                      <AvatarFallback>{connection.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="flex items-center space-x-2">
                            <span>{connection.name}</span>
                            {connection.connectionSource === 'agent_match' && (
                              <Badge variant="secondary" className="text-xs">
                                Agent Match {connection.matchScore}%
                              </Badge>
                            )}
                          </h3>
                          <p className="text-muted-foreground">{connection.title}</p>
                          <p className="text-sm text-muted-foreground">{connection.company} • {connection.location}</p>
                        </div>
                        
                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm">
                              <MoreHorizontal className="w-4 h-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>
                              <MessageSquare className="w-4 h-4 mr-2" />
                              Send Message
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Mail className="w-4 h-4 mr-2" />
                              Email Contact
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Globe className="w-4 h-4 mr-2" />
                              View Profile
                            </DropdownMenuItem>
                            <DropdownMenuItem className="text-destructive">
                              <UserMinus className="w-4 h-4 mr-2" />
                              Remove Connection
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        {connection.skills.map((skill, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <span>{connection.mutualConnections} mutual connections</span>
                        <span>Connected {new Date(connection.connectedDate).toLocaleDateString()}</span>
                        <span>Last interaction: {connection.lastInteraction}</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Requests Tab */}
        <TabsContent value="requests" className="space-y-4">
          <div className="grid gap-4">
            {pendingRequests.map((request) => (
              <Card key={request.id} className="border-blue-200 bg-blue-50/50">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <Avatar className="w-16 h-16">
                      <AvatarImage src={request.avatar} alt={request.name} />
                      <AvatarFallback>{request.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1 space-y-3">
                      <div>
                        <div className="flex items-center space-x-2 mb-1">
                          <h3>{request.name}</h3>
                          <Badge variant="outline" className={
                            request.status === 'pending_received' ? 'border-green-500 text-green-700' : 'border-orange-500 text-orange-700'
                          }>
                            {request.status === 'pending_received' ? 'Request Received' : 'Request Sent'}
                          </Badge>
                          {request.matchScore && (
                            <Badge variant="secondary" className="text-xs">
                              {request.matchScore}% match
                            </Badge>
                          )}
                        </div>
                        <p className="text-muted-foreground">{request.title} at {request.company}</p>
                        <p className="text-sm text-muted-foreground">{request.location} • {request.mutualConnections} mutual connections</p>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        {request.skills.map((skill, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                      
                      {request.message && (
                        <div className="bg-white p-3 rounded-lg border">
                          <p className="text-sm">{request.message}</p>
                        </div>
                      )}
                      
                      <div className="flex items-center justify-between">
                        <span className="text-sm text-muted-foreground">
                          {new Date(request.requestDate).toLocaleDateString()}
                        </span>
                        
                        <div className="flex space-x-2">
                          {request.status === 'pending_received' ? (
                            <>
                              <Button size="sm" onClick={() => handleAcceptRequest(request.id)}>
                                <UserPlus className="w-4 h-4 mr-2" />
                                Accept
                              </Button>
                              <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={() => handleDeclineRequest(request.id)}
                              >
                                Decline
                              </Button>
                            </>
                          ) : (
                            <Badge variant="secondary">Pending Response</Badge>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>

        {/* Suggestions Tab */}
        <TabsContent value="suggestions" className="space-y-4">
          <div className="grid gap-4">
            {suggestions.map((suggestion) => (
              <Card key={suggestion.id} className="hover:shadow-md transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <Avatar className="w-16 h-16">
                      <AvatarImage src={suggestion.avatar} alt={suggestion.name} />
                      <AvatarFallback>{suggestion.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                    </Avatar>
                    
                    <div className="flex-1 space-y-2">
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <h3>{suggestion.name}</h3>
                            <Badge variant="secondary" className="text-xs">
                              {suggestion.matchScore}% match
                            </Badge>
                          </div>
                          <p className="text-muted-foreground">{suggestion.title}</p>
                          <p className="text-sm text-muted-foreground">{suggestion.company} • {suggestion.location}</p>
                        </div>
                        
                        <Button size="sm" onClick={() => handleSendRequest(suggestion.id)}>
                          <UserPlus className="w-4 h-4 mr-2" />
                          Connect
                        </Button>
                      </div>
                      
                      <div className="flex flex-wrap gap-2">
                        {suggestion.skills.map((skill, index) => (
                          <Badge key={index} variant="outline" className="text-xs">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                      
                      <div className="bg-muted p-3 rounded-lg">
                        <p className="text-sm">💡 {suggestion.connectionReason}</p>
                      </div>
                      
                      <p className="text-sm text-muted-foreground">
                        {suggestion.mutualConnections} mutual connections
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}