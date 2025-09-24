const ApiClient = require('../../utils/api.js');
const util = require('../../utils/util.js');
const constants = require('../../utils/constants.js');

Page({
  data: {
    // 分类列表
    categories: [],
    // 搜索关键词
    searchKeyword: '',
    // 热门推荐笑话
    recommendJokes: [],
    // 总笑话数量
    totalJokeCount: 0
  },

  onLoad(options) {
    console.log('分类页面加载', options);
    this.initPage();
    
    // 如果有传入分类参数，直接选择该分类
    if (options.category) {
      this.selectCategory(options.category);
    }
  },

  onShow() {
    console.log('分类页面显示');
  },

  onReady() {
    // 设置导航栏
    wx.setNavigationBarTitle({
      title: '笑话分类'
    });
  },

  // 初始化页面
  async initPage() {
    // 设置分类数据
    const categories = constants.JOKE_CATEGORIES.map(category => ({
      ...category,
      count: Math.floor(Math.random() * 100) + 20 // 模拟数据
    }));
    
    this.setData({
      categories,
      totalJokeCount: categories.reduce((sum, cat) => sum + cat.count, 0)
    });
    
    // 加载热门推荐
    await this.loadRecommendJokes();
  },

  // 加载热门推荐笑话
  async loadRecommendJokes() {
    try {
      // 模拟热门推荐数据
      const recommendJokes = [
        {
          id: 'rec1',
          content: '为什么程序员喜欢黑暗？因为光明会产生bug！',
          description: '程序员专属冷笑话'
        },
        {
          id: 'rec2', 
          content: '医生说我得了健忘症，我问他怎么治，他说先交费。',
          description: '生活趣味笑话'
        },
        {
          id: 'rec3',
          content: '老师问：如果地球停止转动会怎样？学生答：大家都会摔倒。',
          description: '校园幽默笑话'
        }
      ];
      
      this.setData({ recommendJokes });
    } catch (error) {
      console.error('加载热门推荐失败:', error);
    }
  },

  // 分类项点击
  onCategoryTap(e) {
    const categoryId = e.currentTarget.dataset.id;
    const category = this.data.categories.find(item => item.id === categoryId);
    if (!category) return;

    console.log('点击分类:', category);

    // 震动反馈
    if (util.vibrateShort) {
      util.vibrateShort('light');
    }

    // 显示分类选择确认
    wx.showModal({
      title: `选择分类: ${category.name}`,
      content: `即将跳转到首页生成${category.name}类型的笑话`,
      confirmText: '确定',
      cancelText: '取消',
      success: (res) => {
        if (res.confirm) {
          // 先设置全局数据
          const app = getApp();
          app.globalData.selectedCategory = {
            id: category.id,
            name: category.name,
            icon: category.icon
          };
          
          console.log('分类页面传递数据:', {
            originalCategoryId: categoryId,
            categoryObject: category,
            passedData: {
              id: category.id,
              name: category.name,
              icon: category.icon
            }
          });
          
          // 跳转到首页
          wx.switchTab({
            url: '/pages/index/index'
          });
          
          // 显示成功提示
          setTimeout(() => {
            wx.showToast({
              title: `已选择${category.name}分类`,
              icon: 'success',
              duration: 2000
            });
          }, 500);
        }
      }
    });
  },

  // 热门推荐笑话点击
  onRecommendJokeTap(e) {
    const joke = e.currentTarget.dataset.joke;
    
    // 震动反馈
    if (util.vibrateShort) {
      util.vibrateShort('light');
    }
    
    // 显示笑话详情
    wx.showModal({
      title: '推荐笑话',
      content: joke.content,
      showCancel: true,
      cancelText: '关闭',
      confirmText: '复制',
      success: (res) => {
        if (res.confirm) {
          wx.setClipboardData({
            data: joke.content,
            success: () => {
              util.showSuccess('已复制到剪贴板');
            }
          });
        }
      }
    });
  },

  // 搜索输入
  onSearchInput(e) {
    const keyword = e.detail.value;
    this.setData({ searchKeyword: keyword });
    
    // 防抖搜索
    if (this.searchTimer) {
      clearTimeout(this.searchTimer);
    }
    
    this.searchTimer = setTimeout(() => {
      this.performSearch(keyword);
    }, 500);
  },

  // 执行搜索
  performSearch(keyword) {
    if (!keyword.trim()) {
      // 恢复原始分类列表
      this.setData({
        categories: constants.JOKE_CATEGORIES.map(category => ({
          ...category,
          count: Math.floor(Math.random() * 100) + 20
        }))
      });
      return;
    }

    // 过滤分类
    const filteredCategories = this.data.categories.filter(category => 
      category.name.includes(keyword) || 
      (category.tags && category.tags.some(tag => tag.includes(keyword)))
    );

    this.setData({ categories: filteredCategories });
  },

  // 下拉刷新
  async onPullDownRefresh() {
    await this.initPage();
    wx.stopPullDownRefresh();
  },

  // 分享配置
  onShareAppMessage() {
    return {
      title: '笑话分类 - AI冷笑话生成器',
      path: '/pages/category/category'
    };
  },

  onShareTimeline() {
    return {
      title: '笑话分类 - AI冷笑话生成器'
    };
  }
});