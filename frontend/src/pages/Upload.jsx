import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';

export default function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function handleFileChange(e) {
    setFile(e.target.files[0]);
    setStatus('');
    setError('');
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) {
      setError('Vui lòng chọn file');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');
    setStatus('');

    try {
      await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setStatus('Upload thành công!');
      setFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.response?.data?.error || 'Upload thất bại');
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Navbar />
      <div className="container mt-4" style={{ maxWidth: 520 }}>
        <h5 className="mb-4">Upload tài liệu</h5>

        {status && (
          <div className="alert alert-success d-flex justify-content-between align-items-center">
            {status}
            <button className="btn btn-sm btn-success" onClick={() => navigate('/')}>
              Xem danh sách
            </button>
          </div>
        )}
        {error && <div className="alert alert-danger">{error}</div>}

        <div className="card p-4">
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Chọn file</label>
              <input
                className="form-control"
                type="file"
                onChange={handleFileChange}
              />
              {file && (
                <div className="form-text">
                  {file.name} — {(file.size / 1024).toFixed(1)} KB
                </div>
              )}
            </div>
            <div className="d-flex gap-2">
              <button className="btn btn-primary" type="submit" disabled={loading}>
                {loading ? 'Đang upload...' : 'Upload'}
              </button>
              <button
                className="btn btn-outline-secondary"
                type="button"
                onClick={() => navigate('/')}
              >
                Quay lại
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}
