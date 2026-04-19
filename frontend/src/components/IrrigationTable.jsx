import React from 'react';

const actionColors = {
  'Irrigate': { bg: '#EAF3DE', color: '#27500A' },
  'Refill':   { bg: '#EAF3DE', color: '#27500A' },
  'Skip':     { bg: '#f5f5f5', color: '#888780' },
  'Rest':     { bg: '#f5f5f5', color: '#888780' },
  'Monitor':  { bg: '#FAEEDA', color: '#633806' },
  'Drip only':{ bg: '#E6F1FB', color: '#0C447C' },
  'Reduce':   { bg: '#FAEEDA', color: '#633806' },
  'Drain partial': { bg: '#EEEDFE', color: '#3C3489' },
};

export default function IrrigationTable({ result }) {
  const schedule = result?.forecast?.irrigation_schedule;
  if (!schedule) return null;

  return (
    <div style={{ background: '#fff', borderRadius: 12, border: '0.5px solid #e8eceb', padding: 20 }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 4 }}>
        7-Day Irrigation Schedule
      </div>
      <div style={{ fontSize: 12, color: '#888780', marginBottom: 14 }}>
        {result?.forecast?.irrigation_advice}
      </div>

      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
        <thead>
          <tr>
            {['Day', 'Date', 'Action', 'Reason', 'Water'].map(h => (
              <th key={h} style={{
                textAlign: 'left', padding: '6px 8px',
                fontSize: 11, color: '#888780', fontWeight: 500,
                borderBottom: '1px solid #f0f0f0'
              }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {schedule.map((row, i) => {
            const style = actionColors[row.action] || { bg: '#f5f5f5', color: '#888780' };
            return (
              <tr key={i} style={{ background: i % 2 === 0 ? '#fafafa' : '#fff' }}>
                <td style={{ padding: '7px 8px', color: '#888780', fontSize: 12 }}>Day {row.day}</td>
                <td style={{ padding: '7px 8px', fontWeight: 500 }}>{row.date}</td>
                <td style={{ padding: '7px 8px' }}>
                  <span style={{
                    background: style.bg, color: style.color,
                    fontSize: 11, fontWeight: 500,
                    padding: '2px 8px', borderRadius: 999
                  }}>
                    {row.action}
                  </span>
                </td>
                <td style={{ padding: '7px 8px', fontSize: 12, color: '#5F5E5A' }}>{row.reason}</td>
                <td style={{ padding: '7px 8px', fontWeight: 500, color: row.amount_mm > 0 ? '#1D9E75' : '#888780' }}>
                  {row.amount_mm > 0 ? `${row.amount_mm}mm` : '—'}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}