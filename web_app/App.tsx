import React, { useState } from 'react';
import { Users, Bot, Home, User, MessageSquare, Settings, Upload, TrendingUp } from 'lucide-react';
import { Button } from './components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from './components/ui/avatar';
import { Badge } from './components/ui/badge';
import { Sidebar } from './components/ui/sidebar';
import { Header } from './components/Header';
import { Dashboard } from './components/Dashboard';
import { Profile } from './components/Profile';
import { AgentConfig } from './components/AgentConfig';
import { Feed } from './components/Feed';
import { AgentNetwork } from './components/AgentNetwork';
import { Connections } from './components/Connections';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user] = useState({
    name: 'Alex Johnson',
    title: 'Senior Software Engineer',
    company: 'TechCorp',
    avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=400&h=400&fit=crop&crop=face',
    connections: 247,
    agentActive: true
  });

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'feed', label: 'Feed', icon: TrendingUp },
    { id: 'agent-network', label: 'Agent Network', icon: Bot },
    { id: 'connections', label: 'Connections', icon: Users },
    { id: 'profile', label: 'Profile', icon: User },
    { id: 'agent-config', label: 'Agent Config', icon: Settings },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard user={user} />;
      case 'profile':
        return <Profile user={user} />;
      case 'agent-config':
        return <AgentConfig user={user} />;
      case 'feed':
        return <Feed user={user} />;
      case 'agent-network':
        return <AgentNetwork user={user} />;
      case 'connections':
        return <Connections user={user} />;
      default:
        return <Dashboard user={user} />;
    }
  };

  return (
    <div className="min-h-screen bg-background flex">
      {/* Sidebar */}
      <div className="w-64 border-r border-border bg-card">
        <div className="p-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
              <Bot className="w-5 h-5 text-primary-foreground" />
            </div>
            <h1 className="font-semibold text-lg">TwinNet</h1>
          </div>
        </div>
        
        <nav className="px-4 pb-6">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-left transition-colors ${
                  activeTab === item.id
                    ? 'bg-primary text-primary-foreground'
                    : 'hover:bg-accent text-foreground'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        {/* User Info */}
        <div className="px-4 mt-auto">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center space-x-3">
                <Avatar className="w-10 h-10">
                  <AvatarImage src={user.avatar} alt={user.name} />
                  <AvatarFallback>{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="truncate">{user.name}</p>
                  <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${user.agentActive ? 'bg-green-500' : 'bg-gray-400'}`} />
                    <span className="text-xs text-muted-foreground">
                      Agent {user.agentActive ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <Header user={user} />
        <main className="p-6">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}