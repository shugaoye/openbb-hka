import React, { useState, useEffect } from 'react';
import { Card, Button, Alert, Spinner } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';

const WeChatLogin = ({ onLoginSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [isWeChat, setIsWeChat] = useState(false);
  const [error, setError] = useState('');
  const { wechatLogin } = useAuth();

  // Check if user is in WeChat browser
  useEffect(() => {
    const ua = navigator.userAgent.toLowerCase();
    setIsWeChat(ua.includes('micromessenger'));
  }, []);

  const handleWeChatLogin = async () => {
    if (isWeChat) {
      // In WeChat environment, we might need to use WeChat JS SDK
      // For now, we'll simulate with a QR code approach
      setError('Please use the WeChat app to scan the QR code for login');
      // In a real implementation, you'd use the WeChat JS SDK to get the code
    } else {
      // For web browser, we'll use a simulated approach or redirect to WeChat OAuth
      // This will redirect to WeChat OAuth URL
      // Generate a random state for security
      const state = Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      const redirectUri = encodeURIComponent(window.location.origin + window.location.pathname);
      const wechatAuthUrl = `https://open.weixin.qq.com/connect/qrconnect?appid=${process.env.REACT_APP_WECHAT_APP_ID || 'YOUR_WECHAT_APP_ID'}&redirect_uri=${redirectUri}&response_type=code&scope=snsapi_login&state=${state}#wechat_redirect`;
      
      // Store a temporary state to handle the callback
      localStorage.setItem('wechat_login_callback', window.location.href);
      
      // Redirect to WeChat OAuth
      window.location.href = wechatAuthUrl;
    }
  };

  // Function to handle the WeChat OAuth callback
  const handleWeChatCallback = async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    const state = urlParams.get('state');  // Verify state for security
    
    if (code) {
      setLoading(true);
      setError('');
      
      try {
        const result = await wechatLogin(code);
        setLoading(false);
        
        if (result.success) {
          // Redirect back to the original page or home
          const originalPage = localStorage.getItem('wechat_login_callback');
          if (originalPage) {
            localStorage.removeItem('wechat_login_callback');
            window.location.href = originalPage;
          } else {
            onLoginSuccess();
          }
        } else {
          setError(result.error);
        }
      } catch (err) {
        setLoading(false);
        setError('WeChat login failed: ' + err.message);
      }
    }
  };

  // Check if this is a callback from WeChat OAuth
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    if (code) {
      handleWeChatCallback();
    }
  }, []);

  return (
    <div className="form-container">
      <Card>
        <Card.Body>
          <h2 className="text-center mb-4">WeChat Login</h2>
          {error && <Alert variant="danger">{error}</Alert>}
          
          <div className="text-center">
            <p>Scan the QR code with WeChat to log in:</p>
            
            {isWeChat ? (
              <div>
                <p>You are already in the WeChat app!</p>
                <Button 
                  disabled={loading}
                  onClick={handleWeChatLogin}
                  variant="success"
                >
                  {loading ? <Spinner as="span" animation="border" size="sm" /> : 'Login with WeChat'}
                </Button>
              </div>
            ) : (
              <div>
                <div className="wechat-qr-placeholder mb-3">
                  <img 
                    src="data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 200 200'%3e%3crect width='200' height='200' fill='%23f8f9fa'/%3e%3crect x='20' y='20' width='160' height='160' fill='white'/%3e%3ctext x='100' y='100' font-family='Arial' font-size='14' fill='%236c757d' text-anchor='middle' dominant-baseline='middle'%3eWeChat QR Code%3c/text%3e%3c/svg%3e" 
                    alt="WeChat QR Code" 
                    className="img-fluid"
                  />
                </div>
                <Button 
                  disabled={loading}
                  onClick={handleWeChatLogin}
                  variant="success"
                >
                  {loading ? <Spinner as="span" animation="border" size="sm" /> : 'Get WeChat QR Code'}
                </Button>
              </div>
            )}
            
            <p className="mt-3 text-muted">
              {isWeChat 
                ? 'Click the button above to log in with WeChat' 
                : 'Click the button above to get a QR code for WeChat login'}
            </p>
          </div>
        </Card.Body>
      </Card>
      <div className="w-100 text-center mt-2">
        Use regular login? <a href="#" onClick={(e) => { e.preventDefault(); window.location.hash = 'login'; }}>Log In</a>
      </div>
    </div>
  );
};

export default WeChatLogin;