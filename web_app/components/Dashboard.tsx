import React from 'react';
import { Bot, Users, TrendingUp, MessageSquare, Eye, ThumbsUp, Calendar, Briefcase, Settings } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Button } from './ui/button';
import { Progress } from './ui/progress';

interface DashboardProps {
  user: {
    name: string;
    title: string;
    company: string;
    connections: number;
    agentActive: boolean;
  };
}

export function Dashboard({ user }: DashboardProps) {
  const stats = [
    {
      title: "Agent Interactions",
      value: "23",
      change: "+12%",
      icon: Bot,
      color: "text-blue-600"
    },
    {
      title: "New Connections",
      value: "8",
      change: "+4%",
      icon: Users,
      color: "text-green-600"
    },
    {
      title: "Profile Views",
      value: "156",
      change: "+18%",
      icon: Eye,
      color: "text-purple-600"
    },
    {
      title: "Recommendations",
      value: "12",
      change: "+6%",
      icon: TrendingUp,
      color: "text-orange-600"
    }
  ];

  const recentActivity = [
    {
      type: "agent_connection",
      title: "Your agent connected with Dr. Sarah Chen",
      description: "Discussed machine learning projects and potential collaboration",
      time: "2 hours ago",
      avatar: "https://images.unsplash.com/photo-1494790108755-2616b612b786?w=400&h=400&fit=crop&crop=face"
    },
    {
      type: "recommendation",
      title: "New post recommended: 'The Future of AI in Healthcare'",
      description: "Based on your interests in AI and healthcare technology",
      time: "4 hours ago",
      avatar: null
    },
    {
      type: "connection",
      title: "Mike Torres sent you a connection request",
      description: "Product Manager at InnovateX",
      time: "6 hours ago",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=400&fit=crop&crop=face"
    },
    {
      type: "agent_activity",
      title: "Your agent updated networking preferences",
      description: "Now actively looking for blockchain project collaborators",
      time: "1 day ago",
      avatar: null
    }
  ];

  const agentMetrics = {
    interactions: 23,
    successfulConnections: 8,
    profileMatches: 15,
    responseRate: 87
  };

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div>
        <h1>Welcome back, {user.name.split(' ')[0]}!</h1>
        <p className="text-muted-foreground">Here's what's happening with your Digital Twin agent today.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Card key={index}>
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-muted-foreground">{stat.title}</p>
                    <p className="text-2xl mt-1">{stat.value}</p>
                    <p className="text-xs text-green-600 mt-1">{stat.change} from last week</p>
                  </div>
                  <Icon className={`w-8 h-8 ${stat.color}`} />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agent Status */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Bot className="w-5 h-5" />
              <span>Digital Twin Agent Status</span>
              <Badge variant={user.agentActive ? "default" : "secondary"}>
                {user.agentActive ? "Active" : "Inactive"}
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span>Networking Effectiveness</span>
                  <span>{agentMetrics.responseRate}%</span>
                </div>
                <Progress value={agentMetrics.responseRate} className="h-2" />
              </div>
              
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-2xl">{agentMetrics.interactions}</p>
                  <p className="text-xs text-muted-foreground">Interactions</p>
                </div>
                <div>
                  <p className="text-2xl">{agentMetrics.successfulConnections}</p>
                  <p className="text-xs text-muted-foreground">Connections</p>
                </div>
                <div>
                  <p className="text-2xl">{agentMetrics.profileMatches}</p>
                  <p className="text-xs text-muted-foreground">Matches</p>
                </div>
              </div>
            </div>
            
            <Button className="w-full" variant="outline">
              <Settings className="w-4 h-4 mr-2" />
              Configure Agent
            </Button>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3">
                  {activity.avatar ? (
                    <Avatar className="w-8 h-8">
                      <AvatarImage src={activity.avatar} />
                      <AvatarFallback>U</AvatarFallback>
                    </Avatar>
                  ) : (
                    <div className="w-8 h-8 bg-muted rounded-full flex items-center justify-center">
                      {activity.type === 'agent_connection' && <Bot className="w-4 h-4" />}
                      {activity.type === 'recommendation' && <TrendingUp className="w-4 h-4" />}
                      {activity.type === 'agent_activity' && <Bot className="w-4 h-4" />}
                    </div>
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm">{activity.title}</p>
                    <p className="text-xs text-muted-foreground">{activity.description}</p>
                    <p className="text-xs text-muted-foreground mt-1">{activity.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Briefcase className="w-6 h-6" />
              <span>Update Profile</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <Bot className="w-6 h-6" />
              <span>Configure Agent</span>
            </Button>
            <Button variant="outline" className="h-20 flex-col space-y-2">
              <MessageSquare className="w-6 h-6" />
              <span>View Conversations</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}