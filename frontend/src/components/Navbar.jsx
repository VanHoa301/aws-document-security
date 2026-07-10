import { NavLink, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');
  const role = localStorage.getItem('role');
  const displayUser = username && role && username !== role ? `${username} · ${role}` : (username || role || 'Guest');

  function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    navigate('/login');
  }

  return (
    <header className="topbar">
      <div className="container-fluid px-4 topbar-inner">
        <NavLink className="brand-lockup" to="/">
          <span className="brand-mark">AWS</span>
          <span>
            <span className="brand-title">DA_AWS Documents</span>
          </span>
        </NavLink>

        <nav className="nav-actions" aria-label="Main navigation">
          <NavLink className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`} to="/" end>
            Documents
          </NavLink>
          <NavLink className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`} to="/upload">
            Upload
          </NavLink>
          <NavLink className={({ isActive }) => `nav-pill ${isActive ? 'active' : ''}`} to="/incidents">
            Incidents
          </NavLink>
          <span className="user-chip">{displayUser}</span>
          <button className="btn btn-sm btn-outline-danger" onClick={handleLogout}>
            Logout
          </button>
        </nav>
      </div>
    </header>
  );
}
