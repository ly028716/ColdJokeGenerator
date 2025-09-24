-- AI冷笑话生成器数据库初始化脚本

-- 设置数据库编码
SET client_encoding = 'UTF8';

-- 创建扩展 (如果需要)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 创建索引优化查询性能
-- 这些索引会在SQLAlchemy创建表后自动创建，这里仅作为参考

-- 用户表索引
-- CREATE INDEX IF NOT EXISTS idx_users_openid ON users(openid);
-- CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
-- CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);

-- 笑话表索引
-- CREATE INDEX IF NOT EXISTS idx_jokes_category ON jokes(category);
-- CREATE INDEX IF NOT EXISTS idx_jokes_created_at ON jokes(created_at);
-- CREATE INDEX IF NOT EXISTS idx_jokes_is_featured ON jokes(is_featured);
-- CREATE INDEX IF NOT EXISTS idx_jokes_is_public ON jokes(is_public);
-- CREATE INDEX IF NOT EXISTS idx_jokes_user_id ON jokes(user_id);

-- 分享记录表索引
-- CREATE INDEX IF NOT EXISTS idx_shares_joke_id ON shares(joke_id);
-- CREATE INDEX IF NOT EXISTS idx_shares_user_id ON shares(user_id);
-- CREATE INDEX IF NOT EXISTS idx_shares_created_at ON shares(created_at);
-- CREATE INDEX IF NOT EXISTS idx_shares_share_to ON shares(share_to);

-- 用户偏好表索引
-- CREATE INDEX IF NOT EXISTS idx_user_preferences_user_id ON user_preferences(user_id);

-- 插入初始数据 (可选)
-- INSERT INTO jokes (content, category, is_featured, is_public, created_at, updated_at) VALUES
-- ('为什么程序员喜欢冷笑话？因为它们像代码一样冷！', '程序员', true, true, NOW(), NOW()),
-- ('有一天，一个程序员对他的妻子说："去超市买一斤苹果，如果有鸡蛋的话，买十个。"程序员回来了，手里拿着十斤苹果。妻子问："你怎么买了这么多苹果？"程序员："因为他们有鸡蛋。"', '程序员', true, true, NOW(), NOW()),
-- ('为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！', '程序员', true, true, NOW(), NOW());

-- 数据库优化设置
-- ALTER DATABASE jokes_db SET timezone TO 'UTC';

COMMIT;