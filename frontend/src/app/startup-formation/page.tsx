"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertCircle, CheckCircle, Clock, Play, Eye, Download, Settings, Zap } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import WorkflowVisualization from '@/components/workflow-visualization';
import PlotlyWorkflowVisualization from '@/components/plotly-workflow-visualization';

interface WorkflowStep {
  step_id: string;
  name: string;
  description: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  estimated_duration: number;
  actual_duration?: number;
  started_at?: string;
  completed_at?: string;
  result?: any;
  error?: string;
}

interface Workflow {
  workflow_id: string;
  company_name: string;
  status: string;
  progress: number;
  current_step?: string;
  created_at: string;
  estimated_completion: string;
  steps?: WorkflowStep[];
}

interface WorkflowTemplate {
  name: string;
  description: string;
  estimated_duration: string;
  steps: number;
  states_supported: string[];
}

export default function StartupFormationPage() {
  const [activeTab, setActiveTab] = useState('create');
  const [workflows, setWorkflows] = useState<Workflow[]>([]);
  const [templates, setTemplates] = useState<{ [key: string]: WorkflowTemplate }>({});
  const [selectedWorkflow, setSelectedWorkflow] = useState<Workflow | null>(null);
  const [workflowVisualization, setWorkflowVisualization] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);

  // Form state for creating new workflow
  const [formData, setFormData] = useState({
    companyName: '',
    entityType: 'llc',
    state: 'washington',
    industry: 'technology',
    description: '',
    founderName: '',
    founderEmail: '',
    founderRole: 'ceo'
  });

  useEffect(() => {
    loadWorkflows();
    loadTemplates();
  }, []);

  const loadWorkflows = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v2/startup/workflows');
      if (response.ok) {
        const data = await response.json();
        setWorkflows(data.workflows || []);
      }
    } catch (error) {
      console.error('Failed to load workflows:', error);
    }
  };

  const loadTemplates = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v2/startup/templates');
      if (response.ok) {
        const data = await response.json();
        setTemplates(data.templates || {});
      }
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
  };

  const createWorkflow = async () => {
    if (!formData.companyName || !formData.founderName || !formData.founderEmail) {
      alert('Please fill in all required fields');
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v2/startup/workflows', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_name: formData.companyName,
          entity_type: formData.entityType,
          state: formData.state,
          industry: formData.industry,
          description: formData.description,
          founder_name: formData.founderName,
          founder_email: formData.founderEmail,
          founder_role: formData.founderRole
        }),
      });

      if (response.ok) {
        const data = await response.json();
        alert(`Workflow created successfully! Company: ${formData.companyName}`);
        loadWorkflows();
        setActiveTab('monitor');

        // Reset form
        setFormData({
          companyName: '',
          entityType: 'llc',
          state: 'washington',
          industry: 'technology',
          description: '',
          founderName: '',
          founderEmail: '',
          founderRole: 'ceo'
        });
      } else {
        const errorData = await response.json().catch(() => ({}));
        alert(`Failed to create workflow: ${errorData.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Error creating workflow:', error);
      alert('Error creating workflow. Please check if the backend server is running.');
    }
    setIsLoading(false);
  };

  const handleWorkflowClick = (workflow: Workflow) => {
    setSelectedWorkflow(workflow);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          🚀 Startup Formation Platform
        </h1>
        <p className="text-gray-600">
          AI-powered end-to-end startup formation with multi-founder support and visual progress tracking
        </p>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="create">Create Workflow</TabsTrigger>
          <TabsTrigger value="monitor">Monitor Workflows</TabsTrigger>
          <TabsTrigger value="templates">Templates</TabsTrigger>
        </TabsList>

        <TabsContent value="create" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Create New Startup Formation Workflow</CardTitle>
              <CardDescription>
                Start the automated process of forming your business entity
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div>
                    <Label htmlFor="companyName">Company Name *</Label>
                    <Input
                      id="companyName"
                      value={formData.companyName}
                      onChange={(e) => setFormData({...formData, companyName: e.target.value})}
                      placeholder="Enter your company name"
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label htmlFor="entityType">Entity Type</Label>
                      <Select value={formData.entityType} onValueChange={(value) => setFormData({...formData, entityType: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="llc">LLC</SelectItem>
                          <SelectItem value="corporation">Corporation</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>

                    <div>
                      <Label htmlFor="state">State</Label>
                      <Select value={formData.state} onValueChange={(value) => setFormData({...formData, state: value})}>
                        <SelectTrigger>
                          <SelectValue />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="washington">Washington</SelectItem>
                          <SelectItem value="california">California</SelectItem>
                          <SelectItem value="texas">Texas</SelectItem>
                          <SelectItem value="florida">Florida</SelectItem>
                          <SelectItem value="new_york">New York</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>

                  <div>
                    <Label htmlFor="industry">Industry</Label>
                    <Select value={formData.industry} onValueChange={(value) => setFormData({...formData, industry: value})}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="technology">Technology</SelectItem>
                        <SelectItem value="healthcare">Healthcare</SelectItem>
                        <SelectItem value="finance">Finance</SelectItem>
                        <SelectItem value="retail">Retail</SelectItem>
                        <SelectItem value="consulting">Consulting</SelectItem>
                        <SelectItem value="manufacturing">Manufacturing</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-4">
                  <div>
                    <Label htmlFor="founderName">Founder Name *</Label>
                    <Input
                      id="founderName"
                      value={formData.founderName}
                      onChange={(e) => setFormData({...formData, founderName: e.target.value})}
                      placeholder="Enter founder name"
                    />
                  </div>

                  <div>
                    <Label htmlFor="founderEmail">Founder Email *</Label>
                    <Input
                      id="founderEmail"
                      type="email"
                      value={formData.founderEmail}
                      onChange={(e) => setFormData({...formData, founderEmail: e.target.value})}
                      placeholder="Enter founder email"
                    />
                  </div>

                  <div>
                    <Label htmlFor="founderRole">Founder Role</Label>
                    <Select value={formData.founderRole} onValueChange={(value) => setFormData({...formData, founderRole: value})}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="ceo">CEO</SelectItem>
                        <SelectItem value="cfo">CFO</SelectItem>
                        <SelectItem value="cto">CTO</SelectItem>
                        <SelectItem value="founder">Founder</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="description">Business Description</Label>
                    <textarea
                      id="description"
                      className="w-full p-2 border rounded-md"
                      rows={3}
                      value={formData.description}
                      onChange={(e) => setFormData({...formData, description: e.target.value})}
                      placeholder="Brief description of your business"
                    />
                  </div>
                </div>
              </div>

              <div className="flex justify-end">
                <Button onClick={createWorkflow} disabled={isLoading} className="min-w-32">
                  {isLoading ? 'Creating...' : 'Create Workflow'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="monitor" className="space-y-6">
          <div className="grid gap-6">
            {workflows.length === 0 ? (
              <Card>
                <CardContent className="p-8 text-center">
                  <p className="text-gray-500">No workflows found. Create your first startup formation workflow!</p>
                </CardContent>
              </Card>
            ) : (
              workflows.map((workflow) => (
                <Card key={workflow.workflow_id} className="cursor-pointer hover:shadow-md transition-shadow"
                      onClick={() => setSelectedWorkflow(workflow)}>
                  <CardHeader>
                    <div className="flex justify-between items-start">
                      <div>
                        <CardTitle className="flex items-center gap-2">
                          {workflow.company_name}
                          <Badge className={getStatusColor(workflow.status)}>
                            {workflow.status.replace('_', ' ').toUpperCase()}
                          </Badge>
                        </CardTitle>
                        <CardDescription>
                          Created: {new Date(workflow.created_at).toLocaleDateString()}
                        </CardDescription>
                      </div>
                      <div className="text-right">
                        <div className="text-sm text-gray-500">Progress</div>
                        <div className="text-2xl font-bold text-blue-600">{Math.round(workflow.progress)}%</div>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <Progress value={workflow.progress} className="w-full" />

                      <div className="flex justify-between text-sm text-gray-600">
                        <span>Current: {workflow.current_step || 'Initializing'}</span>
                        <span>Est. completion: {new Date(workflow.estimated_completion).toLocaleDateString()}</span>
                      </div>

                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          <Eye className="w-4 h-4 mr-1" />
                          View Details
                        </Button>
                        <Button variant="outline" size="sm">
                          <Download className="w-4 h-4 mr-1" />
                          Export Logs
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </TabsContent>

        <TabsContent value="templates" className="space-y-6">
          <div className="grid gap-6 md:grid-cols-2">
            {Object.entries(templates).map(([key, template]) => (
              <Card key={key}>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {template.name}
                    <Badge variant="secondary">{key.toUpperCase()}</Badge>
                  </CardTitle>
                  <CardDescription>{template.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <span className="font-medium">Duration:</span>
                        <p className="text-gray-600">{template.estimated_duration}</p>
                      </div>
                      <div>
                        <span className="font-medium">Steps:</span>
                        <p className="text-gray-600">{template.steps} steps</p>
                      </div>
                    </div>

                    <div>
                      <span className="font-medium">States Supported:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {template.states_supported.map((state) => (
                          <Badge key={state} variant="outline" className="text-xs">
                            {state}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <Button className="w-full">
                      <Play className="w-4 h-4 mr-2" />
                      Use This Template
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabsContent>
      </Tabs>

      {/* Workflow Detail Modal/Card */}
      {selectedWorkflow && (
        <Card className="mt-6">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              {selectedWorkflow.company_name} - Workflow Details
              <Button variant="outline" onClick={() => setSelectedWorkflow(null)}>
                Close
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {/* Workflow Progress Overview */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="text-center p-4 bg-blue-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{Math.round(selectedWorkflow.progress)}%</div>
                  <div className="text-sm text-blue-800">Complete</div>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">
                    {selectedWorkflow.steps ? selectedWorkflow.steps.filter(s => s.status === 'completed').length : 0}
                  </div>
                  <div className="text-sm text-green-800">Steps Done</div>
                </div>
                <div className="text-center p-4 bg-purple-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">
                    {selectedWorkflow.steps ? selectedWorkflow.steps.filter(s => s.status === 'pending').length : 0}
                  </div>
                  <div className="text-sm text-purple-800">Remaining</div>
                </div>
              </div>

              {/* Workflow Visualization */}
              <Tabs value="visualization" className="w-full">
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="mermaid">Mermaid Diagram</TabsTrigger>
                  <TabsTrigger value="plotly">Interactive Workflow</TabsTrigger>
                </TabsList>

                <TabsContent value="mermaid" className="space-y-4">
                  <WorkflowVisualization
                    mermaidDiagram={workflowVisualization}
                    workflowId={selectedWorkflow.workflow_id}
                  />
                </TabsContent>

                <TabsContent value="plotly" className="space-y-4">
                  <PlotlyWorkflowVisualization
                    workflowId={selectedWorkflow.workflow_id}
                    onNodeClick={(nodeId) => {
                      console.log('Node clicked:', nodeId);
                    }}
                    onApprovalRequired={(nodeId) => {
                      console.log('Approval required for node:', nodeId);
                      alert(`Manual approval required for step: ${nodeId}`);
                    }}
                  />
                </TabsContent>
              </Tabs>

              {/* Current Step Information */}
              {selectedWorkflow.current_step && (
                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <h4 className="font-medium text-yellow-800 mb-2">Currently Processing</h4>
                  <p className="text-yellow-700">
                    Step: {selectedWorkflow.current_step.replace('_', ' ').toUpperCase()}
                  </p>
                  <p className="text-sm text-yellow-600 mt-1">
                    Estimated completion: {new Date(selectedWorkflow.estimated_completion).toLocaleString()}
                  </p>
                </div>
              )}

              {/* Business Registration Checklist */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <CheckCircle className="w-5 h-5" />
                    Business Registration Checklist
                  </CardTitle>
                  <CardDescription>
                    Track all requirements for {selectedWorkflow.company_name} formation
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                        </div>
                        <div>
                          <p className="font-medium">Business Name Available</p>
                          <p className="text-sm text-gray-600">Checked with WA SOS</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-green-100 flex items-center justify-center">
                          <CheckCircle className="w-4 h-4 text-green-600" />
                        </div>
                        <div>
                          <p className="font-medium">Articles of Organization</p>
                          <p className="text-sm text-gray-600">Generated and prepared</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-blue-100 flex items-center justify-center">
                          <Clock className="w-4 h-4 text-blue-600" />
                        </div>
                        <div>
                          <p className="font-medium">WA SOS Filing</p>
                          <p className="text-sm text-gray-600">Pending submission</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <Clock className="w-4 h-4 text-gray-400" />
                        </div>
                        <div>
                          <p className="font-medium">WA DOR Registration</p>
                          <p className="text-sm text-gray-600">Pending</p>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <Clock className="w-4 h-4 text-gray-400" />
                        </div>
                        <div>
                          <p className="font-medium">Tax Account Setup</p>
                          <p className="text-sm text-gray-600">Pending</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center">
                          <AlertCircle className="w-4 h-4 text-amber-600" />
                        </div>
                        <div>
                          <p className="font-medium">Manual Approval Required</p>
                          <p className="text-sm text-gray-600">Review documents before final registration</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <Clock className="w-4 h-4 text-gray-400" />
                        </div>
                        <div>
                          <p className="font-medium">EIN Application</p>
                          <p className="text-sm text-gray-600">Pending</p>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <Clock className="w-4 h-4 text-gray-400" />
                        </div>
                        <div>
                          <p className="font-medium">Formation Complete</p>
                          <p className="text-sm text-gray-600">Pending</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Document Management */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Download className="w-5 h-5" />
                    Document Management
                  </CardTitle>
                  <CardDescription>
                    Generated documents for {selectedWorkflow.company_name}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="p-4 border rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium">Articles of Organization</h4>
                          <Badge className="bg-green-100 text-green-800">Ready</Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                          Legal document for LLC formation in Washington State
                        </p>
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline">
                            <Eye className="w-4 h-4 mr-1" />
                            Preview
                          </Button>
                          <Button size="sm" variant="outline">
                            <Download className="w-4 h-4 mr-1" />
                            Download
                          </Button>
                        </div>
                      </div>

                      <div className="p-4 border rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-medium">Operating Agreement</h4>
                          <Badge className="bg-blue-100 text-blue-800">Generating</Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-3">
                          Internal agreement defining LLC operations and ownership
                        </p>
                        <div className="flex gap-2">
                          <Button size="sm" variant="outline" disabled>
                            <Eye className="w-4 h-4 mr-1" />
                            Preview
                          </Button>
                          <Button size="sm" variant="outline" disabled>
                            <Download className="w-4 h-4 mr-1" />
                            Download
                          </Button>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Integration Status */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Zap className="w-5 h-5" />
                    Integration Status
                  </CardTitle>
                  <CardDescription>
                    Connected government and business services
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 border rounded-lg">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      </div>
                      <h4 className="font-medium text-sm">WA Secretary of State</h4>
                      <p className="text-xs text-gray-600">Connected</p>
                    </div>

                    <div className="text-center p-4 border rounded-lg">
                      <div className="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                      </div>
                      <h4 className="font-medium text-sm">WA Dept. of Revenue</h4>
                      <p className="text-xs text-gray-600">Connected</p>
                    </div>

                    <div className="text-center p-4 border rounded-lg">
                      <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-2">
                        <Clock className="w-5 h-5 text-blue-600" />
                      </div>
                      <h4 className="font-medium text-sm">IRS EIN Service</h4>
                      <p className="text-xs text-gray-600">Pending</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Workflow Controls */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Settings className="w-5 h-5" />
                    Workflow Controls
                  </CardTitle>
                  <CardDescription>
                    Manage and control the startup formation process
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-3">
                    <Button variant="outline" className="flex items-center gap-2">
                      <Play className="w-4 h-4" />
                      Resume Workflow
                    </Button>
                    <Button variant="outline" className="flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      Pause Workflow
                    </Button>
                    <Button variant="outline" className="flex items-center gap-2">
                      <AlertCircle className="w-4 h-4" />
                      Retry Failed Steps
                    </Button>
                    <Button variant="outline" className="flex items-center gap-2">
                      <Download className="w-4 h-4" />
                      Export Workflow Data
                    </Button>
                  </div>

                  <div className="mt-4 p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-2">📋 Next Steps</h4>
                    <ul className="text-sm text-blue-700 space-y-1">
                      <li>• Complete manual document review and approval</li>
                      <li>• Submit registration documents to WA SOS</li>
                      <li>• Set up business banking with EIN</li>
                      <li>• Configure payroll and HR systems</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
