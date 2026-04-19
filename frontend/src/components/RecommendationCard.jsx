import React from 'react';

export default function RecommendationCard({ result }) {
  const rec = result?.recommendation;
  const fore = result?.forecast;
  if (!rec) return null;

  return (
    <div style={{ background: '#fff', borderRadius: 12, border: '0.5px solid #e8eceb', padding: 20 }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 14 }}>
        AI Recommendation
      </div>

      {/* MAIN ADVICE */}
      <div style={{
        borderLeft: '3px solid #1D9E75', paddingLeft: 12, marginBottom: 16
      }}>
        <div style={{ fontSize: 15, fontWeight: 600, color: '#1a1a1a', marginBottom: 4 }}>
          {rec.text}
        </div>
        <div style={{ fontSize: 12, color: '#888780', fontStyle: 'italic' }}>
          {rec.hindi}
        </div>
      </div>

      {/* STEPS */}
      <div style={{ marginBottom: 16 }}>
        <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', marginBottom: 8 }}>Action steps</div>
        {rec.steps?.map((s, i) => (
          <div key={i} style={{ display: 'flex', gap: 10, marginBottom: 8, alignItems: 'flex-start' }}>
            <div style={{
              width: 22, height: 22, borderRadius: '50%',
              background: '#1D9E75', color: '#fff',
              fontSize: 11, fontWeight: 600,
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0, marginTop: 1
            }}>{i + 1}</div>
            <div style={{ fontSize: 13, color: '#1a1a1a', lineHeight: 1.5 }}>{s}</div>
          </div>
        ))}
      </div>

      {/* REASONING */}
      <div style={{
        background: '#E6F1FB', border: '0.5px solid #85B7EB',
        borderRadius: 8, padding: '10px 12px', marginBottom: 16
      }}>
        <div style={{ fontSize: 11, fontWeight: 500, color: '#0C447C', marginBottom: 4 }}>
          Why AI decided this
        </div>
        <div style={{ fontSize: 12, color: '#185FA5', lineHeight: 1.5 }}>
          {rec.reasoning}
        </div>
      </div>

      {/* YIELD IMPACT */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
        <div style={{
          background: '#FCEBEB', borderRadius: 8,
          padding: '10px 12px', textAlign: 'center'
        }}>
          <div style={{ fontSize: 11, color: '#888780', marginBottom: 4 }}>Without treatment</div>
          <div style={{ fontSize: 18, fontWeight: 600, color: '#E24B4A' }}>
            {fore?.yield_prediction?.without_treatment ?? '—'}
          </div>
          <div style={{ fontSize: 10, color: '#A32D2D' }}>quintals/acre</div>
        </div>
        <div style={{
          background: '#EAF3DE', borderRadius: 8,
          padding: '10px 12px', textAlign: 'center'
        }}>
          <div style={{ fontSize: 11, color: '#888780', marginBottom: 4 }}>With treatment</div>
          <div style={{ fontSize: 18, fontWeight: 600, color: '#1D9E75' }}>
            {fore?.yield_prediction?.with_treatment ?? '—'}
          </div>
          <div style={{ fontSize: 10, color: '#27500A' }}>quintals/acre</div>
        </div>
      </div>

      {/* FEDERATED NOTE */}
      <div style={{
        marginTop: 14, background: '#1D9E75',
        borderRadius: 8, padding: '8px 12px',
        fontSize: 11, color: '#fff',
        display: 'flex', alignItems: 'center', gap: 6
      }}>
        🔒 {result?.federated_note}
      </div>
    </div>
  );
}