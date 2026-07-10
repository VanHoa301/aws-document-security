import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';

const ALLOWED_EXTENSIONS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'txt'];
const MAX_FILE_SIZE = 20 * 1024 * 1024;

export default function Upload() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  function validateFile(nextFile) {
    if (!nextFile) return 'Please choose a file';
    const extension = nextFile.name.split('.').pop().toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(extension)) return 'This file type is not allowed';
    if (nextFile.size > MAX_FILE_SIZE) return 'File must be 20 MB or smaller';
    return '';
  }

  function handleFileChange(e) {
    const nextFile = e.target.files[0];
    const validationError = validateFile(nextFile);
    setFile(validationError ? null : nextFile);
    setStatus('');
    setError(validationError);
    setProgress(0);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setError('');
    setStatus('');
    setProgress(0);

    try {
      await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: event => {
          if (event.total) setProgress(Math.round((event.loaded * 100) / event.total));
        },
      });
      setStatus('Upload successful. Metadata was saved to DynamoDB.');
      setFile(null);
      e.target.reset();
    } catch (err) {
      setError(err.response?.data?.error || 'Upload failed');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <Navbar />
      <main className="page page-narrow">
        <div className="page-header">
          <div>
            <div className="eyebrow">Private S3 storage</div>
            <h1 className="page-title">Upload Document</h1>
          </div>
        </div>

        {status && (
          <div className="alert alert-success d-flex justify-content-between align-items-center gap-3">
            <span>{status}</span>
            <button className="btn btn-sm btn-success" onClick={() => navigate('/')}>
              View dashboard
            </button>
          </div>
        )}
        {error && <div className="alert alert-danger">{error}</div>}

        <section className="panel">
          <div className="panel-header">
            <div>
              <h2 className="panel-title">Document details</h2>
              <div className="muted-small">Accepted file size is 20 MB or smaller.</div>
            </div>
          </div>

          <div className="p-4">
            <form onSubmit={handleSubmit}>
              <div className="upload-drop mb-4">
                <label className="form-label fw-bold">Choose file</label>
                <input className="form-control form-control-lg" type="file" onChange={handleFileChange} />
                <div className="form-text mt-2">
                  Allowed: PDF, DOC, DOCX, XLS, XLSX, PNG, JPG, JPEG, TXT.
                </div>
                {file && (
                  <div className="mt-3 p-3 bg-white rounded border">
                    <div className="file-name">{file.name}</div>
                    <div className="muted-small">{(file.size / 1024).toFixed(1)} KB ready to upload</div>
                  </div>
                )}
              </div>

              {loading && (
                <div className="progress mb-4" role="progressbar" aria-valuenow={progress} aria-valuemin="0" aria-valuemax="100">
                  <div className="progress-bar" style={{ width: `${progress}%` }}>{progress}%</div>
                </div>
              )}

              <div className="d-flex flex-wrap gap-2">
                <button className="btn btn-primary" type="submit" disabled={loading || !file}>
                  {loading ? 'Uploading...' : 'Upload to S3'}
                </button>
                <button className="btn btn-outline-secondary" type="button" onClick={() => navigate('/')}>
                  Back to dashboard
                </button>
              </div>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
}
