import React from 'react';

export default function DiseaseResult({ result }) {
  const pred = result?.prediction;
  if (!pred) return null;

  const confPct = Math.round(pred.confidence * 100);
  const confColor = confPct >= 85 ? '#E24B4A' : confPct >= 70 ? '#EF9F27' : '#1D9E75';

  return (
    <div style={{ background: '#fff', borderRadius: 12, border: '0.5px solid #e8eceb', padding: 20 }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 14 }}>
        AI Detection Result
      </div>

      {/* PRIMARY RESULT */}
      <div style={{
        background: '#F8FDF5', border: '0.5px solid #97C459',
        borderRadius: 10, padding: '14px 16px', marginBottom: 14
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
          <div>
            <div style={{ fontSize: 18, fontWeight: 600, color: '#1a1a1a' }}>{pred.disease}</div>
            <div style={{ fontSize: 11, color: '#888780', marginTop: 2 }}>
              {pred.model} · {pred.inference_time_ms}ms
            </div>
          </div>
          <span style={{
            background: pred.severity === 'high' ? '#FCEBEB' : '#FAEEDA',
            color: pred.severity === 'high' ? '#A32D2D' : '#633806',
            fontSize: 11, fontWeight: 500, padding: '3px 10px', borderRadius: 999
          }}>
            {pred.severity === 'high' ? 'High' : 'Moderate'} severity
          </span>
        </div>

        {/* CONFIDENCE BAR */}
        <div style={{ fontSize: 12, color: '#5F5E5A', marginBottom: 4 }}>
          Confidence: <strong style={{ color: confColor }}>{confPct}%</strong>
        </div>
        <div style={{ height: 8, background: '#e8eceb', borderRadius: 4, overflow: 'hidden' }}>
          <div style={{
            height: '100%', width: `${confPct}%`,
            background: confColor, borderRadius: 4,
            transition: 'width 1s ease'
          }} />
        </div>
      </div>

      {/* TOP PREDICTIONS */}
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', marginBottom: 8 }}>
        All predictions
      </div>
      {pred.top_predictions?.map((p, i) => (
        <div key={i} style={{
          display: 'flex', alignItems: 'center',
          gap: 10, marginBottom: 6
        }}>
          <div style={{ fontSize: 12, color: '#1a1a1a', width: 180, flexShrink: 0 }}>{p.disease}</div>
          <div style={{ flex: 1, height: 5, background: '#f0f0f0', borderRadius: 3, overflow: 'hidden' }}>
            <div style={{
              height: '100%',
              width: `${Math.round(p.confidence * 100)}%`,
              background: i === 0 ? confColor : '#B4B2A9',
              borderRadius: 3
            }} />
          </div>
          <div style={{ fontSize: 11, color: '#888780', width: 36, textAlign: 'right' }}>
            {Math.round(p.confidence * 100)}%
          </div>
        </div>
      ))}

      {/* HEATMAP PLACEHOLDER */}
      <div style={{ marginTop: 14 }}>
        <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', marginBottom: 6 }}>
          Grad-CAM Explainability Heatmap
        </div>
        <div style={{
          height: 100, borderRadius: 8, overflow: 'hidden', position: 'relative',
          background: 'linear-gradient(135deg, #2d5a27 0%, #4a7c3f 30%, #e8a020 60%, #e03020 100%)'
        }}>
          <div style={{
            position: 'absolute', bottom: 6, left: 8,
            background: 'rgba(0,0,0,0.6)', color: '#fff',
            fontSize: 10, padding: '2px 8px', borderRadius: 4
          }}>
            AI Focus Region
          </div>
          <div style={{
            position: 'absolute', top: 6, right: 8,
            background: 'rgba(0,0,0,0.6)', color: '#fff',
            fontSize: 10, padding: '2px 8px', borderRadius: 4
          }}>
            {confPct}% confidence
          </div>
        </div>
        <div style={{ fontSize: 10, color: '#888780', marginTop: 4 }}>
          Red zones indicate disease-affected regions detected by EfficientNet-Lite
        </div>
      </div>
    </div>
  );
}