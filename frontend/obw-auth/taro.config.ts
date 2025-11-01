import { defineConfig } from '@tarojs/cli'

export default defineConfig({
  projectName: 'obw-auth',
  date: '2025-10-31',
  designWidth: 750,
  deviceRatio: {
    640: 2.34 / 2,
    750: 1,
    828: 1.81 / 2
  },
  sourceRoot: 'src',
  outputRoot: 'dist',
  framework: 'react',
  compiler: {
    type: 'vite'
  },
  sass: {},
  defineConstants: {},
  copy: {
    patterns: [],
    options: {}
  },
  alias: {},
  h5: {
    publicPath: '/',
    staticDirectory: 'static'
  },
  mini: {
    postcss: {
      pxtransform: {
        enable: true
      },
      url: {
        enable: true,
        limit: 1024
      }
    }
  }
})
