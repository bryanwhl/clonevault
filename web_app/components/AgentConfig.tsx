import React, { useState } from 'react';
import { Bot, Settings, Target, MessageSquare, Brain, Shield, Save, RefreshCw } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Switch } from './ui/switch';
import { Badge } from './ui/badge';
import { Slider } from './ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './ui/select';
import { Label } from './ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Separator } from './ui/separator';

interface AgentConfigProps {
  user: {
    name: string;
    agentActive: boolean;
  };
}

export function AgentConfig({ user }: AgentConfigProps) {
  const [agentConfig, setAgentConfig] = useState({
    isActive: user.agentActive,
    name: "Alex's Professional Twin",
    personalityStyle: "professional",
    networkingGoals: ["research_collaboration", "mentorship", "project_partnerships"],
    communicationStyle: "detailed",
    proactiveness: [7],
    responseTime: "within_hours",
    interests: ["machine_learning", "healthcare_ai", "team_leadership"],
    lookingFor: "I am seeking opportunities to collaborate on healthcare AI projects and contribute to meaningful research that can improve patient outcomes.",
    avoidTopics: ["politics", "personal_finance"],
    maxConversationsPerDay: [10],
    qualityThreshold: [70],
    autoConnect: false,
    sharePublicProfile: true,
    allowDirectMessages: true,
    notifyOnMatches: true
  });

  const personalityOptions = [
    { value: "professional", label: "Professional & Formal" },
    { value: "friendly", label: "Friendly & Approachable" },
    { value: "analytical", label: "Analytical & Data-Driven" },
    { value: "creative", label: "Creative & Innovative" }
  ];

  const networkingGoalOptions = [
    { value: "job_opportunities", label: "Job Opportunities" },
    { value: "research_collaboration", label: "Research Collaboration" },
    { value: "mentorship", label: "Mentorship (Give/Receive)" },
    { value: "project_partnerships", label: "Project Partnerships" },
    { value: "knowledge_sharing", label: "Knowledge Sharing" },
    { value: "business_opportunities", label: "Business Opportunities" }
  ];

  const interestOptions = [
    { value: "machine_learning", label: "Machine Learning" },
    { value: "healthcare_ai", label: "Healthcare AI" },
    { value: "team_leadership", label: "Team Leadership" },
    { value: "product_management", label: "Product Management" },
    { value: "startup_experience", label: "Startup Experience" },
    { value: "blockchain", label: "Blockchain" },
    { value: "cloud_computing", label: "Cloud Computing" },
    { value: "data_science", label: "Data Science" }
  ];

  const handleSaveConfig = () => {
    // Save configuration to backend
    console.log("Saving agent configuration:", agentConfig);
  };

  const handleTestAgent = () => {
    // Test agent configuration
    console.log("Testing agent with current configuration");
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bot className="w-8 h-8" />
          <div>
            <h1>Digital Twin Agent Configuration</h1>
            <p className="text-muted-foreground">Customize how your agent represents you in the network</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Switch 
            checked={agentConfig.isActive}
            onCheckedChange={(checked) => setAgentConfig({...agentConfig, isActive: checked})}
          />
          <Label>Agent {agentConfig.isActive ? 'Active' : 'Inactive'}</Label>
        </div>
      </div>

      {/* Agent Status Card */}
      <Card className={agentConfig.isActive ? "border-green-200 bg-green-50/50" : "border-gray-200"}>
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className={`w-3 h-3 rounded-full ${agentConfig.isActive ? 'bg-green-500' : 'bg-gray-400'}`} />
              <span>Agent Status: {agentConfig.isActive ? 'Active and Networking' : 'Inactive'}</span>
            </div>
            <div className="flex space-x-2">
              <Button variant="outline" size="sm" onClick={handleTestAgent}>
                <RefreshCw className="w-4 h-4 mr-2" />
                Test Configuration
              </Button>
              <Button onClick={handleSaveConfig}>
                <Save className="w-4 h-4 mr-2" />
                Save Changes
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="personality" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="personality">Personality</TabsTrigger>
          <TabsTrigger value="networking">Networking</TabsTrigger>
          <TabsTrigger value="preferences">Preferences</TabsTrigger>
          <TabsTrigger value="privacy">Privacy</TabsTrigger>
        </TabsList>

        {/* Personality Tab */}
        <TabsContent value="personality" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Brain className="w-5 h-5 mr-2" />
                Agent Personality
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Agent Name</Label>
                <Input
                  value={agentConfig.name}
                  onChange={(e) => setAgentConfig({...agentConfig, name: e.target.value})}
                  placeholder="Give your agent a name"
                />
              </div>

              <div className="space-y-2">
                <Label>Communication Style</Label>
                <Select 
                  value={agentConfig.personalityStyle} 
                  onValueChange={(value) => setAgentConfig({...agentConfig, personalityStyle: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select communication style" />
                  </SelectTrigger>
                  <SelectContent>
                    {personalityOptions.map((option) => (
                      <SelectItem key={option.value} value={option.value}>
                        {option.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Proactiveness Level: {agentConfig.proactiveness[0]}/10</Label>
                <Slider
                  value={agentConfig.proactiveness}
                  onValueChange={(value) => setAgentConfig({...agentConfig, proactiveness: value})}
                  max={10}
                  min={1}
                  step={1}
                />
                <p className="text-xs text-muted-foreground">
                  How actively should your agent initiate conversations and seek connections?
                </p>
              </div>

              <div className="space-y-2">
                <Label>Response Time Preference</Label>
                <Select 
                  value={agentConfig.responseTime} 
                  onValueChange={(value) => setAgentConfig({...agentConfig, responseTime: value})}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="immediate">Immediate (within minutes)</SelectItem>
                    <SelectItem value="within_hours">Within hours</SelectItem>
                    <SelectItem value="daily">Daily check-ins</SelectItem>
                    <SelectItem value="weekly">Weekly summaries</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Networking Tab */}
        <TabsContent value="networking" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2" />
                Networking Goals & Interests
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Primary Networking Goals</Label>
                <div className="grid grid-cols-2 gap-2">
                  {networkingGoalOptions.map((goal) => (
                    <div key={goal.value} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        id={goal.value}
                        checked={agentConfig.networkingGoals.includes(goal.value)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setAgentConfig({
                              ...agentConfig,
                              networkingGoals: [...agentConfig.networkingGoals, goal.value]
                            });
                          } else {
                            setAgentConfig({
                              ...agentConfig,
                              networkingGoals: agentConfig.networkingGoals.filter(g => g !== goal.value)
                            });
                          }
                        }}
                      />
                      <label htmlFor={goal.value} className="text-sm">{goal.label}</label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>Professional Interests</Label>
                <div className="flex flex-wrap gap-2">
                  {interestOptions.map((interest) => (
                    <Badge
                      key={interest.value}
                      variant={agentConfig.interests.includes(interest.value) ? "default" : "secondary"}
                      className="cursor-pointer"
                      onClick={() => {
                        if (agentConfig.interests.includes(interest.value)) {
                          setAgentConfig({
                            ...agentConfig,
                            interests: agentConfig.interests.filter(i => i !== interest.value)
                          });
                        } else {
                          setAgentConfig({
                            ...agentConfig,
                            interests: [...agentConfig.interests, interest.value]
                          });
                        }
                      }}
                    >
                      {interest.label}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label>What Are You Looking For?</Label>
                <Textarea
                  value={agentConfig.lookingFor}
                  onChange={(e) => setAgentConfig({...agentConfig, lookingFor: e.target.value})}
                  rows={3}
                  placeholder="Describe what you're looking for in your professional network..."
                />
              </div>

              <div className="space-y-2">
                <Label>Topics to Avoid</Label>
                <Input
                  value={agentConfig.avoidTopics.join(", ")}
                  onChange={(e) => setAgentConfig({
                    ...agentConfig, 
                    avoidTopics: e.target.value.split(", ").filter(t => t.trim())
                  })}
                  placeholder="e.g., politics, personal finance"
                />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Preferences Tab */}
        <TabsContent value="preferences" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Settings className="w-5 h-5 mr-2" />
                Agent Preferences
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label>Maximum Conversations Per Day: {agentConfig.maxConversationsPerDay[0]}</Label>
                <Slider
                  value={agentConfig.maxConversationsPerDay}
                  onValueChange={(value) => setAgentConfig({...agentConfig, maxConversationsPerDay: value})}
                  max={20}
                  min={1}
                  step={1}
                />
              </div>

              <div className="space-y-2">
                <Label>Connection Quality Threshold: {agentConfig.qualityThreshold[0]}%</Label>
                <Slider
                  value={agentConfig.qualityThreshold}
                  onValueChange={(value) => setAgentConfig({...agentConfig, qualityThreshold: value})}
                  max={100}
                  min={50}
                  step={5}
                />
                <p className="text-xs text-muted-foreground">
                  Minimum compatibility score required before engaging in conversation
                </p>
              </div>

              <Separator />

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Auto-Connect on High Matches</Label>
                    <p className="text-sm text-muted-foreground">
                      Automatically send connection requests for matches above 90%
                    </p>
                  </div>
                  <Switch
                    checked={agentConfig.autoConnect}
                    onCheckedChange={(checked) => setAgentConfig({...agentConfig, autoConnect: checked})}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <Label>Notify on New Matches</Label>
                    <p className="text-sm text-muted-foreground">
                      Get notified when your agent finds potential connections
                    </p>
                  </div>
                  <Switch
                    checked={agentConfig.notifyOnMatches}
                    onCheckedChange={(checked) => setAgentConfig({...agentConfig, notifyOnMatches: checked})}
                  />
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Privacy Tab */}
        <TabsContent value="privacy" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Shield className="w-5 h-5 mr-2" />
                Privacy & Security Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <Label>Share Public Profile</Label>
                    <p className="text-sm text-muted-foreground">
                      Allow your agent to share basic profile information during conversations
                    </p>
                  </div>
                  <Switch
                    checked={agentConfig.sharePublicProfile}
                    onCheckedChange={(checked) => setAgentConfig({...agentConfig, sharePublicProfile: checked})}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <Label>Allow Direct Messages</Label>
                    <p className="text-sm text-muted-foreground">
                      Permit other users to message you directly after successful agent connections
                    </p>
                  </div>
                  <Switch
                    checked={agentConfig.allowDirectMessages}
                    onCheckedChange={(checked) => setAgentConfig({...agentConfig, allowDirectMessages: checked})}
                  />
                </div>
              </div>

              <Separator />

              <div className="bg-muted p-4 rounded-lg">
                <h4 className="mb-2">Data Usage</h4>
                <p className="text-sm text-muted-foreground">
                  Your agent uses information from your profile, resume, and preferences to represent you professionally. 
                  No personal or sensitive information is shared without explicit consent.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}