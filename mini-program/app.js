// app.js
App({
  globalData: {
    userInfo: null,
    token: null
  },
  
  onLaunch: function () {
    // Get token from storage if available
    const token = wx.getStorageSync('token');
    if (token) {
      this.globalData.token = token;
      // Set header for all requests
      wx.request({
        url: 'DUMMY_URL', // Just to set the header for all future requests
        header: {
          'Authorization': 'Bearer ' + token
        },
        success: function() {}
      });
    }
  },

  // Login with username and password
  login: function(username, password, callback) {
    wx.request({
      url: 'https://your-backend-domain.com/auth/token', // Update this to your actual backend URL
      method: 'POST',
      data: {
        username: username,
        password: password
      },
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data.access_token) {
          // Store the token
          wx.setStorageSync('token', res.data.access_token);
          this.globalData.token = res.data.access_token;
          
          // Set header for future requests
          wx.request({
            url: 'DUMMY_URL',
            header: {
              'Authorization': 'Bearer ' + res.data.access_token
            },
            success: function() {}
          });
          
          callback && callback(true, res.data);
        } else {
          callback && callback(false, res.data.detail || 'Login failed');
        }
      },
      fail: (err) => {
        callback && callback(false, 'Network error');
      }
    });
  },

  // Register a new user
  register: function(username, email, password, callback) {
    wx.request({
      url: 'https://your-backend-domain.com/auth/register',
      method: 'POST',
      data: {
        username: username,
        email: email,
        password: password
      },
      header: {
        'Content-Type': 'application/json'
      },
      success: (res) => {
        if (res.statusCode === 200) {
          // Auto-login after registration
          this.login(username, password, callback);
        } else {
          callback && callback(false, res.data.detail || 'Registration failed');
        }
      },
      fail: (err) => {
        callback && callback(false, 'Network error');
      }
    });
  },

  // WeChat login
  wechatLogin: function(callback) {
    // Get the login code from WeChat
    wx.login({
      success: (res) => {
        if (res.code) {
          // Send code to backend to get token
          wx.request({
            url: 'https://your-backend-domain.com/auth/wechat/login',
            method: 'POST',
            data: {
              code: res.code
            },
            header: {
              'Content-Type': 'application/json'
            },
            success: (loginRes) => {
              if (loginRes.statusCode === 200 && loginRes.data.access_token) {
                // Store the token
                wx.setStorageSync('token', loginRes.data.access_token);
                this.globalData.token = loginRes.data.access_token;
                
                callback && callback(true, loginRes.data);
              } else {
                callback && callback(false, loginRes.data.detail || 'WeChat login failed');
              }
            },
            fail: (err) => {
              callback && callback(false, 'Network error');
            }
          });
        } else {
          callback && callback(false, 'Failed to get login code');
        }
      },
      fail: (err) => {
        callback && callback(false, 'WeChat login failed');
      }
    });
  }
});