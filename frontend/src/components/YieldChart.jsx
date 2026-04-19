import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell, LabelList
} from 'recharts';

export default function YieldChart({ result }) {
  const yp = result?.forecast?.yield_prediction;
  if (!yp) return null;

  const data = [
    { name: 'Without\nTreatment', value: yp.without_treatment, color: '#E24B4A' },
    { name: 'With\nTreatment',    value: yp.with_treatment,    color: '#1D9E75' },
    { name: 'Seasonal\nAverage',  value: yp.seasonal_average,  color: '#378ADD' },
  ];

  return (
    <div style={{ background: '#fff', borderRadius: 12, border: '0.5px solid #e8eceb', padding: 20 }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 4 }}>
        Yield Forecast
      </div>
      <div style={{ fontSize: 12, color: '#888780', marginBottom: 16 }}>
        Projected output in quintals/acre
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} margin={{ top: 20, right: 10, left: -10, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fill: '#888780' }}
            tickLine={false} axisLine={false}
          />
          <YAxis
            tick={{ fontSize: 11, fill: '#888780' }}
            tickLine={false} axisLine={false}
            domain={[0, 35]}
          />
          <Tooltip
            contentStyle={{ borderRadius: 8, border: '0.5px solid #e8eceb', fontSize: 12 }}
            formatter={(v) => [`${v} quintals/acre`, 'Yield']}
          />
          <Bar dataKey="value" radius={[6, 6, 0, 0]}>
            <LabelList dataKey="value" position="top" style={{ fontSize: 12, fontWeight: 600 }} />
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>

      <div style={{ display: 'flex', gap: 16, justifyContent: 'center', marginTop: 8 }}>
        {data.map((d, i) => (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 11, color: '#888780' }}>
            <div style={{ width: 10, height: 10, borderRadius: 2, background: d.color }} />
            {d.name.replace('\n', ' ')}
          </div>
        ))}
      </div>
    </div>
  );
}