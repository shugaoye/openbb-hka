// pages/register/register.js
Page({
  data: {
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    canSubmit: false,
    isLoading: false
  },

  onUsernameInput(e) {
    this.setData({
      username: e.detail.value
    });
    this.updateCanSubmit();
  },

  onEmailInput(e) {
    this.setData({
      email: e.detail.value
    });
    this.updateCanSubmit();
  },

  onPasswordInput(e) {
    this.setData({
      password: e.detail.value
    });
    this.updateCanSubmit();
  },

  onConfirmPasswordInput(e) {
    this.setData({
      confirmPassword: e.detail.value
    });
    this.updateCanSubmit();
  },

  updateCanSubmit() {
    const { username, email, password, confirmPassword } = this.data;
    const canSubmit = username.trim() !== '' && 
                      email.trim() !== '' && 
                      password.trim() !== '' && 
                      password === confirmPassword;
    this.setData({ canSubmit });
  },

  onRegister() {
    const { username, email, password } = this.data;
    
    if (!username || !email || !password) {
      wx.showToast({
        title: 'Please fill in all fields',
        icon: 'none'
      });
      return;
    }
    
    if (password.length < 6) {
      wx.showToast({
        title: 'Password must be at least 6 characters',
        icon: 'none'
      });
      return;
    }
    
    const app = getApp();
    
    // Show loading
    this.setData({ isLoading: true });
    wx.showLoading({
      title: 'Creating account...'
    });
    
    // Perform registration
    app.register(username, email, password, (success, data) => {
      wx.hideLoading();
      this.setData({ isLoading: false });
      
      if (success) {
        wx.showToast({
          title: 'Registration successful!',
          icon: 'success'
        });
        
        // Navigate to dashboard
        wx.redirectTo({
          url: '/pages/dashboard/dashboard'
        });
      } else {
        wx.showToast({
          title: data || 'Registration failed',
          icon: 'none'
        });
      }
    });
  },

  goToLogin() {
    wx.navigateTo({
      url: '/pages/login/login'
    });
  }
});