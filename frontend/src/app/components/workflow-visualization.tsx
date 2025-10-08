"use client";

import React, { useEffect, useRef } from 'react';

interface WorkflowVisualizationProps {
  mermaidDiagram: string;
  workflowId: string;
}

export default function WorkflowVisualization({ mermaidDiagram, workflowId }: WorkflowVisualizationProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Simple fallback visualization when Mermaid is not available in static export
    if (containerRef.current && mermaidDiagram) {
      containerRef.current.innerHTML = `
        <div class="bg-white p-6 rounded-lg border">
          <h3 class="text-lg font-semibold mb-4">Workflow Visualization</h3>
          <div class="space-y-3">
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                <span class="text-blue-600 text-sm font-bold">1</span>
              </div>
              <div>
                <p class="font-medium">Business Name Check</p>
                <p class="text-sm text-gray-600">Verify name availability</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                <span class="text-green-600 text-sm font-bold">2</span>
              </div>
              <div>
                <p class="font-medium">Document Generation</p>
                <p class="text-sm text-gray-600">Create formation documents</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                <span class="text-yellow-600 text-sm font-bold">3</span>
              </div>
              <div>
                <p class="font-medium">State Filing</p>
                <p class="text-sm text-gray-600">Submit to WA SOS</p>
              </div>
            </div>
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                <span class="text-purple-600 text-sm font-bold">4</span>
              </div>
              <div>
                <p class="font-medium">Tax Registration</p>
                <p class="text-sm text-gray-600">Register with WA DOR</p>
              </div>
            </div>
          </div>
          <div class="mt-4 p-3 bg-gray-50 rounded">
            <p class="text-sm text-gray-600">
              <strong>Workflow ID:</strong> ${workflowId}
            </p>
          </div>
        </div>
      `;
    }
  }, [mermaidDiagram, workflowId]);

  return (
    <div className="w-full">
      <div ref={containerRef} className="min-h-[400px]" />
    </div>
  );
}
