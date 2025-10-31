// pages/login/login.js
Page({
  data: {
    username: '',
    password: '',
    canSubmit: false,
    isLoading: false
  },

  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    });
    this.updateCanSubmit();
  },

  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    });
    this.updateCanSubmit();
  },

  updateCanSubmit() {
    const { username, password } = this.data;
    const canSubmit = username.trim() !== '' && password.trim() !== '';
    this.setData({ canSubmit });
  },

  onLogin() {
    const { username, password } = this.data;
    
    if (!username || !password) {
      wx.showToast({
        title: 'Please fill in all fields',
        icon: 'none'
      });
      return;
    }
    
    const app = getApp();
    
    // Show loading
    this.setData({ isLoading: true });
    wx.showLoading({
      title: 'Logging in...'
    });
    
    // Perform login
    app.login(username, password, (success, data) => {
      wx.hideLoading();
      this.setData({ isLoading: false });
      
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