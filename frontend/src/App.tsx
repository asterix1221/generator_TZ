import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import SpecificationView from './pages/SpecificationView';
import SharedSpec from './pages/SharedSpec';
import { useEffect, useState } from 'react';
import { authApi } from './services/api';

function App() {
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = authApi.getToken();
    setIsAuthenticated(!!token);
    setLoading(false);
  }, []);

  if (loading) {
    return <div className="flex items-center justify-center h-screen">Загрузка...</div>;
  }

  return (
    <BrowserRouter>
      <Layout isAuthenticated={isAuthenticated} onLogout={() => setIsAuthenticated(false)}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/shared/:token" element={<SharedSpec />} />
          <Route 
            path="/login" 
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Login onLogin={() => setIsAuthenticated(true)} />} 
          />
          <Route 
            path="/register" 
            element={isAuthenticated ? <Navigate to="/dashboard" /> : <Register onRegister={() => setIsAuthenticated(true)} />} 
          />
          <Route 
            path="/dashboard" 
            element={isAuthenticated ? <Dashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/specification/:id" 
            element={isAuthenticated ? <SpecificationView /> : <Navigate to="/login" />} 
          />
        </Routes>
      </Layout>
      <Toaster position="top-right" />
    </BrowserRouter>
  );
}

export default App;