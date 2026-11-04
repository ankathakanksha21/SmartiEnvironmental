import { useEffect } from 'react'
import { Link, NavLink, Outlet, useLocation, useNavigate } from 'react-router'

const MESSAGE_SECONDS = 5

// The header shown on every page. The current page appears in <Outlet />.
export default function Layout() {
  const location = useLocation()
  const navigate = useNavigate()
  const message = location.state?.message
  const here = location.pathname + location.search

  // A page shows a success message by navigating with { state: { message } }.
  // This clears it after a few seconds, so reloading the page doesn't bring it back.
  useEffect(() => {
    if (!message) return undefined
    const timer = setTimeout(() => navigate(here, { replace: true }), MESSAGE_SECONDS * 1000)
    return () => clearTimeout(timer)
  }, [location.key, message, here, navigate])

  return (
    <>
      <header className="site-header">
        <div className="container site-header-inner">
          <Link to="/" className="site-name">
            Smarti CRM
          </Link>
          <nav className="site-nav">
            <NavLink to="/" end>
              Overview
            </NavLink>
            <NavLink to="/customers">Customers</NavLink>
            <NavLink to="/jobs">Jobs</NavLink>
            <NavLink to="/staff">Staff</NavLink>
          </nav>
        </div>
      </header>
      <main className="container">
        {message && (
          <div className="success-box" role="status">
            {message}
          </div>
        )}
        <Outlet />
      </main>
    </>
  )
}
