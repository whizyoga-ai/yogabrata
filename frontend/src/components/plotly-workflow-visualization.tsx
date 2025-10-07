"use client";

import React, { useEffect, useRef, useState } from 'react';
import dynamic from 'next/dynamic';

// Dynamically import plotly.js to avoid SSR issues
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

interface WorkflowNode {
  id: string;
  name: string;
  type: 'start' | 'process' | 'decision' | 'mcp' | 'approval' | 'end';
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'waiting_approval';
  x: number;
  y: number;
  data?: any;
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type: 'normal' | 'conditional' | 'error';
}

interface WorkflowNode {
  id: string;
  name: string;
  type: 'start' | 'process' | 'decision' | 'mcp' | 'approval' | 'end';
  status: 'pending' | 'in_progress' | 'completed' | 'failed' | 'waiting_approval';
  x: number;
  y: number;
  data?: any;
}

interface WorkflowEdge {
  id: string;
  source: string;
  target: string;
  type: 'normal' | 'conditional' | 'error';
}

interface PlotlyWorkflowVisualizationProps {
  workflowId?: string;
  nodes?: WorkflowNode[];
  edges?: WorkflowEdge[];
  onNodeClick?: (nodeId: string) => void;
  onApprovalRequired?: (nodeId: string) => void;
}

