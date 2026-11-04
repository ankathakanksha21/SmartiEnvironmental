import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router'
import Layout from './components/Layout.jsx'
import CustomerDetail from './pages/CustomerDetail.jsx'
import CustomerEdit from './pages/CustomerEdit.jsx'
import CustomerList from './pages/CustomerList.jsx'
import CustomerNew from './pages/CustomerNew.jsx'
import JobDetail from './pages/JobDetail.jsx'
import JobEdit from './pages/JobEdit.jsx'
import JobList from './pages/JobList.jsx'
import JobNew from './pages/JobNew.jsx'
import NotFound from './pages/NotFound.jsx'
import StaffDetail from './pages/StaffDetail.jsx'
import StaffEdit from './pages/StaffEdit.jsx'
import StaffList from './pages/StaffList.jsx'
import StaffNew from './pages/StaffNew.jsx'
import './style.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route index element={<Navigate to="/customers" replace />} />
          <Route path="customers" element={<CustomerList />} />
          <Route path="customers/new" element={<CustomerNew />} />
          <Route path="customers/:id" element={<CustomerDetail />} />
          <Route path="customers/:id/edit" element={<CustomerEdit />} />
          <Route path="jobs" element={<JobList />} />
          <Route path="jobs/new" element={<JobNew />} />
          <Route path="jobs/:id" element={<JobDetail />} />
          <Route path="jobs/:id/edit" element={<JobEdit />} />
          <Route path="staff" element={<StaffList />} />
          <Route path="staff/new" element={<StaffNew />} />
          <Route path="staff/:id" element={<StaffDetail />} />
          <Route path="staff/:id/edit" element={<StaffEdit />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
