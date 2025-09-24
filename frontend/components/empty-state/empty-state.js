// 空状态组件
Component({
  properties: {
    // 图标
    icon: {
      type: String,
      value: '📭'
    },
    // 标题
    title: {
      type: String,
      value: '暂无内容'
    },
    // 描述
    description: {
      type: String,
      value: ''
    },
    // 按钮文本
    buttonText: {
      type: String,
      value: ''
    },
    // 按钮类型
    buttonType: {
      type: String,
      value: 'primary' // primary, secondary
    },
    // 是否显示
    show: {
      type: Boolean,
      value: true
    },
    // 自定义样式类
    customClass: {
      type: String,
      value: ''
    }
  },

  methods: {
    // 按钮点击事件
    onButtonTap() {
      this.triggerEvent('buttonclick');
    }
  }
});