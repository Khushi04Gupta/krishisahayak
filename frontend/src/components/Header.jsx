import React, { useState, useEffect } from 'react';

export default function Header() {
  const [time, setTime] = useState(new Date());

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  return (
    <div style={{
      background: '#1a1a2e', padding: '0 24px',
      height: 56, display: 'flex', alignItems: 'center',
      justifyContent: 'space-between', position: 'sticky', top: 0, zIndex: 100
    }}>
      {/* LEFT */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <div style={{
          width: 32, height: 32, borderRadius: 8,
          background: '#1D9E75', display: 'flex',
          alignItems: 'center', justifyContent: 'center',
          fontSize: 16
        }}>🌾</div>
        <div>
          <span style={{ color: '#fff', fontWeight: 600, fontSize: 15 }}>KrishiSahayak</span>
          <span style={{ color: '#1D9E75', fontSize: 12, marginLeft: 6 }}>Dashboard</span>
        </div>
      </div>

      {/* CENTER */}
      <div style={{ color: '#8696a0', fontSize: 12 }}>
        Farm ID: VID-2847 · Ramesh Kumar · Vidarbha, Maharashtra
      </div>

      {/* RIGHT */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <span style={{ color: '#8696a0', fontSize: 12 }}>
          {time.toLocaleTimeString()}
        </span>
        <span style={{
          background: '#1D9E7520', color: '#1D9E75',
          border: '1px solid #1D9E75', borderRadius: 999,
          fontSize: 11, fontWeight: 500, padding: '3px 10px',
          display: 'flex', alignItems: 'center', gap: 5
        }}>
          <span style={{
            width: 6, height: 6, borderRadius: '50%',
            background: '#1D9E75', display: 'inline-block'
          }}></span>
          System Online
        </span>
        <span style={{
          background: '#FAEEDA', color: '#633806',
          borderRadius: 999, fontSize: 11,
          fontWeight: 500, padding: '3px 10px'
        }}>
          Offline Ready
        </span>
      </div>
    </div>
  );
}