// 加载组件
Component({
  properties: {
    // 是否显示加载
    show: {
      type: Boolean,
      value: false
    },
    // 加载文本
    text: {
      type: String,
      value: '加载中...'
    },
    // 加载类型
    type: {
      type: String,
      value: 'default' // default, dots, spinner
    },
    // 大小
    size: {
      type: String,
      value: 'medium' // small, medium, large
    },
    // 颜色
    color: {
      type: String,
      value: '#4A90E2'
    },
    // 是否全屏
    fullscreen: {
      type: Boolean,
      value: false
    }
  },

  data: {
    animationClass: ''
  },

  lifetimes: {
    attached() {
      this.startAnimation();
    },

    detached() {
      this.stopAnimation();
    }
  },

  observers: {
    'show': function(show) {
      if (show) {
        this.startAnimation();
      } else {
        this.stopAnimation();
      }
    }
  },

  methods: {
    // 开始动画
    startAnimation() {
      if (!this.data.show) return;
      
      this.setData({
        animationClass: 'animate'
      });
    },

    // 停止动画
    stopAnimation() {
      this.setData({
        animationClass: ''
      });
    },

    // 点击遮罩
    onMaskTap() {
      // 全屏模式下不允许点击关闭
      if (!this.data.fullscreen) {
        this.triggerEvent('close');
      }
    }
  }
});