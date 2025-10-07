declare module 'react-plotly.js' {
  import { Component } from 'react';
  import { PlotlyHTMLElement } from 'plotly.js';

  export interface PlotParams {
    data: any[];
    layout?: any;
    frames?: any[];
    config?: any;
    revision?: number;
    debug?: boolean;
  }

  export default class Plot extends Component<PlotParams> {
    static relayout: (gd: PlotlyHTMLElement, update: any) => Promise<any>;
    static restyle: (gd: PlotlyHTMLElement, update: any, traces?: number | number[]) => Promise<any>;
    static addTraces: (gd: PlotlyHTMLElement, traces: any | any[], newIndices?: number | number[]) => Promise<any>;
    static deleteTraces: (gd: PlotlyHTMLElement, indices: number | number[]) => Promise<any>;
  }
}
