import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import api from '../services/api';

const STATUSES = ['OPEN', 'INVESTIGATING', 'RESOLVED'];

export default function Incidents() {
  const [incidents, setIncidents] = useState([]);
  const [filters, setFilters] = useState({ severity: '', status: '', type: '' });
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [actionLoading, setActionLoading] = useState('');
  const [searchParams] = useSearchParams();
  const role = localStorage.getItem('role');

  useEffect(() => {
    fetchIncidents();
    const timer = window.setInterval(fetchIncidents, 30000);
    return () => window.clearInterval(timer);
  }, []);

  const summary = useMemo(() => ({
    total: incidents.length,
    open: incidents.filter(item => String(item.status).toUpperCase() === 'OPEN').length,
    high: incidents.filter(item => ['HIGH', 'CRITICAL'].includes(String(item.severity).toUpperCase())).length,
  }), [incidents]);

  async function fetchIncidents(nextFilters = filters) {
    setError('');
    try {
      const params = new URLSearchParams();
      Object.entries(nextFilters).forEach(([key, value]) => {
        if (value) params.set(key, value);
      });
      const res = await api.get(`/incidents?${params.toString()}`);
      setIncidents(res.data);
      const requestedIncident = searchParams.get('incident');
      if (requestedIncident) {
        const match = res.data.find(item => item.incident_id === requestedIncident);
        if (match) {
          setSelected(match);
        } else {
          const detail = await api.get(`/incidents/${encodeURIComponent(requestedIncident)}`);
          setSelected(detail.data);
        }
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Cannot load incidents');
    } finally {
      setLoading(false);
    }
  }

  function handleFilterChange(e) {
    const nextFilters = { ...filters, [e.target.name]: e.target.value };
    setFilters(nextFilters);
    fetchIncidents(nextFilters);
  }

  async function updateStatus(incident, status) {
    try {
      const res = await api.patch(`/incidents/${incident.incident_id}/status`, { status });
      setIncidents(incidents.map(item => item.incident_id === incident.incident_id ? res.data : item));
      setSelected(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Cannot update incident status');
    }
  }

  async function runResponseAction(action) {
    if (!selected) return;
    const labels = { quarantine: 'cách ly', restore: 'khôi phục', stop: 'DỪNG' };
    const label = labels[action] || action;
    if (!window.confirm(`Xác nhận ${label} EC2 ${selected.instance_id || selected.resource_id}?`)) return;

    setActionLoading(action);
    setError('');
    try {
      const res = await api.post(`/incidents/${selected.incident_id}/${action}`);
      const updated = res.data.incident;
      setIncidents(current => current.map(item => item.incident_id === updated.incident_id ? updated : item));
      setSelected(updated);
    } catch (err) {
      setError(err.response?.data?.detail || err.response?.data?.error || `Cannot ${action} instance`);
    } finally {
      setActionLoading('');
    }
  }

  function severityBadge(severity) {
    const normalized = String(severity || 'UNKNOWN').toUpperCase();
    const className = `severity-badge severity-${normalized.toLowerCase()}`;
    return <span className={className}>{normalized}</span>;
  }

  function statusBadge(status) {
    const normalized = String(status || 'OPEN').toUpperCase();
    return <span className={`status-label ${normalized.toLowerCase()}`}>{normalized}</span>;
  }

  function formatDate(value) {
    if (!value) return '-';
    return new Date(value).toLocaleString('vi-VN');
  }

  return (
    <div className="app-shell">
      <Navbar />
      <main className="page">
        <div className="page-header">
          <div>
            <div className="eyebrow">Automated security response</div>
            <h1 className="page-title">Security Incidents</h1>
          </div>
          <button className="btn btn-primary" onClick={() => fetchIncidents()} disabled={loading}>
            {loading ? 'Refreshing...' : 'Refresh incidents'}
          </button>
        </div>

        <div className="row g-3 mb-4">
          <div className="col-md-4">
            <div className="metric-card metric-blue">
              <div className="metric-label">Total incidents</div>
              <div className="metric-value">{summary.total}</div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="metric-card metric-amber">
              <div className="metric-label">Open</div>
              <div className="metric-value">{summary.open}</div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="metric-card metric-red">
              <div className="metric-label">High/Critical</div>
              <div className="metric-value">{summary.high}</div>
            </div>
          </div>
        </div>

        {error && <div className="alert alert-warning">{error}</div>}

        <div className="row g-3">
          <div className="col-lg-8">
            <section className="panel">
              <div className="panel-header">
                <div>
                  <h2 className="panel-title">Incident stream</h2>
                  <div className="muted-small">Auto-refreshes every 30 seconds while this page is open.</div>
                </div>
              </div>
              <div className="filter-bar">
                <select className="form-select form-select-sm" style={{ maxWidth: 180 }} name="severity" value={filters.severity} onChange={handleFilterChange}>
                  <option value="">All severity</option>
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
                <select className="form-select form-select-sm" style={{ maxWidth: 180 }} name="status" value={filters.status} onChange={handleFilterChange}>
                  <option value="">All status</option>
                  {STATUSES.map(status => <option key={status} value={status}>{status}</option>)}
                </select>
                <input
                  className="form-control form-control-sm"
                  style={{ maxWidth: 270 }}
                  name="type"
                  value={filters.type}
                  onChange={handleFilterChange}
                  placeholder="Filter finding type"
                />
              </div>

              {loading && <div className="p-4 text-muted">Loading incidents...</div>}

              <div className="table-responsive">
                <table className="table table-hover align-middle">
                  <thead>
                    <tr>
                      <th>Type</th>
                      <th>Severity</th>
                      <th>Status</th>
                      <th>Resource</th>
                      <th>Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {incidents.map(incident => (
                      <tr
                        key={incident.incident_id}
                        className={selected?.incident_id === incident.incident_id ? 'selected-row' : ''}
                        onClick={() => setSelected(incident)}
                        style={{ cursor: 'pointer' }}
                      >
                        <td>
                          <div className="file-name">{incident.finding_type || incident.type || 'Unknown'}</div>
                          <div className="muted-small">{incident.incident_id}</div>
                        </td>
                        <td>{severityBadge(incident.severity)}</td>
                        <td>{statusBadge(incident.status)}</td>
                        <td>{incident.resource_id || incident.instance_id || incident.account_id || '-'}</td>
                        <td>{formatDate(incident.timestamp || incident.time)}</td>
                      </tr>
                    ))}
                    {!loading && incidents.length === 0 && (
                      <tr>
                        <td colSpan="5">
                          <div className="empty-state compact">
                            <div className="empty-icon">SEC</div>
                            <h3>No incidents found</h3>
                            <p>Security findings will appear here after Lambda writes to DynamoDB.</p>
                          </div>
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </section>
          </div>

          <div className="col-lg-4">
            <section className="panel detail-panel">
              <div className="panel-header">
                <h2 className="panel-title">Incident detail</h2>
              </div>
              <div className="p-4">
                {!selected && <p className="text-muted mb-0">Select an incident to inspect its AWS context.</p>}
                {selected && (
                  <>
                    <dl className="row small mb-4">
                      <dt className="col-4">ID</dt><dd className="col-8 text-break">{selected.incident_id}</dd>
                      <dt className="col-4">Type</dt><dd className="col-8">{selected.finding_type || selected.type || '-'}</dd>
                      <dt className="col-4">Severity</dt><dd className="col-8">{severityBadge(selected.severity)}</dd>
                      <dt className="col-4">Status</dt><dd className="col-8">{statusBadge(selected.status)}</dd>
                      <dt className="col-4">Region</dt><dd className="col-8">{selected.region || '-'}</dd>
                      <dt className="col-4">Resource</dt><dd className="col-8 text-break">{selected.resource_id || selected.instance_id || '-'}</dd>
                    </dl>
                    {role === 'admin' && (
                      <div>
                        <div className="muted-small mb-2">Approved response actions</div>
                        <div className="d-grid gap-2 mb-4">
                          <button
                            className="btn btn-danger"
                            disabled={Boolean(actionLoading) || !String(selected.resource_id || selected.instance_id || '').startsWith('i-')}
                            onClick={() => runResponseAction('quarantine')}
                          >
                            {actionLoading === 'quarantine' ? 'Quarantining...' : 'Approve quarantine'}
                          </button>
                          <button
                            className="btn btn-outline-success"
                            disabled={Boolean(actionLoading) || !selected.original_security_groups}
                            onClick={() => runResponseAction('restore')}
                          >
                            {actionLoading === 'restore' ? 'Restoring...' : 'Restore security groups'}
                          </button>
                          <button
                            className="btn btn-outline-danger"
                            disabled={Boolean(actionLoading) || !String(selected.resource_id || selected.instance_id || '').startsWith('i-')}
                            onClick={() => runResponseAction('stop')}
                          >
                            {actionLoading === 'stop' ? 'Stopping...' : 'Stop EC2 (emergency)'}
                          </button>
                        </div>
                        <div className="muted-small mb-2">Update response status</div>
                        <div className="d-flex flex-wrap gap-2">
                          {STATUSES.map(status => (
                            <button key={status} className="btn btn-sm btn-outline-primary" onClick={() => updateStatus(selected, status)}>
                              {status}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
