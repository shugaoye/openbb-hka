import React, { useState } from 'react';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import TokenDisplay from './components/TokenDisplay';

function App() {
  const [currentView, setCurrentView] = useState<'login' | 'register' | 'token'>('login');
  const [token, setToken] = useState<string>('');

  const handleLoginSuccess = (jwtToken: string) => {
    setToken(jwtToken);
    setCurrentView('token');
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
            OpenBB Workspace Authentication
          </h2>
        </div>
        
        {currentView === 'login' && (
          <LoginForm 
            onLoginSuccess={handleLoginSuccess} 
            onSwitchToRegister={() => setCurrentView('register')} 
          />
        )}
        
        {currentView === 'register' && (
          <RegisterForm 
            onRegisterSuccess={handleLoginSuccess} 
            onSwitchToLogin={() => setCurrentView('login')} 
          />
        )}
        
        {currentView === 'token' && (
          <TokenDisplay 
            token={token} 
            onLogout={() => setCurrentView('login')} 
          />
        )}
      </div>
    </div>
  );
}

export default App;