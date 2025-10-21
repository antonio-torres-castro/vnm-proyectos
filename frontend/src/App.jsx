/**
 * Aplicación Principal
 * Configuración de rutas y sistema de autenticación
 */
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import Header from './components/layout/Header';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import MonitoringPage from './pages/MonitoringPage';
import NotFound from './pages/NotFound';
import useAuth from './hooks/useAuth';

// Componente wrapper para manejar la redirección inicial
const AppRoutes = () => {
  const { isAuthenticated, isInitializing } = useAuth();

  // Mostrar loading mientras se inicializa
  if (isInitializing) {
    return (
      <div className="loading-screen">
        <div className="loading-spinner"></div>
        <h2>Cargando Sistema VNM...</h2>
        <p>Inicializando autenticación</p>
      </div>
    );
  }

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <Routes>
          {/* Redirección de la raíz */}
          <Route 
            path="/" 
            element={
              isAuthenticated ? 
                <Navigate to="/dashboard" replace /> : 
                <Navigate to="/login" replace />
            } 
          />
          
          {/* Página de login */}
          <Route path="/login" element={<LoginPage />} />
          
          {/* Rutas protegidas */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          {/* Rutas futuras del sistema */}
          <Route 
            path="/monitoring" 
            element={
              <ProtectedRoute>
                <MonitoringPage />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/reports" 
            element={
              <ProtectedRoute>
                <div className="placeholder-page">
                  <h2>📈 Módulo de Reportes</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                </div>
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/profile" 
            element={
              <ProtectedRoute>
                <div className="placeholder-page">
                  <h2>👤 Mi Perfil</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                </div>
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/settings" 
            element={
              <ProtectedRoute>
                <div className="placeholder-page">
                  <h2>⚙️ Configuración</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                </div>
              </ProtectedRoute>
            } 
          />
          
          {/* Rutas de administración */}
          <Route 
            path="/admin/*" 
            element={
              <ProtectedRoute requiredRoles={['Administrador', 'Super Admin']}>
                <div className="placeholder-page">
                  <h2>⚙️ Panel de Administración</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                  <div className="admin-notice">
                    <strong>🔐 Acceso de Administrador Detectado</strong>
                    <p>Tienes permisos para acceder a funciones administrativas</p>
                  </div>
                </div>
              </ProtectedRoute>
            } 
          />
          
          {/* Página 404 */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true
      }}
    >
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;