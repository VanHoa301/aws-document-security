import { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import api from '../services/api';

export default function Dashboard() {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDocuments();
  }, []);

  async function fetchDocuments() {
    try {
      const res = await api.get('/documents');
      setDocs(res.data);
    } catch {
      setError('Không thể tải danh sách tài liệu');
    } finally {
      setLoading(false);
    }
  }

  async function handleDownload(doc) {
    try {
      const res = await api.get(`/documents/download/${doc.document_id}`);
      window.open(res.data.download_url, '_blank');
    } catch {
      alert('Không thể tải file');
    }
  }

  async function handleDelete(doc) {
    if (!window.confirm(`Xóa tài liệu "${doc.filename}"?`)) return;
    try {
      await api.delete(`/documents/${doc.document_id}`);
      setDocs(docs.filter(d => d.document_id !== doc.document_id));
    } catch {
      alert('Xóa thất bại');
    }
  }

  function formatSize(bytes) {
    if (!bytes || bytes === 0) return '—';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
  }

  function formatDate(iso) {
    if (!iso) return '—';
    return new Date(iso).toLocaleString('vi-VN');
  }

  function getOriginalName(filename) {
    const parts = filename.split('_');
    return parts.slice(1).join('_') || filename;
  }

  return (
    <>
      <Navbar />
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">Danh sách tài liệu</h5>
          <button className="btn btn-sm btn-outline-secondary" onClick={fetchDocuments}>
            Làm mới
          </button>
        </div>

        {loading && <p className="text-muted">Đang tải...</p>}
        {error && <div className="alert alert-danger">{error}</div>}

        {!loading && docs.length === 0 && (
          <div className="text-center text-muted py-5">
            Chưa có tài liệu nào. <a href="/upload">Upload ngay</a>
          </div>
        )}

        {docs.length > 0 && (
          <div className="table-responsive">
            <table className="table table-hover align-middle">
              <thead className="table-dark">
                <tr>
                  <th>Tên file</th>
                  <th>Người upload</th>
                  <th>Kích thước</th>
                  <th>Thời gian</th>
                  <th>Thao tác</th>
                </tr>
              </thead>
              <tbody>
                {docs.map(doc => (
                  <tr key={doc.document_id}>
                    <td>{getOriginalName(doc.filename)}</td>
                    <td>{doc.uploader}</td>
                    <td>{formatSize(doc.size)}</td>
                    <td>{formatDate(doc.uploaded_at)}</td>
                    <td>
                      <button
                        className="btn btn-sm btn-primary me-2"
                        onClick={() => handleDownload(doc)}
                      >
                        Download
                      </button>
                      <button
                        className="btn btn-sm btn-outline-danger"
                        onClick={() => handleDelete(doc)}
                      >
                        Xóa
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
