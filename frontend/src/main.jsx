import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Navigate, Route, Routes } from 'react-router'
import Layout from './components/Layout.jsx'
import CustomerDetail from './pages/CustomerDetail.jsx'
import CustomerEdit from './pages/CustomerEdit.jsx'
import CustomerList from './pages/CustomerList.jsx'
import CustomerNew from './pages/CustomerNew.jsx'
import NotFound from './pages/NotFound.jsx'
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
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
