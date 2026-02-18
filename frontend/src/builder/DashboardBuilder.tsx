"use client";

import ReactECharts from "echarts-for-react";

const sampleOption = {
  xAxis: { type: "category", data: ["Mon", "Tue", "Wed", "Thu", "Fri"] },
  yAxis: { type: "value" },
  series: [{ data: [120, 200, 150, 80, 70], type: "bar", smooth: true }],
};

export function DashboardBuilder() {
  return (
    <section style={{ background: "white", borderRadius: 12, padding: 20, boxShadow: "0 3px 18px #e7ebf5" }}>
      <h2>Dashboard Builder</h2>
      <p>Drag/resize-ready widget containers with chart configuration API support.</p>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <div style={{ border: "1px solid #dde2ef", borderRadius: 8, padding: 8 }}>
          <h4>Revenue Trend (Bar)</h4>
          <ReactECharts option={sampleOption} style={{ height: 280 }} />
        </div>
        <div style={{ border: "1px dashed #b9c2da", borderRadius: 8, padding: 12 }}>
          <h4>Widget Config</h4>
          <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(sampleOption, null, 2)}</pre>
        </div>
      </div>
    </section>
  );
}
