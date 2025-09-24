const ApiClient = require('../../utils/api.js');
const util = require('../../utils/util.js');
const constants = require('../../utils/constants.js');

Page({
  data: {
    // 历史记录列表
    historyList: [],
    // 收藏列表
    favoriteList: [],
    // 当前标签页
    currentTab: 0,
    // 标签页列表
    tabs: [
      { id: 0, name: '浏览历史', icon: '📖' },
      { id: 1, name: '我的收藏', icon: '❤️' }
    ],
    // 加载状态
    isLoading: false,
    // 编辑模式
    isEditMode: false,
    // 选中的项目
    selectedItems: [],
    // 搜索关键词
    searchKeyword: '',
    // 是否显示搜索
    showSearch: false,
    // 过滤后的列表
    filteredList: [],
    // 统计信息
    statistics: {
      totalViewed: 0,
      totalFavorited: 0,
      todayViewed: 0,
      weekViewed: 0
    }
  },

  onLoad(options) {
    console.log('历史页面加载', options);
    
    // 如果有传入标签参数
    if (options.tab !== undefined) {
      this.setData({ currentTab: parseInt(options.tab) });
    }
    
    this.initPage();
  },

  onShow() {
    console.log('历史页面显示');
    // 每次显示时刷新数据
    this.loadData();
  },

  onReady() {
    wx.setNavigationBarTitle({
      title: '历史记录'
    });
  },

  // 初始化页面
  initPage() {
    this.loadData();
    this.calculateStatistics();
  },

  // 加载数据
  loadData() {
    this.setData({ isLoading: true });
    
    try {
      // 加载历史记录
      const historyList = util.storage.get(constants.STORAGE_KEYS.JOKE_HISTORY, []);
      console.log('历史页面加载数据:', {
        storageKey: constants.STORAGE_KEYS.JOKE_HISTORY,
        historyList: historyList,
        historyLength: historyList ? historyList.length : 0,
        isArray: Array.isArray(historyList)
      });
      
      // 加载收藏列表
      const favoriteList = util.storage.get(constants.STORAGE_KEYS.FAVORITE_JOKES, []);
      console.log('收藏列表数据:', {
        favoriteList: favoriteList,
        favoriteLength: favoriteList ? favoriteList.length : 0
      });
      
      // 确保数据是数组格式
      const validHistoryList = Array.isArray(historyList) ? historyList : [];
      const validFavoriteList = Array.isArray(favoriteList) ? favoriteList : [];
      
      this.setData({
        historyList: validHistoryList,
        favoriteList: validFavoriteList,
        isLoading: false
      });
      
      // 更新过滤后的列表
      this.updateFilteredList();
      
      this.calculateStatistics();
      
    } catch (error) {
      console.error('加载数据失败:', error);
      this.setData({ 
        isLoading: false,
        historyList: [],
        favoriteList: []
      });
      util.showError('加载失败');
    }
  },

  // 计算统计信息
  calculateStatistics() {
    const historyList = this.data.historyList;
    const favoriteList = this.data.favoriteList;
    const today = new Date();
    const todayStr = util.formatTime(today, 'YYYY-MM-DD');
    const weekAgo = new Date(today.getTime() - 7 * 24 * 60 * 60 * 1000);

    let todayViewed = 0;
    let weekViewed = 0;

    historyList.forEach(item => {
      if (item.viewTime) {
        const viewDate = new Date(item.viewTime);
        const viewDateStr = util.formatTime(viewDate, 'YYYY-MM-DD');
        
        if (viewDateStr === todayStr) {
          todayViewed++;
        }
        
        if (viewDate >= weekAgo) {
          weekViewed++;
        }
      }
    });

    this.setData({
      statistics: {
        totalViewed: historyList.length,
        totalFavorited: favoriteList.length,
        todayViewed,
        weekViewed
      }
    });
  },

  // 切换标签页
  switchTab(e) {
    const tabId = e.currentTarget.dataset.id;
    if (tabId === this.data.currentTab) return;

    // 震动反馈
    util.vibrateShort('light');

    this.setData({
      currentTab: tabId,
      isEditMode: false,
      selectedItems: [],
      searchKeyword: '',
      showSearch: false
    });

    // 更新过滤后的列表
    this.updateFilteredList();

    // 更新导航栏标题
    const tabName = this.data.tabs[tabId].name;
    wx.setNavigationBarTitle({
      title: tabName
    });
  },

  // 获取当前列表
  getCurrentList() {
    return this.data.currentTab === 0 ? this.data.historyList : this.data.favoriteList;
  },

  // 获取过滤后的列表
  // 更新过滤后的列表
  updateFilteredList() {
    const list = this.getCurrentList();
    const keyword = this.data.searchKeyword.trim();
    
    console.log('updateFilteredList调用:', {
      currentTab: this.data.currentTab,
      historyListLength: this.data.historyList.length,
      favoriteListLength: this.data.favoriteList.length,
      currentList: list,
      currentListLength: list ? list.length : 0,
      keyword: keyword
    });
    
    let filteredList;
    if (!keyword) {
      console.log('无搜索关键词，返回完整列表:', list);
      filteredList = list || [];
    } else {
      filteredList = (list || []).filter(item => 
        item.content.includes(keyword) || 
        (item.tags && item.tags.some(tag => tag.includes(keyword))) ||
        (item.category && item.category.includes(keyword))
      );
      console.log('过滤后的列表:', filteredList);
    }
    
    this.setData({
      filteredList: filteredList
    });
  },

  getFilteredList() {
    return this.data.filteredList;
  },

  // 检查项目是否被选中
  isItemSelected(itemId) {
    return this.data.selectedItems.some(item => item.id === itemId);
  },

  // 笑话卡片事件处理
  onJokeClick(e) {
    if (this.data.isEditMode) {
      this.toggleSelectItem(e.detail.joke);
    } else {
      console.log('笑话被点击:', e.detail.joke);
      // 更新浏览时间
      this.updateViewTime(e.detail.joke);
    }
  },

  onJokeCopy(e) {
    console.log('笑话被复制:', e.detail.joke);
  },

  onJokeFavorite(e) {
    const joke = e.detail.joke;
    const isFavorited = e.detail.isFavorited;
    
    if (isFavorited) {
      this.addToFavorites(joke);
    } else {
      this.removeFromFavorites(joke);
    }
  },

  onJokeShare(e) {
    console.log('笑话被分享:', e.detail.joke);
  },

  // 更新浏览时间
  updateViewTime(joke) {
    if (this.data.currentTab !== 0) return;
    
    let historyList = [...this.data.historyList];
    const index = historyList.findIndex(item => item.id === joke.id);
    
    if (index !== -1) {
      historyList[index].viewTime = new Date().toISOString();
      // 移到最前面
      const item = historyList.splice(index, 1)[0];
      historyList.unshift(item);
      
      this.setData({ historyList });
      util.storage.set(constants.STORAGE_KEYS.JOKE_HISTORY, historyList);
    }
  },

  // 添加到收藏
  addToFavorites(joke) {
    let favoriteList = [...this.data.favoriteList];
    
    // 检查是否已收藏
    const exists = favoriteList.some(item => item.id === joke.id);
    if (exists) return;
    
    // 添加收藏时间
    const favoriteJoke = {
      ...joke,
      favoriteTime: new Date().toISOString()
    };
    
    favoriteList.unshift(favoriteJoke);
    
    // 限制收藏数量
    if (favoriteList.length > constants.PAGE_CONFIG.MAX_FAVORITE_COUNT) {
      favoriteList = favoriteList.slice(0, constants.PAGE_CONFIG.MAX_FAVORITE_COUNT);
    }
    
    this.setData({ favoriteList });
    util.storage.set(constants.STORAGE_KEYS.FAVORITE_JOKES, favoriteList);
    this.calculateStatistics();
    
    util.showSuccess('已添加到收藏');
  },

  // 从收藏中移除
  removeFromFavorites(joke) {
    let favoriteList = this.data.favoriteList.filter(item => item.id !== joke.id);
    
    this.setData({ favoriteList });
    util.storage.set(constants.STORAGE_KEYS.FAVORITE_JOKES, favoriteList);
    this.calculateStatistics();
    
    util.showSuccess('已取消收藏');
  },

  // 切换编辑模式
  toggleEditMode() {
    const isEditMode = !this.data.isEditMode;
    this.setData({
      isEditMode,
      selectedItems: []
    });
    
    // 震动反馈
    util.vibrateShort('medium');
  },

  // 切换选中项目
  toggleSelectItem(joke) {
    let selectedItems = [...this.data.selectedItems];
    const index = selectedItems.findIndex(item => item.id === joke.id);
    
    if (index !== -1) {
      selectedItems.splice(index, 1);
    } else {
      selectedItems.push(joke);
    }
    
    this.setData({ selectedItems });
    
    // 震动反馈
    util.vibrateShort('light');
  },

  // 全选/取消全选
  toggleSelectAll() {
    const currentList = this.data.filteredList;
    const selectedItems = this.data.selectedItems;
    
    if (selectedItems.length === currentList.length) {
      // 取消全选
      this.setData({ selectedItems: [] });
    } else {
      // 全选
      this.setData({ selectedItems: [...currentList] });
    }
    
    // 震动反馈
    util.vibrateShort('medium');
  },

  // 删除选中项目
  deleteSelectedItems() {
    const selectedItems = this.data.selectedItems;
    if (selectedItems.length === 0) return;
    
    wx.showModal({
      title: '确认删除',
      content: `确定要删除选中的 ${selectedItems.length} 个项目吗？`,
      confirmColor: '#FF4444',
      success: (res) => {
        if (res.confirm) {
          this.performDelete();
        }
      }
    });
  },

  // 执行删除
  performDelete() {
    const selectedIds = this.data.selectedItems.map(item => item.id);
    
    if (this.data.currentTab === 0) {
      // 删除历史记录
      const historyList = this.data.historyList.filter(item => !selectedIds.includes(item.id));
      this.setData({ historyList });
      util.storage.set(constants.STORAGE_KEYS.JOKE_HISTORY, historyList);
    } else {
      // 删除收藏
      const favoriteList = this.data.favoriteList.filter(item => !selectedIds.includes(item.id));
      this.setData({ favoriteList });
      util.storage.set(constants.STORAGE_KEYS.FAVORITE_JOKES, favoriteList);
    }
    
    this.setData({
      selectedItems: [],
      isEditMode: false
    });
    
    this.calculateStatistics();
    
    // 震动反馈
    util.vibrateShort('success');
    util.showSuccess('删除成功');
  },

  // 清空所有记录
  clearAllRecords() {
    const tabName = this.data.tabs[this.data.currentTab].name;
    
    wx.showModal({
      title: '确认清空',
      content: `确定要清空所有${tabName}吗？此操作不可恢复。`,
      confirmColor: '#FF4444',
      success: (res) => {
        if (res.confirm) {
          this.performClearAll();
        }
      }
    });
  },

  // 执行清空
  performClearAll() {
    if (this.data.currentTab === 0) {
      this.setData({ historyList: [] });
      util.storage.set(constants.STORAGE_KEYS.JOKE_HISTORY, []);
    } else {
      this.setData({ favoriteList: [] });
      util.storage.set(constants.STORAGE_KEYS.FAVORITE_JOKES, []);
    }
    
    this.setData({
      selectedItems: [],
      isEditMode: false
    });
    
    this.calculateStatistics();
    
    // 震动反馈
    util.vibrateShort('success');
    util.showSuccess('清空成功');
  },

  // 切换搜索
  toggleSearch() {
    this.setData({
      showSearch: !this.data.showSearch,
      searchKeyword: ''
    });
  },

  // 搜索输入
  onSearchInput(e) {
    const keyword = e.detail.value;
    this.setData({ searchKeyword: keyword });
    // 更新过滤后的列表
    this.updateFilteredList();
  },

  // 跳转到首页
  goToIndex() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  // 导出数据
  exportData() {
    const currentList = this.getCurrentList();
    if (currentList.length === 0) {
      util.showError('没有数据可导出');
      return;
    }
    
    try {
      const exportData = {
        type: this.data.currentTab === 0 ? 'history' : 'favorites',
        exportTime: new Date().toISOString(),
        count: currentList.length,
        data: currentList
      };
      
      const jsonString = JSON.stringify(exportData, null, 2);
      
      // 这里可以实现具体的导出逻辑
      // 比如保存到文件、分享等
      console.log('导出数据:', jsonString);
      
      util.showSuccess('数据已准备就绪');
      
    } catch (error) {
      console.error('导出失败:', error);
      util.showError('导出失败');
    }
  },

  // 下拉刷新
  async onPullDownRefresh() {
    this.loadData();
    wx.stopPullDownRefresh();
  },

  // 分享配置
  onShareAppMessage() {
    const statistics = this.data.statistics;
    return {
      title: `我已经看过 ${statistics.totalViewed} 个笑话，收藏了 ${statistics.totalFavorited} 个`,
      path: '/pages/index/index'
    };
  },

  onShareTimeline() {
    const statistics = this.data.statistics;
    return {
      title: `AI冷笑话生成器 - 已看过 ${statistics.totalViewed} 个笑话`
    };
  }
});