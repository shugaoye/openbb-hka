import React, { useState, useEffect } from 'react';
import { Container, Nav, Navbar, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import WeChatLogin from './components/WeChatLogin';
import TokenDisplay from './components/TokenDisplay';
import './App.css';

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

const AppContent = () => {
  const { currentUser, logout, error: authError } = useAuth();
  const [activeTab, setActiveTab] = useState('login');

  const handleLogout = async () => {
    try {
      await logout();
      setActiveTab('login');
    } catch (error) {
      console.error('Failed to log out:', error);
    }
  };

  return (
    <div className="App">
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-4">
        <Container>
          <Navbar.Brand href="#home">OpenBB Authentication</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {currentUser ? (
                <>
                  <Nav.Link onClick={() => setActiveTab('dashboard')}>Dashboard</Nav.Link>
                  <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
                </>
              ) : (
                <>
                  <Nav.Link onClick={() => setActiveTab('login')}>Login</Nav.Link>
                  <Nav.Link onClick={() => setActiveTab('register')}>Register</Nav.Link>
                  <Nav.Link onClick={() => setActiveTab('wechat')}>WeChat Login</Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container>
        {authError && <Alert variant="danger">{authError}</Alert>}

        {!currentUser ? (
          <>
            {activeTab === 'login' && <LoginForm onLoginSuccess={() => setActiveTab('dashboard')} />}
            {activeTab === 'register' && <RegisterForm onRegisterSuccess={() => setActiveTab('login')} />}
            {activeTab === 'wechat' && <WeChatLogin onLoginSuccess={() => setActiveTab('dashboard')} />}
          </>
        ) : (
          <TokenDisplay />
        )}
      </Container>
    </div>
  );
};

export default App;