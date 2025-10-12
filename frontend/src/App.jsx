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
import NotFound from './pages/NotFound';
import useAuth from './hooks/useAuth';

// Componente wrapper para manejar la redirección inicial
const AppRoutes = () => {
  const { isAuthenticated, isInitializing } = useAuth();

  // Mostrar loading mientras se inicializa
  if (isInitializing) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
        flexDirection: 'column',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white'
      }}>
        <div style={{
          border: '4px solid rgba(255, 255, 255, 0.3)',
          borderTop: '4px solid white',
          borderRadius: '50%',
          width: '50px',
          height: '50px',
          animation: 'spin 1s linear infinite',
          marginBottom: '1rem'
        }}></div>
        <h2>Cargando Sistema VNM...</h2>
        <p>Inicializando autenticación</p>
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
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
                <div style={{ padding: '2rem', textAlign: 'center' }}>
                  <h2>📡 Módulo de Monitoreo</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                  <div style={{ 
                    background: '#f8f9fa', 
                    padding: '2rem', 
                    borderRadius: '8px',
                    marginTop: '2rem'
                  }}>
                    <h3>Características planeadas:</h3>
                    <ul style={{ textAlign: 'left', maxWidth: '400px', margin: '0 auto' }}>
                      <li>📊 Monitoreo en tiempo real</li>
                      <li>📈 Gráficos de rendimiento</li>
                      <li>🚨 Sistema de alertas</li>
                      <li>🗺️ Mapas de red</li>
                    </ul>
                  </div>
                </div>
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/reports" 
            element={
              <ProtectedRoute>
                <div style={{ padding: '2rem', textAlign: 'center' }}>
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
                <div style={{ padding: '2rem', textAlign: 'center' }}>
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
                <div style={{ padding: '2rem', textAlign: 'center' }}>
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
                <div style={{ padding: '2rem', textAlign: 'center' }}>
                  <h2>⚙️ Panel de Administración</h2>
                  <p>En desarrollo - Próximamente disponible</p>
                  <div style={{ 
                    background: '#fff3cd', 
                    padding: '1rem', 
                    borderRadius: '8px',
                    marginTop: '2rem',
                    border: '1px solid #ffeaa7'
                  }}>
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

      {/* Estilos globales */}
      <style jsx global>{`
        * {
          margin: 0;
          padding: 0;
          box-sizing: border-box;
        }

        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background-color: #f8f9fa;
          color: #333;
          line-height: 1.6;
        }

        .app {
          min-height: 100vh;
          display: flex;
          flex-direction: column;
        }

        .main-content {
          flex: 1;
        }

        /* Utilidades globales */
        .text-center { text-align: center; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }

        .mt-1 { margin-top: 0.25rem; }
        .mt-2 { margin-top: 0.5rem; }
        .mt-3 { margin-top: 1rem; }
        .mt-4 { margin-top: 1.5rem; }

        .mb-1 { margin-bottom: 0.25rem; }
        .mb-2 { margin-bottom: 0.5rem; }
        .mb-3 { margin-bottom: 1rem; }
        .mb-4 { margin-bottom: 1.5rem; }

        .p-1 { padding: 0.25rem; }
        .p-2 { padding: 0.5rem; }
        .p-3 { padding: 1rem; }
        .p-4 { padding: 1.5rem; }

        /* Botones estándar */
        .btn {
          display: inline-block;
          padding: 0.75rem 1.5rem;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 600;
          text-decoration: none;
          transition: all 0.2s ease;
          text-align: center;
        }

        .btn-primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .btn-primary:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .btn-secondary {
          background: #6c757d;
          color: white;
        }

        .btn-secondary:hover {
          background: #5a6268;
        }

        /* Scroll suave */
        html {
          scroll-behavior: smooth;
        }

        /* Focus styles para accesibilidad */
        button:focus,
        input:focus,
        select:focus,
        textarea:focus {
          outline: 2px solid #667eea;
          outline-offset: 2px;
        }
      `}</style>
    </div>
  );
};

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;