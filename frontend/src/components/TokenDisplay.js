import React, { useState, useEffect } from 'react';
import { Card, Button, Alert } from 'react-bootstrap';
import axios from 'axios';

const TokenDisplay = () => {
  const [token, setToken] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchToken();
  }, []);

  const fetchToken = async () => {
    try {
      // Get the current user info to verify the token is still valid
      const response = await axios.get('/auth/me');
      // The token is already in localStorage, so just get it from there
      const storedToken = localStorage.getItem('token');
      setToken(storedToken || '');
    } catch (err) {
      setError('Failed to verify token: ' + err.message);
      // Fallback: get token from localStorage
      const storedToken = localStorage.getItem('token');
      if (storedToken) {
        setToken(storedToken);
      }
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(token)
      .then(() => {
        alert('Token copied to clipboard!');
      })
      .catch(err => {
        console.error('Failed to copy token: ', err);
        alert('Failed to copy token');
      });
  };

  return (
    <div className="token-display-container">
      <h2 className="mb-4">Your Access Token</h2>
      
      {error && <Alert variant="danger">{error}</Alert>}
      
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Access Token</Card.Title>
          <Card.Text>
            Copy this token and use it with OpenBB Workspace to access protected endpoints.
          </Card.Text>
          
          {loading ? (
            <p>Loading token...</p>
          ) : (
            <div className="token-display">
              <textarea 
                value={token} 
                readOnly 
                rows="3"
                className="form-control mb-2"
              />
              <Button 
                variant="primary" 
                className="copy-btn"
                onClick={copyToClipboard}
              >
                Copy Token
              </Button>
            </div>
          )}
        </Card.Body>
      </Card>
      
      <Card>
        <Card.Body>
          <Card.Title>How to use this token with OpenBB Workspace</Card.Title>
          <Card.Text>
            <ol>
              <li>Copy the token above</li>
              <li>In OpenBB Workspace, go to Settings > API Keys</li>
              <li>Add a new API key with the following details:
                <ul>
                  <li>Name: FinApp Auth Token</li>
                  <li>Key: Paste the token here</li>
                  <li>Provider: Custom</li>
                </ul>
              </li>
              <li>Save and use this key to access protected endpoints</li>
            </ol>
          </Card.Text>
        </Card.Body>
      </Card>
    </div>
  );
};

export default TokenDisplay;