export default function PlotlyWorkflowVisualization({
  workflowId,
  nodes: initialNodes = [],
  edges: initialEdges = [],
  onNodeClick,
  onApprovalRequired
}: PlotlyWorkflowVisualizationProps) {
  const [plotlyLoaded, setPlotlyLoaded] = useState(false);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [nodes, setNodes] = useState<WorkflowNode[]>(initialNodes);
  const [edges, setEdges] = useState<WorkflowEdge[]>(initialEdges);

  useEffect(() => {
    // Update state when props change
    setNodes(initialNodes);
    setEdges(initialEdges);
  }, [initialNodes, initialEdges]);

  useEffect(() => {
    // Simulate loading workflow data if not provided
    if (nodes.length === 0) {
      loadDefaultWorkflow();
    }
  }, []);

  const loadDefaultWorkflow = () => {
    // Default startup formation workflow nodes
    const defaultNodes: WorkflowNode[] = [
      {
        id: 'start',
        name: 'Start Formation',
        type: 'start',
        status: 'completed',
        x: 0,
        y: 0
      },
      {
        id: 'analyze',
        name: 'Analyze Requirements',
        type: 'process',
        status: 'completed',
        x: 200,
        y: 0
      },
      {
        id: 'name_check',
        name: 'Check Name Availability',
        type: 'mcp',
        status: 'completed',
        x: 400,
        y: -100,
        data: { mcp_server: 'wa_sos', endpoint: '/name-availability' }
      },
      {
        id: 'prepare_docs',
        name: 'Prepare Articles',
        type: 'process',
        status: 'in_progress',
        x: 600,
        y: 0
      },
      {
        id: 'dor_registration',
        name: 'WA DOR Registration',
        type: 'mcp',
        status: 'pending',
        x: 800,
        y: -200,
        data: { mcp_server: 'wa_dor', endpoint: '/business-registration' }
      },
      {
        id: 'sos_filing',
        name: 'SOS Filing',
        type: 'mcp',
        status: 'pending',
        x: 800,
        y: 0,
        data: { mcp_server: 'wa_sos', endpoint: '/file-articles' }
      },
      {
        id: 'tax_setup',
        name: 'Tax Account Setup',
        type: 'mcp',
        status: 'pending',
        x: 800,
        y: 200,
        data: { mcp_server: 'wa_dor', endpoint: '/tax-accounts' }
      },
      {
        id: 'manual_approval',
        name: 'Manual Approval Required',
        type: 'approval',
        status: 'waiting_approval',
        x: 1000,
        y: 0,
        data: { requires_review: true, documents: ['articles', 'registrations'] }
      },
      {
        id: 'final_registration',
        name: 'Final Registration',
        type: 'process',
        status: 'pending',
        x: 1200,
        y: 0
      },
      {
        id: 'complete',
        name: 'Formation Complete',
        type: 'end',
        status: 'pending',
        x: 1400,
        y: 0
      }
    ];

    const defaultEdges: WorkflowEdge[] = [
      { id: 'e1', source: 'start', target: 'analyze', type: 'normal' },
      { id: 'e2', source: 'analyze', target: 'name_check', type: 'normal' },
      { id: 'e3', source: 'name_check', target: 'prepare_docs', type: 'normal' },
      { id: 'e4', source: 'prepare_docs', target: 'dor_registration', type: 'normal' },
      { id: 'e5', source: 'prepare_docs', target: 'sos_filing', type: 'normal' },
      { id: 'e6', source: 'dor_registration', target: 'tax_setup', type: 'normal' },
      { id: 'e7', source: 'sos_filing', target: 'manual_approval', type: 'normal' },
      { id: 'e8', source: 'tax_setup', target: 'manual_approval', type: 'normal' },
      { id: 'e9', source: 'manual_approval', target: 'final_registration', type: 'conditional' },
      { id: 'e10', source: 'final_registration', target: 'complete', type: 'normal' }
    ];

    // Update state with default data
    setNodes(defaultNodes);
    setEdges(defaultEdges);
  };

  const getNodeColor = (node: WorkflowNode): string => {
    switch (node.status) {
      case 'completed': return '#10B981'; // green
      case 'in_progress': return '#3B82F6'; // blue
      case 'failed': return '#EF4444'; // red
      case 'waiting_approval': return '#F59E0B'; // amber
      case 'pending':
      default: return '#6B7280'; // gray
    }
  };

  const getNodeSymbol = (node: WorkflowNode): string => {
    switch (node.type) {
      case 'start': return 'circle';
      case 'end': return 'square';
      case 'decision': return 'diamond';
      case 'approval': return 'star';
      case 'mcp': return 'triangle-up';
      case 'process':
      default: return 'circle';
    }
  };

  const getNodeSize = (node: WorkflowNode): number => {
    switch (node.type) {
      case 'start':
      case 'end': return 20;
      case 'approval': return 18;
      case 'mcp': return 16;
      case 'process':
      case 'decision':
      default: return 14;
    }
  };

  const handleNodeClick = (event: any) => {
    if (event.points && event.points.length > 0) {
      const point = event.points[0];
      const nodeId = point.customdata;

      setSelectedNode(nodeId);

      if (onNodeClick) {
        onNodeClick(nodeId);
      }

      // Handle approval requirement
      const node = nodes.find(n => n.id === nodeId);
      if (node && node.type === 'approval' && node.status === 'waiting_approval' && onApprovalRequired) {
        onApprovalRequired(nodeId);
      }
    }
  };

  const handleApprovalAction = (approved: boolean) => {
    if (selectedNode) {
      // Update node status based on approval
      const updatedNodes = nodes.map(node =>
        node.id === selectedNode
          ? { ...node, status: approved ? 'completed' : 'failed' as const }
          : node
      );
      setNodes(updatedNodes);

      if (approved) {
        // Trigger next steps in workflow
        console.log('Approval granted, proceeding with registration...');
      }
    }
  };

  // Prepare data for Plotly
  const nodeX = nodes.map(node => node.x);
  const nodeY = nodes.map(node => node.y);
  const nodeColors = nodes.map(node => getNodeColor(node));
  const nodeSymbols = nodes.map(node => getNodeSymbol(node));
  const nodeSizes = nodes.map(node => getNodeSize(node));
  const nodeText = nodes.map(node => node.name);
  const nodeCustomData = nodes.map(node => node.id);

  // Prepare edges for Plotly
  const edgeX: number[] = [];
  const edgeY: number[] = [];
  const edgeText: string[] = [];

  edges.forEach(edge => {
    const sourceNode = nodes.find(n => n.id === edge.source);
    const targetNode = nodes.find(n => n.id === edge.target);

    if (sourceNode && targetNode) {
      edgeX.push(sourceNode.x, targetNode.x, null);
      edgeY.push(sourceNode.y, targetNode.y, null);
      edgeText.push(`${sourceNode.name} → ${targetNode.name}`);
    }
  });

  const plotData = [
    // Edges (lines)
    {
      x: edgeX,
      y: edgeY,
      mode: 'lines+text',
      type: 'scatter',
      line: { color: '#374151', width: 2 },
      text: edgeText,
      textposition: 'middle right',
      hoverinfo: 'text',
      showlegend: false
    },
    // Nodes
    {
      x: nodeX,
      y: nodeY,
      mode: 'markers+text',
      type: 'scatter',
      marker: {
        size: nodeSizes,
        color: nodeColors,
        symbol: nodeSymbols,
        line: { width: 2, color: '#fff' }
      },
      text: nodeText,
      textposition: 'top center',
      hovertemplate: '%{text}<br>Status: %{customdata}<extra></extra>',
      customdata: nodes.map(node => {
        const statusMap = {
          'completed': '✅ Completed',
          'in_progress': '🔄 In Progress',
          'failed': '❌ Failed',
          'waiting_approval': '⏳ Waiting Approval',
          'pending': '⏳ Pending'
        };
        return statusMap[node.status] || node.status;
      }),
      showlegend: false
    }
  ];

  const plotLayout = {
    title: {
      text: '🚀 Startup Formation Workflow',
      font: { size: 16, color: '#1f2937' }
    },
    xaxis: {
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      range: [-50, 1450]
    },
    yaxis: {
      showgrid: false,
      zeroline: false,
      showticklabels: false,
      range: [-300, 300]
    },
    margin: { l: 20, r: 20, t: 60, b: 20 },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
    font: { family: 'Inter, system-ui, sans-serif' }
  };

  const plotConfig = {
    displayModeBar: true,
    displaylogo: false,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
    modeBarButtonsToAdd: [
      {
        name: 'Reset View',
        icon: {
          width: 500,
          height: 600,
          path: 'M256 48C150 48 64 136 64 240s86 192 192 192 192-86 192-192S362 48 256 48zm0 320c-70.7 0-128-57.3-128-128S185.3 112 256 112s128 57.3 128 128-57.3 128-128 128zm0-96c-35.3 0-64 28.7-64 64s28.7 64 64 64 64-28.7 64-64-28.7-64-64-64z'
        },
        click: function() {
          // Reset to default view
          window.location.reload();
        }
      }
    ]
  };

  if (!plotlyLoaded) {
    return (
      <div className="flex items-center justify-center h-96 bg-gray-50 rounded-lg">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading interactive workflow visualization...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="workflow-visualization space-y-4">
      {/* Controls */}
      <div className="flex justify-between items-center">
        <div className="flex gap-2">
          <button
            onClick={() => setSelectedNode(null)}
            className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded"
          >
            Deselect
          </button>
          <button
            onClick={() => {
              // Simulate workflow progression
              const pendingNodes = nodes.filter(n => n.status === 'pending');
              if (pendingNodes.length > 0) {
                const nextNode = pendingNodes[0];
                const updatedNodes = nodes.map(n =>
                  n.id === nextNode.id ? { ...n, status: 'in_progress' as const } : n
                );
                setNodes(updatedNodes);
              }
            }}
            className="px-3 py-1 text-sm bg-blue-600 text-white hover:bg-blue-700 rounded"
          >
            ▶️ Auto Progress
          </button>
        </div>

        <div className="text-sm text-gray-600">
          Click nodes to interact • Hover for details
        </div>
      </div>

      {/* Plotly Chart */}
      <div className="border border-gray-200 rounded-lg bg-white p-4">
        <Plot
          data={plotData}
          layout={plotLayout}
          config={plotConfig}
          style={{ width: '100%', height: '500px' }}
          onClick={handleNodeClick}
          onInitialized={() => setPlotlyLoaded(true)}
        />
      </div>

      {/* Node Details Panel */}
      {selectedNode && (
        <div className="border border-gray-200 rounded-lg bg-gray-50 p-4">
          {(() => {
            const node = nodes.find(n => n.id === selectedNode);
            if (!node) return null;

            return (
              <div className="space-y-3">
                <div className="flex justify-between items-start">
                  <h3 className="font-semibold text-lg">{node.name}</h3>
                  <div className={`px-2 py-1 rounded text-xs font-medium ${
                    node.status === 'completed' ? 'bg-green-100 text-green-800' :
                    node.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                    node.status === 'failed' ? 'bg-red-100 text-red-800' :
                    node.status === 'waiting_approval' ? 'bg-amber-100 text-amber-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {node.status.replace('_', ' ').toUpperCase()}
                  </div>
                </div>

                <p className="text-gray-600">
                  Type: {node.type.toUpperCase()} •
                  Position: ({node.x}, {node.y})
                </p>

                {node.data && (
                  <div className="bg-white p-3 rounded border">
                    <h4 className="font-medium mb-2">Node Data:</h4>
                    <pre className="text-xs text-gray-600 overflow-x-auto">
                      {JSON.stringify(node.data, null, 2)}
                    </pre>
                  </div>
                )}

                {/* Approval Controls */}
                {node.type === 'approval' && node.status === 'waiting_approval' && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                    <h4 className="font-medium text-amber-800 mb-3">⚖️ Manual Approval Required</h4>
                    <p className="text-amber-700 text-sm mb-4">
                      This step requires manual review of the generated documents before proceeding with registration.
                    </p>
                    <div className="flex gap-3">
                      <button
                        onClick={() => handleApprovalAction(true)}
                        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                      >
                        ✅ Approve & Continue
                      </button>
                      <button
                        onClick={() => handleApprovalAction(false)}
                        className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                      >
                        ❌ Reject & Retry
                      </button>
                    </div>
                  </div>
                )}

                {/* MCP Server Info */}
                {node.type === 'mcp' && node.data?.mcp_server && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                    <h4 className="font-medium text-blue-800 mb-2">🔗 MCP Server Connection</h4>
                    <div className="text-sm text-blue-700">
                      <p><strong>Server:</strong> {node.data.mcp_server}</p>
                      <p><strong>Endpoint:</strong> {node.data.endpoint}</p>
                      <p><strong>Status:</strong> {node.status === 'completed' ? 'Connected' : 'Pending'}</p>
                    </div>
                  </div>
                )}
              </div>
            );
          })()}
        </div>
      )}

      {/* Legend */}
      <div className="flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-green-500"></div>
          <span>Completed</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-blue-500"></div>
          <span>In Progress</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-gray-500"></div>
          <span>Pending</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-red-500"></div>
          <span>Failed</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-4 h-4 rounded-full bg-amber-500"></div>
          <span>Waiting Approval</span>
        </div>
      </div>
    </div>
  );
}
