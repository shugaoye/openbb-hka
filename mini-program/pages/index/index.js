// pages/index/index.js
Page({
  data: {
    hasUserInfo: false,
    canIUseGetUserProfile: false
  },

  onLoad() {
    // Check if user is already logged in
    this.checkLoginStatus();
  },

  checkLoginStatus() {
    const token = wx.getStorageSync('token');
    if (token) {
      // User is logged in, redirect to dashboard
      wx.redirectTo({
        url: '/pages/dashboard/dashboard'
      });
    }
  },

  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  },

  goToRegister() {
    wx.navigateTo({
      url: '/pages/register/register'
    });
  },

  wechatLogin() {
    const app = getApp();
    
    // Show loading
    wx.showLoading({
      title: 'Logging in...'
    });
    
    // Perform WeChat login
    app.wechatLogin((success, data) => {
      wx.hideLoading();
      
      if (success) {
        wx.showToast({
          title: 'Login successful!',
          icon: 'success'
        });
        
        // Navigate to dashboard
        wx.redirectTo({
          url: '/pages/dashboard/dashboard'
        });
      } else {
        wx.showToast({
          title: data || 'Login failed',
          icon: 'none'
        });
      }
    });
  }
});