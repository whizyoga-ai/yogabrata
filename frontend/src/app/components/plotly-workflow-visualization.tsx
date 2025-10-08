"use client";

import React from 'react';

interface PlotlyWorkflowVisualizationProps {
  workflowId: string;
  onNodeClick?: (nodeId: string) => void;
  onApprovalRequired?: (nodeId: string) => void;
}

export default function PlotlyWorkflowVisualization({
  workflowId,
  onNodeClick,
  onApprovalRequired
}: PlotlyWorkflowVisualizationProps) {
  return (
    <div className="w-full bg-white p-6 rounded-lg border">
      <h3 className="text-lg font-semibold mb-4">Interactive Workflow Visualization</h3>

      {/* Simple interactive workflow visualization */}
      <div className="space-y-4">
        {/* Workflow Steps */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div
            className="p-4 bg-blue-50 border-2 border-blue-200 rounded-lg cursor-pointer hover:bg-blue-100 transition-colors"
            onClick={() => onNodeClick?.('name-check')}
          >
            <div className="text-center">
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-white text-sm font-bold">1</span>
              </div>
              <p className="text-sm font-medium">Name Check</p>
              <p className="text-xs text-gray-600">Available</p>
            </div>
          </div>

          <div
            className="p-4 bg-green-50 border-2 border-green-200 rounded-lg cursor-pointer hover:bg-green-100 transition-colors"
            onClick={() => onNodeClick?.('document-gen')}
          >
            <div className="text-center">
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-white text-sm font-bold">2</span>
              </div>
              <p className="text-sm font-medium">Documents</p>
              <p className="text-xs text-gray-600">Generated</p>
            </div>
          </div>

          <div
            className="p-4 bg-yellow-50 border-2 border-yellow-200 rounded-lg cursor-pointer hover:bg-yellow-100 transition-colors"
            onClick={() => onApprovalRequired?.('state-filing')}
          >
            <div className="text-center">
              <div className="w-8 h-8 bg-yellow-500 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-white text-sm font-bold">3</span>
              </div>
              <p className="text-sm font-medium">State Filing</p>
              <p className="text-xs text-gray-600">Pending Approval</p>
            </div>
          </div>

          <div
            className="p-4 bg-purple-50 border-2 border-purple-200 rounded-lg cursor-pointer hover:bg-purple-100 transition-colors"
            onClick={() => onNodeClick?.('tax-reg')}
          >
            <div className="text-center">
              <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-2">
                <span className="text-white text-sm font-bold">4</span>
              </div>
              <p className="text-sm font-medium">Tax Registration</p>
              <p className="text-xs text-gray-600">Pending</p>
            </div>
          </div>
        </div>

        {/* Workflow Progress Bar */}
        <div className="mt-6">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Progress</span>
            <span>50%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full" style={{width: '50%'}}></div>
          </div>
        </div>

        {/* Workflow Info */}
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h4 className="font-medium mb-2">Workflow Details</h4>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Workflow ID:</span>
              <p className="font-mono">{workflowId}</p>
            </div>
            <div>
              <span className="text-gray-600">Status:</span>
              <p className="text-blue-600">In Progress</p>
            </div>
            <div>
              <span className="text-gray-600">Current Step:</span>
              <p>Document Generation</p>
            </div>
            <div>
              <span className="text-gray-600">Est. Completion:</span>
              <p>2-3 business days</p>
            </div>
          </div>
        </div>

        {/* Click Instructions */}
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <p className="text-sm text-blue-800">
            💡 <strong>Click on any step</strong> to view details or trigger actions.
            Steps requiring approval will be highlighted in yellow.
          </p>
        </div>
      </div>
    </div>
  );
}
