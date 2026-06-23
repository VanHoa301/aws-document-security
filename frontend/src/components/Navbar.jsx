import { Link, useNavigate } from 'react-router-dom';

export default function Navbar() {
  const navigate = useNavigate();
  const username = localStorage.getItem('username');

  function handleLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  }

  return (
    <nav className="navbar navbar-dark bg-dark px-4">
      <Link className="navbar-brand fw-bold" to="/">
        DA_AWS Documents
      </Link>
      <div className="d-flex align-items-center gap-3">
        <Link className="btn btn-outline-light btn-sm" to="/upload">
          Upload
        </Link>
        <span className="text-white-50 small">{username}</span>
        <button className="btn btn-danger btn-sm" onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}
