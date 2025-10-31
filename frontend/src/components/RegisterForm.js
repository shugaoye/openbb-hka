import React, { useState } from 'react';
import { Card, Button, Form, Alert } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';

const RegisterForm = ({ onRegisterSuccess }) => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { register, error } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }
    
    if (!username || !password || !email) return;
    
    setLoading(true);
    const result = await register(username, email, password);
    setLoading(false);
    
    if (result.success) {
      onRegisterSuccess();
    }
  };

  return (
    <div className="form-container">
      <Card>
        <Card.Body>
          <h2 className="text-center mb-4">Create Account</h2>
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
            
            <Form.Group id="email" className="mb-2">
              <Form.Label>Email</Form.Label>
              <Form.Control 
                type="email" 
                value={email} 
                onChange={(e) => setEmail(e.target.value)} 
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
            
            <Form.Group id="confirm-password" className="mb-2">
              <Form.Label>Confirm Password</Form.Label>
              <Form.Control 
                type="password" 
                value={confirmPassword} 
                onChange={(e) => setConfirmPassword(e.target.value)} 
                required 
              />
            </Form.Group>
            
            <Button 
              disabled={loading} 
              className="w-100 mt-3" 
              type="submit"
            >
              {loading ? 'Creating Account...' : 'Sign Up'}
            </Button>
          </Form>
        </Card.Body>
      </Card>
      <div className="w-100 text-center mt-2">
        Already have an account? <a href="#" onClick={(e) => { e.preventDefault(); window.location.hash = 'login'; }}>Log In</a>
      </div>
    </div>
  );
};

export default RegisterForm;