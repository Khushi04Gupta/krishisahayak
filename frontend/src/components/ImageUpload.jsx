import React, { useState, useRef } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

export default function ImageUpload({ onResult, onError, loading, setLoading }) {
  const [preview, setPreview] = useState(null);
  const [fileName, setFileName] = useState(null);
  const inputRef = useRef();

  const handleFile = async (file) => {
    if (!file) return;
    setFileName(file.name);
    setPreview(URL.createObjectURL(file));
    setLoading(true);

    const form = new FormData();
    form.append('file', file);

    try {
      const res = await axios.post(`${API}/predict-disease`, form, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      onResult(res.data);
    } catch (e) {
      onError('Could not connect to KrishiSahayak backend. Make sure it is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div style={{
      background: '#fff', borderRadius: 12,
      border: '0.5px solid #e8eceb', padding: 20
    }}>
      <div style={{ fontSize: 11, fontWeight: 500, color: '#888780', textTransform: 'uppercase', letterSpacing: '.07em', marginBottom: 12 }}>
        Crop Image Analysis
      </div>

      {/* DROP ZONE */}
      <div
        onClick={() => inputRef.current.click()}
        onDrop={handleDrop}
        onDragOver={e => e.preventDefault()}
        style={{
          border: '2px dashed #97C459', borderRadius: 10,
          background: '#F8FDF5', cursor: 'pointer',
          display: 'flex', flexDirection: 'column',
          alignItems: 'center', justifyContent: 'center',
          height: preview ? 'auto' : 160,
          overflow: 'hidden', marginBottom: 12,
          transition: 'border-color .2s'
        }}
      >
        {preview ? (
          <img src={preview} alt="crop"
            style={{ width: '100%', borderRadius: 8, display: 'block' }} />
        ) : (
          <>
            <div style={{ fontSize: 32, marginBottom: 8 }}>📷</div>
            <div style={{ fontSize: 13, fontWeight: 500, color: '#27500A' }}>
              Click or drag to upload
            </div>
            <div style={{ fontSize: 11, color: '#888780', marginTop: 4 }}>
              JPG, PNG, WEBP supported
            </div>
          </>
        )}
      </div>

      <input
        ref={inputRef} type="file"
        accept="image/*" style={{ display: 'none' }}
        onChange={e => handleFile(e.target.files[0])}
      />

      {/* ANALYZE BUTTON */}
      <button
        onClick={() => inputRef.current.click()}
        disabled={loading}
        style={{
          width: '100%', padding: '10px 0',
          background: loading ? '#97C459' : '#1D9E75',
          color: '#fff', border: 'none', borderRadius: 8,
          fontSize: 13, fontWeight: 500, cursor: loading ? 'not-allowed' : 'pointer',
          transition: 'background .2s'
        }}
      >
        {loading ? '🔍 Analysing crop...' : '+ Upload & Analyse'}
      </button>

      {fileName && (
        <div style={{ fontSize: 11, color: '#888780', marginTop: 8, textAlign: 'center' }}>
          {fileName}
        </div>
      )}

      {/* FEDERATED BADGE */}
      <div style={{
        marginTop: 12, background: '#EAF3DE',
        border: '0.5px solid #97C459', borderRadius: 8,
        padding: '8px 12px', fontSize: 11, color: '#27500A',
        display: 'flex', alignItems: 'center', gap: 6
      }}>
        🔒 Federated AI — your image is processed locally. No raw data leaves your device.
      </div>
    </div>
  );
}