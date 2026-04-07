import { ReactNode } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authApi } from '../services/api';

interface LayoutProps {
  children: ReactNode;
  isAuthenticated: boolean;
  onLogout: () => void;
}

function Layout({ children, isAuthenticated, onLogout }: LayoutProps) {
  const navigate = useNavigate();

  const handleLogout = () => {
    authApi.logout();
    onLogout();
    navigate('/');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link to="/" className="text-xl font-bold text-gray-800">
            Генератор ТЗ
          </Link>
          <nav className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link to="/dashboard" className="text-gray-600 hover:text-gray-800">
                  Мои ТЗ
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-600 hover:text-gray-800"
                >
                  Выйти
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-600 hover:text-gray-800">
                  Вход
                </Link>
                <Link
                  to="/register"
                  className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                >
                  Регистрация
                </Link>
              </>
            )}
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-8">{children}</main>
    </div>
  );
}

export default Layout;