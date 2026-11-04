import { Link, Outlet } from 'react-router'

// The header shown on every page. The current page appears in <Outlet />.
export default function Layout() {
  return (
    <>
      <header className="site-header">
        <div className="container site-header-inner">
          <Link to="/" className="site-name">
            Smarti CRM
          </Link>
        </div>
      </header>
      <main className="container">
        <Outlet />
      </main>
    </>
  )
}
