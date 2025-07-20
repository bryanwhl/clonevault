import React, { useState } from 'react';
import { Upload, User, Briefcase, GraduationCap, Award, MapPin, Calendar, Edit2, Save, X } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar';
import { Badge } from './ui/badge';
import { Separator } from './ui/separator';

interface ProfileProps {
  user: {
    name: string;
    title: string;
    company: string;
    avatar: string;
    connections: number;
  };
}

export function Profile({ user }: ProfileProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [profileData, setProfileData] = useState({
    name: user.name,
    title: user.title,
    company: user.company,
    location: "San Francisco, CA",
    bio: "Passionate software engineer with 8+ years of experience in machine learning, healthcare technology, and team leadership. Currently focused on AI applications in medical diagnosis and clinical decision support systems.",
    email: "alex.johnson@email.com",
    linkedin: "linkedin.com/in/alexjohnson",
    website: "alexjohnson.dev"
  });

  const experience = [
    {
      title: "Senior Software Engineer",
      company: "TechCorp",
      duration: "2021 - Present",
      location: "San Francisco, CA",
      description: "Lead development of AI-powered healthcare applications, managing a team of 6 engineers. Built machine learning models for medical image analysis with 94% accuracy."
    },
    {
      title: "Software Engineer",
      company: "InnovateMed",
      duration: "2019 - 2021",
      location: "Palo Alto, CA",
      description: "Developed clinical decision support systems and electronic health record integrations. Improved patient data processing efficiency by 40%."
    },
    {
      title: "Junior Developer",
      company: "StartupX",
      duration: "2017 - 2019",
      location: "San Jose, CA",
      description: "Built full-stack web applications using React and Node.js. Contributed to platform that served 10K+ healthcare professionals."
    }
  ];

  const education = [
    {
      degree: "Master of Science in Computer Science",
      school: "Stanford University",
      year: "2017",
      description: "Focus on Machine Learning and Artificial Intelligence"
    },
    {
      degree: "Bachelor of Science in Computer Engineering",
      school: "UC Berkeley",
      year: "2015",
      description: "Magna Cum Laude, Phi Beta Kappa"
    }
  ];

  const skills = [
    "Machine Learning", "Python", "React", "Node.js", "TensorFlow", "PyTorch", 
    "Healthcare IT", "FHIR", "Medical Imaging", "Team Leadership", "Product Management",
    "AWS", "Docker", "Kubernetes", "PostgreSQL", "MongoDB"
  ];

  const certifications = [
    "AWS Certified Solutions Architect",
    "Google Cloud Professional ML Engineer",
    "Certified Kubernetes Administrator (CKA)",
    "Project Management Professional (PMP)"
  ];

  const handleSave = () => {
    setIsEditing(false);
    // Here you would typically save to backend
  };

  const handleCancel = () => {
    setIsEditing(false);
    // Reset form data
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1>Professional Profile</h1>
        <Button 
          variant={isEditing ? "destructive" : "default"} 
          onClick={() => isEditing ? handleCancel() : setIsEditing(true)}
        >
          {isEditing ? <X className="w-4 h-4 mr-2" /> : <Edit2 className="w-4 h-4 mr-2" />}
          {isEditing ? "Cancel" : "Edit Profile"}
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column - Basic Info */}
        <div className="space-y-6">
          {/* Profile Card */}
          <Card>
            <CardContent className="p-6 text-center">
              <Avatar className="w-24 h-24 mx-auto mb-4">
                <AvatarImage src={user.avatar} alt={user.name} />
                <AvatarFallback className="text-xl">{user.name.split(' ').map(n => n[0]).join('')}</AvatarFallback>
              </Avatar>
              
              {isEditing ? (
                <div className="space-y-3">
                  <Input
                    value={profileData.name}
                    onChange={(e) => setProfileData({...profileData, name: e.target.value})}
                    placeholder="Full Name"
                  />
                  <Input
                    value={profileData.title}
                    onChange={(e) => setProfileData({...profileData, title: e.target.value})}
                    placeholder="Job Title"
                  />
                  <Input
                    value={profileData.company}
                    onChange={(e) => setProfileData({...profileData, company: e.target.value})}
                    placeholder="Company"
                  />
                  <Button className="w-full" onClick={handleSave}>
                    <Save className="w-4 h-4 mr-2" />
                    Save Changes
                  </Button>
                </div>
              ) : (
                <div>
                  <h2>{profileData.name}</h2>
                  <p className="text-muted-foreground">{profileData.title}</p>
                  <p className="text-sm text-muted-foreground">{profileData.company}</p>
                  <div className="flex items-center justify-center mt-2 text-sm text-muted-foreground">
                    <MapPin className="w-4 h-4 mr-1" />
                    {profileData.location}
                  </div>
                  <div className="flex items-center justify-center mt-2">
                    <Badge variant="secondary">{user.connections} connections</Badge>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Contact Info */}
          <Card>
            <CardHeader>
              <CardTitle>Contact Information</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {isEditing ? (
                <div className="space-y-3">
                  <Input
                    type="email"
                    value={profileData.email}
                    onChange={(e) => setProfileData({...profileData, email: e.target.value})}
                    placeholder="Email"
                  />
                  <Input
                    value={profileData.linkedin}
                    onChange={(e) => setProfileData({...profileData, linkedin: e.target.value})}
                    placeholder="LinkedIn URL"
                  />
                  <Input
                    value={profileData.website}
                    onChange={(e) => setProfileData({...profileData, website: e.target.value})}
                    placeholder="Website"
                  />
                </div>
              ) : (
                <div className="space-y-2">
                  <p className="text-sm"><span className="font-medium">Email:</span> {profileData.email}</p>
                  <p className="text-sm"><span className="font-medium">LinkedIn:</span> {profileData.linkedin}</p>
                  <p className="text-sm"><span className="font-medium">Website:</span> {profileData.website}</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Resume Upload */}
          <Card>
            <CardHeader>
              <CardTitle>Resume</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                <Upload className="w-8 h-8 mx-auto mb-4 text-muted-foreground" />
                <p className="text-sm text-muted-foreground mb-2">
                  Upload your resume to enhance your Digital Twin agent's networking capabilities
                </p>
                <Button variant="outline" size="sm">
                  Upload Resume
                </Button>
                <p className="text-xs text-muted-foreground mt-2">
                  PDF, DOC, or DOCX (Max 10MB)
                </p>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Right Column - Detailed Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Bio */}
          <Card>
            <CardHeader>
              <CardTitle>About</CardTitle>
            </CardHeader>
            <CardContent>
              {isEditing ? (
                <Textarea
                  value={profileData.bio}
                  onChange={(e) => setProfileData({...profileData, bio: e.target.value})}
                  rows={4}
                  placeholder="Tell us about yourself..."
                />
              ) : (
                <p>{profileData.bio}</p>
              )}
            </CardContent>
          </Card>

          {/* Experience */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Briefcase className="w-5 h-5 mr-2" />
                Experience
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              {experience.map((exp, index) => (
                <div key={index}>
                  <div className="flex items-start justify-between">
                    <div>
                      <h3>{exp.title}</h3>
                      <p className="text-muted-foreground">{exp.company}</p>
                      <p className="text-sm text-muted-foreground">{exp.location}</p>
                      <p className="text-sm mt-2">{exp.description}</p>
                    </div>
                    <div className="text-sm text-muted-foreground flex items-center">
                      <Calendar className="w-4 h-4 mr-1" />
                      {exp.duration}
                    </div>
                  </div>
                  {index < experience.length - 1 && <Separator className="mt-6" />}
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Education */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <GraduationCap className="w-5 h-5 mr-2" />
                Education
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {education.map((edu, index) => (
                <div key={index}>
                  <h3>{edu.degree}</h3>
                  <p className="text-muted-foreground">{edu.school}</p>
                  <p className="text-sm text-muted-foreground">{edu.year}</p>
                  <p className="text-sm mt-1">{edu.description}</p>
                  {index < education.length - 1 && <Separator className="mt-4" />}
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Skills */}
          <Card>
            <CardHeader>
              <CardTitle>Skills</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {skills.map((skill, index) => (
                  <Badge key={index} variant="secondary">{skill}</Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Certifications */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Award className="w-5 h-5 mr-2" />
                Certifications
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {certifications.map((cert, index) => (
                  <div key={index} className="flex items-center">
                    <Award className="w-4 h-4 mr-2 text-muted-foreground" />
                    <span>{cert}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}