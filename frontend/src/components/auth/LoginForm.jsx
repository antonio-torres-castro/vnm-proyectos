/**
 * Componente LoginForm
 * Formulario de autenticación que se conecta al backend IAM
 */
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

const LoginForm = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isLoading, error, clearError, isAuthenticated } = useAuth();

  // Estado del formulario
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const [formErrors, setFormErrors] = useState({});
  const [showPassword, setShowPassword] = useState(false);
  const [submitAttempted, setSubmitAttempted] = useState(false);

  // Obtener la ruta de origen para redirección después del login
  const from = location.state?.from || '/dashboard';
  const loginMessage = location.state?.message;

  // Redireccionar si ya está autenticado
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  // Limpiar errores cuando el componente se monta
  useEffect(() => {
    clearError();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []); // Solo ejecutar al montar el componente

  // Manejar cambios en los inputs
  const handleInputChange = e => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));

    // Limpiar error específico del campo cuando se empieza a escribir
    if (formErrors[name]) {
      setFormErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }

    // El error global se limpiará automáticamente al escribir
  };

  // Validar formulario
  const validateForm = () => {
    const errors = {};

    if (!formData.email.trim()) {
      errors.email = 'El email es requerido';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Formato de email inválido';
    }

    if (!formData.password) {
      errors.password = 'La contraseña es requerida';
    } else if (formData.password.length < 4) {
      errors.password = 'La contraseña debe tener al menos 4 caracteres';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  // Manejar envío del formulario
  const handleSubmit = async e => {
    e.preventDefault();
    setSubmitAttempted(true);

    if (!validateForm()) {
      return;
    }

    try {
      const result = await login({
        email: formData.email.trim(),
        clave: formData.password,
      });

      if (result.success) {
        // Login exitoso - la redirección se maneja en el useEffect
      }
      // Si no es exitoso, el error se maneja automáticamente por el contexto
    } catch (err) {
      console.error('Error inesperado en login:', err);
    }
  };

  // Manejar Enter en los campos
  const handleKeyPress = e => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="login-container">
      <div className="login-form-wrapper">
        <div className="login-header">
          <h1>🚀 Sistema VNM</h1>
          <h2>Iniciar Sesión</h2>
          <p>Monitoreo de Red IP</p>
        </div>

        {/* Mensaje de redirección */}
        {loginMessage && (
          <div className="alert alert-info">
            <span>ℹ️</span>
            {loginMessage}
          </div>
        )}

        {/* Error global */}
        {error && (
          <div className="alert alert-error">
            <span>⚠️</span>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          {/* Campo Email */}
          <div className="form-group">
            <label htmlFor="email">✉️ Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              className={`form-input ${formErrors.email ? 'error' : ''}`}
              placeholder="Ingresa tu email"
              disabled={isLoading}
              autoComplete="email"
              autoFocus
            />
            {formErrors.email && (
              <span className="error-message">{formErrors.email}</span>
            )}
          </div>

          {/* Campo Password */}
          <div className="form-group">
            <label htmlFor="password">🔐 Contraseña</label>
            <div className="password-input-wrapper">
              <input
                type={showPassword ? 'text' : 'password'}
                id="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                className={`form-input ${formErrors.password ? 'error' : ''}`}
                placeholder="Ingresa tu contraseña"
                disabled={isLoading}
                autoComplete="current-password"
              />
              <button
                type="button"
                className="password-toggle"
                onClick={() => setShowPassword(!showPassword)}
                disabled={isLoading}
                title={
                  showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'
                }
              >
                {showPassword ? '👁️' : '👁️‍🗨️'}
              </button>
            </div>
            {formErrors.password && (
              <span className="error-message">{formErrors.password}</span>
            )}
          </div>

          {/* Botón de envío */}
          <button
            type="submit"
            className={`login-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span className="spinner"></span>
                Iniciando sesión...
              </>
            ) : (
              '🚀 Iniciar Sesión'
            )}
          </button>
        </form>

        {/* Información adicional */}
        <div className="login-footer">
          <p>
            <small>
              💡 Usa el email y contraseña proporcionados por el administrador
              del sistema
            </small>
          </p>
        </div>
      </div>

      {/* Estilos CSS embebidos */}
      <style>{`
        .login-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: linear-gradient(135deg, #FF2315 0%, #B52217 100%);
          padding: 1rem;
        }

        .login-form-wrapper {
          background: white;
          border-radius: 12px;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
          padding: 2.5rem;
          width: 100%;
          max-width: 400px;
          animation: slideUp 0.5s ease-out;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .login-header {
          text-align: center;
          margin-bottom: 2rem;
        }

        .login-header h1 {
          color: #333;
          font-size: 1.8rem;
          margin: 0 0 0.5rem 0;
        }

        .login-header h2 {
          color: #555;
          font-size: 1.3rem;
          margin: 0 0 0.25rem 0;
          font-weight: normal;
        }

        .login-header p {
          color: #777;
          font-size: 0.9rem;
          margin: 0;
        }

        .alert {
          padding: 0.75rem 1rem;
          border-radius: 6px;
          margin-bottom: 1rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.9rem;
        }

        .alert-info {
          background-color: #e3f2fd;
          color: #1976d2;
          border: 1px solid #bbdefb;
        }

        .alert-error {
          background-color: #ffebee;
          color: #d32f2f;
          border: 1px solid #ffcdd2;
        }

        .login-form {
          margin-bottom: 1.5rem;
        }

        .form-group {
          margin-bottom: 1.25rem;
        }

        .form-group label {
          display: block;
          margin-bottom: 0.5rem;
          color: #333;
          font-weight: 500;
          font-size: 0.9rem;
        }

        .form-input {
          width: 100%;
          padding: 0.875rem 1rem;
          border: 2px solid #e1e5e9;
          border-radius: 6px;
          font-size: 1rem;
          transition: all 0.2s ease;
          box-sizing: border-box;
        }

        .form-input:focus {
          outline: none;
          border-color: #FF2315;
          box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .form-input.error {
          border-color: #f44336;
        }

        .form-input:disabled {
          background-color: #f5f5f5;
          cursor: not-allowed;
        }

        .password-input-wrapper {
          position: relative;
        }

        .password-input-wrapper .form-input {
          padding-right: 3rem;
        }

        .password-toggle {
          position: absolute;
          right: 0.75rem;
          top: 50%;
          transform: translateY(-50%);
          background: none;
          border: none;
          cursor: pointer;
          font-size: 1.1rem;
          padding: 0.25rem;
          border-radius: 4px;
          transition: background-color 0.2s ease;
        }

        .password-toggle:hover:not(:disabled) {
          background-color: #f0f0f0;
        }

        .password-toggle:disabled {
          cursor: not-allowed;
          opacity: 0.5;
        }

        .error-message {
          color: #f44336;
          font-size: 0.8rem;
          margin-top: 0.25rem;
          display: block;
        }

        .login-button {
          width: 100%;
          padding: 1rem;
          background: linear-gradient(135deg, #FF2315 0%, #B52217 100%);
          color: white;
          border: none;
          border-radius: 6px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.5rem;
        }

        .login-button:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .login-button:disabled {
          cursor: not-allowed;
          opacity: 0.7;
          transform: none;
        }

        .login-button.loading {
          position: relative;
        }

        .spinner {
          width: 16px;
          height: 16px;
          border: 2px solid transparent;
          border-top: 2px solid currentColor;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        .login-footer {
          text-align: center;
          padding-top: 1rem;
          border-top: 1px solid #eee;
        }

        .login-footer small {
          color: #666;
          line-height: 1.4;
        }

        /* Responsive */
        @media (max-width: 480px) {
          .login-form-wrapper {
            padding: 2rem 1.5rem;
            margin: 1rem;
          }
        }
      `}</style>
    </div>
  );
};

export default LoginForm;
