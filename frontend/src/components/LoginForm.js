import React, { useState } from 'react';
import { Card, Button, Form, Alert } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';

const LoginForm = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, error } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!username || !password) return;
    
    setLoading(true);
    const result = await login(username, password);
    setLoading(false);
    
    if (result.success) {
      onLoginSuccess();
    }
  };

  return (
    <div className="form-container">
      <Card>
        <Card.Body>
          <h2 className="text-center mb-4">Login</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          
          <Form onSubmit={handleSubmit}>
            <Form.Group id="username">
              <Form.Label>Username</Form.Label>
              <Form.Control 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)} 
                required 
              />
            </Form.Group>
            
            <Form.Group id="password" className="mb-2">
              <Form.Label>Password</Form.Label>
              <Form.Control 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
              />
            </Form.Group>
            
            <Button 
              disabled={loading} 
              className="w-100 mt-3" 
              type="submit"
            >
              {loading ? 'Logging In...' : 'Log In'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
      <div className="w-100 text-center mt-2">
        Need an account? <a href="#" onClick={(e) => { e.preventDefault(); window.location.hash = 'register'; }}>Register</a>
      </div>
    </div>
  );
};

export default LoginForm;