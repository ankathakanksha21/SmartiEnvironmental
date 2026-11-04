import { useEffect, useState } from 'react'
import { Link, NavLink, Outlet } from 'react-router'

const MESSAGE_SECONDS = 5

// The header shown on every page. The current page appears in <Outlet />.
export default function Layout() {
  const [message, setMessage] = useState(null)

  // Pages get this through useOutletContext. Each call makes a new object, so a
  // second message restarts the timer even if its text is the same.
  const showMessage = (text) => setMessage({ text })

  useEffect(() => {
    if (!message) return undefined
    const timer = setTimeout(() => setMessage(null), MESSAGE_SECONDS * 1000)
    return () => clearTimeout(timer)
  }, [message])

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
        <Outlet context={showMessage} />
      </main>
      {/* Screen readers announce changes inside this, so it stays on the page. */}
      <div role="status">{message && <div className="success-box">{message.text}</div>}</div>
    </>
  )
}
