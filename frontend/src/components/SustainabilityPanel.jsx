import React from 'react';

export default function SustainabilityPanel({ result }) {
  const s = result?.sustainability;
  if (!s) return null;

  const cards = [
    {
      icon: '💧', label: 'Water Saved',
      value: `${s.water_saved_litres?.toLocaleString() ?? 2400}L`,
      sub: 'vs traditional irrigation method',
      bg: '#E6F1FB', color: '#0C447C'
    },
    {
      icon: '🌿', label: 'Carbon Footprint',
      value: s.carbon_impact ?? 'Low',
      sub: 'Targeted treatment reduces chemical use by 40%',
      bg: '#EAF3DE', color: '#27500A'
    },
    {
      icon: '₹', label: 'Yield Protection Value',
      value: `₹${s.economic_protection_inr?.toLocaleString() ?? '42,000'}`,
      sub: 'Estimated savings based on current wheat MSP',
      bg: '#FAEEDA', color: '#633806'
    },
  ];

  return (
    <div style={{ background: '#fff', borderRadius: 12, border: '0.5px solid #e8eceb', padding: 20 }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 14 }}>
        Sustainability Impact
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 14 }}>
        {cards.map((c, i) => (
          <div key={i} style={{
            background: c.bg, borderRadius: 10,
            padding: '16px 18px', textAlign: 'center'
          }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>{c.icon}</div>
            <div style={{ fontSize: 11, color: '#888780', marginBottom: 4 }}>{c.label}</div>
            <div style={{ fontSize: 22, fontWeight: 600, color: c.color, marginBottom: 4 }}>{c.value}</div>
            <div style={{ fontSize: 11, color: '#888780', lineHeight: 1.4 }}>{c.sub}</div>
          </div>
        ))}
      </div>
    </div>
  );
}