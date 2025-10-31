// pages/dashboard/dashboard.js
Page({
  data: {
    token: ''
  },

  onLoad() {
    // Get token from global data or storage
    const app = getApp();
    const token = app.globalData.token || wx.getStorageSync('token');
    
    if (token) {
      this.setData({
        token: token
      });
    } else {
      // If no token, redirect to login
      wx.redirectTo({
        url: '/pages/login/login'
      });
    }
  },

  copyToken() {
    const { token } = this.data;
    if (token) {
      wx.setClipboardData({
        data: token,
        success: () => {
          wx.showToast({
            title: 'Token copied!',
            icon: 'success'
          });
        },
        fail: () => {
          wx.showToast({
            title: 'Failed to copy',
            icon: 'none'
          });
        }
      });
    }
  },

  logout() {
    // Clear token from storage and global data
    wx.clearStorage({
      success: () => {
        const app = getApp();
        app.globalData.token = null;
        
        wx.showToast({
          title: 'Logged out',
          icon: 'success'
        });
        
        // Redirect to index
        wx.redirectTo({
          url: '/pages/index/index'
        });
      }
    });
  }
});