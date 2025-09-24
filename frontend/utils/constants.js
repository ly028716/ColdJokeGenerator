// 常量定义

// 笑话分类
const JOKE_CATEGORIES = [
  { id: 'programmer', name: '程序员', icon: '💻', color: '#4A90E2' },
  { id: 'daily', name: '日常生活', icon: '🏠', color: '#07C160' },
  { id: 'work', name: '职场', icon: '💼', color: '#FF6B6B' },
  { id: 'love', name: '恋爱', icon: '💕', color: '#FF69B4' },
  { id: 'student', name: '学生', icon: '📚', color: '#9C27B0' },
  { id: 'food', name: '美食', icon: '🍔', color: '#FF9800' },
  { id: 'animal', name: '动物', icon: '🐱', color: '#4CAF50' },
  { id: 'travel', name: '旅行', icon: '✈️', color: '#00BCD4' },
  { id: 'sports', name: '运动', icon: '⚽', color: '#795548' },
  { id: 'technology', name: '科技', icon: '🔬', color: '#607D8B' }
];

// 笑话长度选项
const JOKE_LENGTHS = [
  { id: 'short', name: '短笑话', desc: '一句话笑话' },
  { id: 'medium', name: '中等', desc: '几句话的小故事' },
  { id: 'long', name: '长笑话', desc: '完整的笑话故事' }
];

// 生成温度选项
const TEMPERATURE_OPTIONS = [
  { value: 0.3, name: '保守', desc: '更加稳定和可预测' },
  { value: 0.7, name: '平衡', desc: '创意和稳定的平衡' },
  { value: 1.0, name: '创意', desc: '更加有创意和随机' },
  { value: 1.5, name: '疯狂', desc: '非常有创意，可能很奇怪' }
];

// 分享平台
const SHARE_PLATFORMS = [
  { id: 'wechat', name: '微信好友', icon: 'wechat' },
  { id: 'timeline', name: '朋友圈', icon: 'timeline' },
  { id: 'qq', name: 'QQ', icon: 'qq' },
  { id: 'weibo', name: '微博', icon: 'weibo' },
  { id: 'copy', name: '复制链接', icon: 'copy' }
];

// API错误码
const ERROR_CODES = {
  SUCCESS: 200,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  VALIDATION_ERROR: 422,
  RATE_LIMIT: 429,
  INTERNAL_ERROR: 500
};

// 错误消息
const ERROR_MESSAGES = {
  [ERROR_CODES.BAD_REQUEST]: '请求参数错误',
  [ERROR_CODES.UNAUTHORIZED]: '未授权访问',
  [ERROR_CODES.FORBIDDEN]: '禁止访问',
  [ERROR_CODES.NOT_FOUND]: '资源不存在',
  [ERROR_CODES.VALIDATION_ERROR]: '数据验证失败',
  [ERROR_CODES.RATE_LIMIT]: '请求过于频繁，请稍后再试',
  [ERROR_CODES.INTERNAL_ERROR]: '服务器内部错误'
};

// 存储键名
const STORAGE_KEYS = {
  USER_INFO: 'userInfo',
  JOKE_HISTORY: 'jokeHistory',
  FAVORITE_JOKES: 'favoriteJokes',
  USER_PREFERENCES: 'userPreferences',
  LAST_CATEGORY: 'lastCategory',
  GENERATION_COUNT: 'generationCount',
  SHARE_COUNT: 'shareCount',
  FAVORITE_COUNT: 'favoriteCount',
  GENERATED_JOKES: 'generatedJokes',
  SHARED_JOKES: 'sharedJokes',
  FIRST_USE_TIME: 'firstUseTime',
  FEEDBACK_LIST: 'feedbackList',
  FAVORITES: 'favorites'
};

// 用户偏好默认值
const DEFAULT_PREFERENCES = {
  category: 'programmer',
  length: 'medium',
  temperature: 0.7,
  autoShare: false,
  vibration: true,
  sound: true
};

// 动画配置
const ANIMATION_CONFIG = {
  DURATION: 300,
  TIMING_FUNCTION: 'ease-in-out'
};

