"use client";

import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

interface WorkflowVisualizationProps {
  mermaidDiagram: string;
  workflowId?: string;
}

export default function WorkflowVisualization({ mermaidDiagram, workflowId }: WorkflowVisualizationProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (mermaidDiagram && containerRef.current) {
      // Initialize mermaid
      mermaid.initialize({
        startOnLoad: false,
        theme: 'default',
        securityLevel: 'loose',
        fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Consolas, "Liberation Mono", Menlo, monospace',
      });

      // Clear previous content
      containerRef.current.innerHTML = '';

      // Render the diagram
      mermaid.render(`workflow-diagram-${workflowId || 'default'}`, mermaidDiagram)
        .then((result) => {
          if (containerRef.current) {
            containerRef.current.innerHTML = result.svg;
          }
        })
        .catch((error) => {
          console.error('Mermaid rendering error:', error);
          if (containerRef.current) {
            containerRef.current.innerHTML = `
              <div class="p-4 border border-red-200 rounded-lg bg-red-50">
                <p class="text-red-800">Error rendering workflow diagram</p>
                <pre class="text-xs text-red-600 mt-2">${error.message}</pre>
              </div>
            `;
          }
        });
    }
  }, [mermaidDiagram, workflowId]);

  if (!mermaidDiagram) {
    return (
      <div className="p-8 text-center text-gray-500">
        <p>No workflow diagram available</p>
      </div>
    );
  }

  return (
    <div className="workflow-visualization">
      <div className="mb-4 flex justify-between items-center">
        <h3 className="text-lg font-semibold">Workflow Visualization</h3>
        <div className="flex gap-2">
          <button
            onClick={() => window.print()}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Export as Image
          </button>
        </div>
      </div>

      <div
        ref={containerRef}
        className="border border-gray-200 rounded-lg p-4 bg-white overflow-auto"
        style={{ minHeight: '400px' }}
      />

      <div className="mt-4 text-sm text-gray-600">
        <p>
          <strong>Legend:</strong>
          <span className="ml-4">
            <span className="inline-block w-3 h-3 bg-gray-100 border border-gray-400 mr-1"></span>
            Pending
          </span>
          <span className="ml-2">
            <span className="inline-block w-3 h-3 bg-blue-100 border border-blue-400 mr-1"></span>
            In Progress
          </span>
          <span className="ml-2">
            <span className="inline-block w-3 h-3 bg-green-100 border border-green-400 mr-1"></span>
            Completed
          </span>
          <span className="ml-2">
            <span className="inline-block w-3 h-3 bg-red-100 border border-red-400 mr-1"></span>
            Failed
          </span>
        </p>
      </div>
    </div>
  );
}
