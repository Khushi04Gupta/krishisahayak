import React from 'react';

const cards = [
  { label: 'NDVI Health Index', value: '0.73', unit: '', sub: 'Sentinel-2 · Updated 2h ago', color: '#1D9E75', bar: 73 },
  { label: 'Soil Moisture', value: '34', unit: '%', sub: 'IoT Sensor · Field A', color: '#378ADD', bar: 34 },
  { label: 'Temperature', value: '28', unit: '°C', sub: 'OpenWeather · Vidarbha', color: '#EF9F27', bar: 65 },
  { label: 'Rainfall Forecast', value: '8', unit: 'mm', sub: 'Next 48 hours · Low risk', color: '#534AB7', bar: 20 },
];

export default function MetricCards({ result }) {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
      {cards.map((c, i) => (
        <div key={i} style={{
          background: '#fff', borderRadius: 12,
          border: '0.5px solid #e8eceb',
          padding: '14px 16px',
          borderLeft: `3px solid ${c.color}`
        }}>
          <div style={{ fontSize: 11, color: '#888780', marginBottom: 6 }}>{c.label}</div>
          <div style={{ fontSize: 24, fontWeight: 600, color: '#1a1a1a' }}>
            {c.value}<span style={{ fontSize: 14, fontWeight: 400, color: '#888780' }}>{c.unit}</span>
          </div>
          <div style={{
            height: 4, background: '#f0f0f0',
            borderRadius: 2, margin: '8px 0', overflow: 'hidden'
          }}>
            <div style={{
              height: '100%', width: `${c.bar}%`,
              background: c.color, borderRadius: 2,
              transition: 'width 1s ease'
            }} />
          </div>
          <div style={{ fontSize: 10, color: '#888780' }}>{c.sub}</div>
        </div>
      ))}
    </div>
  );
}