// 页面配置
const PAGE_CONFIG = {
  JOKE_LIST_PAGE_SIZE: 10,
  HISTORY_PAGE_SIZE: 20,
  MAX_HISTORY_COUNT: 100,
  MAX_FAVORITE_COUNT: 50
};

// 笑话标签
const JOKE_TAGS = {
  programmer: ['编程', '代码', '程序员', '技术', '开发', 'Bug', '算法'],
  daily: ['生活', '家庭', '朋友', '邻居', '购物', '做饭', '清洁'],
  work: ['上班', '老板', '同事', '会议', '加班', '升职', '辞职'],
  love: ['恋爱', '约会', '情侣', '表白', '分手', '结婚', '单身'],
  student: ['学习', '考试', '老师', '同学', '作业', '毕业', '校园'],
  food: ['美食', '餐厅', '做菜', '减肥', '零食', '饮料', '厨师'],
  animal: ['宠物', '猫咪', '狗狗', '动物园', '野生动物', '鸟类', '鱼类'],
  travel: ['旅游', '景点', '酒店', '飞机', '火车', '自驾', '导游'],
  sports: ['运动', '健身', '足球', '篮球', '跑步', '游泳', '比赛'],
  technology: ['科技', '手机', '电脑', '互联网', '人工智能', '机器人', '未来']
};

// 表情符号
const EMOJIS = {
  laugh: ['😂', '🤣', '😆', '😄', '😃', '😀', '😊'],
  love: ['❤️', '💕', '💖', '💗', '💝', '💘', '💞'],
  surprise: ['😮', '😯', '😲', '🤯', '😱', '🙀', '😵'],
  thinking: ['🤔', '💭', '🧐', '🤨', '😏', '🙄', '😑'],
  celebration: ['🎉', '🎊', '🥳', '🎈', '🎁', '🏆', '🌟']
};

// 颜色主题
const COLORS = {
  primary: '#4A90E2',
  secondary: '#07C160',
  accent: '#FF6B6B',
  warning: '#FF9800',
  error: '#F44336',
  success: '#4CAF50',
  info: '#2196F3',
  text: {
    primary: '#333333',
    secondary: '#666666',
    disabled: '#999999',
    white: '#FFFFFF'
  },
  background: {
    primary: '#FFFFFF',
    secondary: '#F5F5F5',
    disabled: '#EEEEEE'
  },
  border: {
    light: '#E0E0E0',
    medium: '#CCCCCC',
    dark: '#999999'
  }
};

// 字体大小
const FONT_SIZES = {
  xs: '20rpx',
  sm: '24rpx',
  base: '28rpx',
  lg: '32rpx',
  xl: '36rpx',
  '2xl': '40rpx',
  '3xl': '48rpx',
  '4xl': '56rpx'
};

// 间距
const SPACING = {
  xs: '8rpx',
  sm: '16rpx',
  base: '24rpx',
  lg: '32rpx',
  xl: '48rpx',
  '2xl': '64rpx',
  '3xl': '96rpx'
};

// 圆角
const BORDER_RADIUS = {
  sm: '8rpx',
  base: '16rpx',
  lg: '24rpx',
  xl: '32rpx',
  full: '50%'
};

// 阴影
const SHADOWS = {
  sm: '0 2rpx 8rpx rgba(0,0,0,0.1)',
  base: '0 4rpx 16rpx rgba(0,0,0,0.1)',
  lg: '0 8rpx 32rpx rgba(0,0,0,0.15)',
  xl: '0 16rpx 64rpx rgba(0,0,0,0.2)'
};

module.exports = {
  JOKE_CATEGORIES,
  JOKE_LENGTHS,
  TEMPERATURE_OPTIONS,
  SHARE_PLATFORMS,
  ERROR_CODES,
  ERROR_MESSAGES,
  STORAGE_KEYS,
  DEFAULT_PREFERENCES,
  ANIMATION_CONFIG,
  PAGE_CONFIG,
  JOKE_TAGS,
  EMOJIS,
  COLORS,
  FONT_SIZES,
  SPACING,
  BORDER_RADIUS,
  SHADOWS
};