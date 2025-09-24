# AI冷笑话生成器 API 文档

## 📋 概述

AI冷笑话生成器提供了一套完整的RESTful API，支持笑话生成、用户管理、分享统计等功能。

## 🔗 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: 暂无（后续可添加JWT认证）
- **数据格式**: JSON
- **字符编码**: UTF-8

## 📊 统一响应格式

所有API响应都遵循统一格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {},
    "request_id": "uuid-string"
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，200表示成功 |
| message | string | 响应消息 |
| data | any | 响应数据，可为对象、数组或null |
| request_id | string | 请求唯一标识符 |

### 常见状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 422 | 数据验证失败 |
| 429 | 请求过于频繁 |
| 500 | 服务器内部错误 |

## 🎭 笑话相关接口

### 1. 生成单个笑话

**接口地址**: `POST /jokes/generate`

**请求参数**:
```json
{
    "category": "程序员",
    "tags": ["编程", "幽默"],
    "length": "medium",
    "temperature": 0.8,
    "custom_prompt": "关于Python的笑话"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 否 | 笑话分类 |
| tags | array | 否 | 标签列表 |
| length | string | 否 | 长度偏好：short/medium/long |
| temperature | float | 否 | 生成温度，0.1-2.0 |
| custom_prompt | string | 否 | 自定义提示词 |

**响应示例**:
```json
{
    "code": 200,
    "message": "笑话生成成功",
    "data": {
        "id": 1,
        "content": "为什么程序员喜欢冷笑话？因为它们像代码一样冷！",
        "category": "程序员",
        "tags": "编程,幽默",
        "view_count": 0,
        "share_count": 0,
        "like_count": 0,
        "is_featured": false,
        "is_public": true,
        "created_at": "2023-12-22T14:30:00Z",
        "updated_at": "2023-12-22T14:30:00Z"
    },
    "request_id": "uuid-string"
}
```

**限流规则**: 10次/分钟

### 2. 批量生成笑话

**接口地址**: `POST /jokes/batch`

**请求参数**:
```json
{
    "count": 3,
    "category": "程序员",
    "tags": ["编程"],
    "length": "medium",
    "temperature": 0.8
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| count | int | 是 | 生成数量，1-10 |
| category | string | 否 | 笑话分类 |
| tags | array | 否 | 标签列表 |
| length | string | 否 | 长度偏好 |
| temperature | float | 否 | 生成温度 |

**响应示例**:
```json
{
    "code": 200,
    "message": "成功生成3个笑话",
    "data": [
        {
            "id": 1,
            "content": "笑话内容1",
            // ... 其他字段
        },
        {
            "id": 2,
            "content": "笑话内容2",
            // ... 其他字段
        }
    ],
    "request_id": "uuid-string"
}
```

**限流规则**: 5次/分钟

### 3. 按分类生成笑话

**接口地址**: `GET /jokes/category/{category}`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| category | string | 是 | 笑话分类 |

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| temperature | float | 否 | 生成温度，默认0.8 |

**限流规则**: 20次/分钟

### 4. 获取笑话列表

**接口地址**: `GET /jokes/`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| size | int | 否 | 每页数量，默认10，最大50 |
| category | string | 否 | 分类筛选 |
| is_featured | bool | 否 | 是否精选 |

**响应示例**:
```json
{
    "code": 200,
    "message": "获取笑话列表成功",
    "data": {
        "items": [
            {
                "id": 1,
                "content": "笑话内容",
                // ... 其他字段
            }
        ],
        "total": 100,
        "page": 1,
        "size": 10,
        "pages": 10
    },
    "request_id": "uuid-string"
}
```

### 5. 获取单个笑话

**接口地址**: `GET /jokes/{joke_id}`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| joke_id | int | 是 | 笑话ID |

**响应示例**:
```json
{
    "code": 200,
    "message": "获取笑话成功",
    "data": {
        "id": 1,
        "content": "笑话内容",
        "category": "程序员",
        "view_count": 10,
        // ... 其他字段
    },
    "request_id": "uuid-string"
}
```

### 6. 收藏笑话

**接口地址**: `POST /jokes/{joke_id}/favorite`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| joke_id | int | 是 | 笑话ID |

**响应示例**:
```json
{
    "code": 200,
    "message": "收藏成功",
    "data": {
        "favorited": true
    },
    "request_id": "uuid-string"
}
```

**限流规则**: 30次/分钟

### 7. 获取用户笑话历史

**接口地址**: `GET /jokes/user/{user_id}/history`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| size | int | 否 | 每页数量，默认10 |

### 8. 分享笑话

**接口地址**: `POST /jokes/share`

**请求参数**:
```json
{
    "joke_id": 1,
    "share_to": "wechat",
    "share_title": "分享一个笑话",
    "share_desc": "这个笑话很有趣",
    "device_info": "iPhone 12"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| joke_id | int | 是 | 笑话ID |
| share_to | string | 是 | 分享平台 |
| share_title | string | 否 | 分享标题 |
| share_desc | string | 否 | 分享描述 |
| device_info | string | 否 | 设备信息 |

**响应示例**:
```json
{
    "code": 200,
    "message": "分享记录成功",
    "data": {
        "id": 1,
        "joke_id": 1,
        "share_to": "wechat",
        "share_url": "/share/joke/1",
        "click_count": 0,
        "created_at": "2023-12-22T14:30:00Z"
    },
    "request_id": "uuid-string"
}
```

**限流规则**: 20次/分钟

### 9. 获取分享统计

**接口地址**: `GET /jokes/share/stats`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| days | int | 否 | 统计天数，默认7，最大30 |

**响应示例**:
```json
{
    "code": 200,
    "message": "获取分享统计成功",
    "data": {
        "total_shares": 100,
        "platform_stats": {
            "wechat": 60,
            "weibo": 25,
            "qq": 15
        },
        "recent_shares": [
            {
                "id": 1,
                "joke_id": 1,
                "share_to": "wechat",
                "created_at": "2023-12-22T14:30:00Z"
            }
        ],
        "top_shared_jokes": [
            {
                "id": 1,
                "content": "最受欢迎的笑话",
                "share_count": 50
            }
        ]
    },
    "request_id": "uuid-string"
}
```

## 👤 用户相关接口

### 1. 创建用户

**接口地址**: `POST /users/`

**请求参数**:
```json
{
    "openid": "wx_openid_123",
    "nickname": "用户昵称",
    "avatar_url": "https://example.com/avatar.jpg",
    "gender": 1,
    "city": "北京",
    "province": "北京",
    "country": "中国",
    "language": "zh_CN"
}
```

**参数说明**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openid | string | 是 | 微信openid |
| nickname | string | 否 | 用户昵称 |
| avatar_url | string | 否 | 头像URL |
| gender | int | 否 | 性别：0-未知，1-男，2-女 |
| city | string | 否 | 城市 |
| province | string | 否 | 省份 |
| country | string | 否 | 国家 |
| language | string | 否 | 语言，默认zh_CN |

**响应示例**:
```json
{
    "code": 200,
    "message": "用户创建成功",
    "data": {
        "id": 1,
        "openid": "wx_openid_123",
        "nickname": "用户昵称",
        "avatar_url": "https://example.com/avatar.jpg",
        "gender": 1,
        "city": "北京",
        "province": "北京",
        "country": "中国",
        "language": "zh_CN",
        "is_active": true,
        "is_banned": false,
        "total_generated": 0,
        "total_shared": 0,
        "created_at": "2023-12-22T14:30:00Z",
        "updated_at": "2023-12-22T14:30:00Z",
        "last_login_at": null
    },
    "request_id": "uuid-string"
}
```

### 2. 获取用户信息

**接口地址**: `GET /users/{user_id}`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | int | 是 | 用户ID |

### 3. 通过openid获取用户信息

**接口地址**: `GET /users/openid/{openid}`

**路径参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| openid | string | 是 | 微信openid |

### 4. 更新用户信息

**接口地址**: `PUT /users/{user_id}`

**请求参数**:
```json
{
    "nickname": "新昵称",
    "avatar_url": "https://example.com/new_avatar.jpg",
    "city": "上海"
}
```

### 5. 用户登录

**接口地址**: `POST /users/{user_id}/login`

**限流规则**: 10次/分钟

### 6. 获取用户列表

**接口地址**: `GET /users/`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| page | int | 否 | 页码，默认1 |
| size | int | 否 | 每页数量，默认10 |
| is_active | bool | 否 | 是否激活 |

### 7. 获取用户统计

**接口地址**: `GET /users/stats/overview`

**响应示例**:
```json
{
    "code": 200,
    "message": "获取用户统计成功",
    "data": {
        "total_users": 1000,
        "active_users": 800,
        "new_users_today": 10,
        "top_generators": [
            {
                "id": 1,
                "nickname": "用户1",
                "total_generated": 100
            }
        ],
        "top_sharers": [
            {
                "id": 2,
                "nickname": "用户2",
                "total_shared": 50
            }
        ]
    },
    "request_id": "uuid-string"
}
```

## 🔧 管理员接口

### 1. 系统健康检查

**接口地址**: `GET /admin/health`

**响应示例**:
```json
{
    "code": 200,
    "message": "系统健康检查完成",
    "data": {
        "database": {
            "status": "healthy"
        },
        "ai_service": {
            "status": "success",
            "message": "API连接正常"
        },
        "cache": {
            "enabled": true,
            "connected_clients": 1,
            "used_memory": "1.2MB"
        },
        "overall": "healthy"
    },
    "request_id": "uuid-string"
}
```

### 2. 清除缓存

**接口地址**: `POST /admin/cache/clear`

**查询参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pattern | string | 否 | 缓存模式，默认* |

### 3. 获取系统统计

**接口地址**: `GET /admin/stats`

**响应示例**:
```json
{
    "code": 200,
    "message": "获取系统统计成功",
    "data": {
        "users": {
            "total_users": 1000,
            "active_users": 800,
            "new_users_today": 10
        },
        "jokes": {
            "total": 5000,
            "featured": 100
        },
        "shares": {
            "total": 2000,
            "platforms": {
                "wechat": 1200,
                "weibo": 500,
                "qq": 300
            }
        },
        "cache": {
            "enabled": true,
            "keyspace_hits": 1000,
            "keyspace_misses": 100
        }
    },
    "request_id": "uuid-string"
}
```

## 🚨 错误处理

### 错误响应格式

```json
{
    "code": 400,
    "message": "请求参数错误",
    "data": {
        "errors": [
            {
                "field": "category",
                "message": "分类不能为空"
            }
        ]
    },
    "request_id": "uuid-string"
}
```

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求参数格式和类型 |
| 401 | 未授权访问 | 检查认证信息 |
| 404 | 资源不存在 | 检查资源ID是否正确 |
| 422 | 数据验证失败 | 检查请求数据是否符合要求 |
| 429 | 请求过于频繁 | 降低请求频率 |
| 500 | 服务器内部错误 | 联系技术支持 |

## 📝 使用示例

### JavaScript/Axios示例

```javascript
// 生成笑话
const generateJoke = async () => {
    try {
        const response = await axios.post('/api/v1/jokes/generate', {
            category: '程序员',
            temperature: 0.8
        });
        console.log(response.data.data.content);
    } catch (error) {
        console.error('生成笑话失败:', error.response.data.message);
    }
};

// 创建用户
const createUser = async (userData) => {
    try {
        const response = await axios.post('/api/v1/users/', userData);
        return response.data.data;
    } catch (error) {
        if (error.response.data.code === 400) {
            console.error('用户已存在');
        }
        throw error;
    }
};
```

### Python/Requests示例

```python
import requests

# 生成笑话
def generate_joke(category=None):
    url = 'http://localhost:8000/api/v1/jokes/generate'
    data = {'category': category} if category else {}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['data']['content']
    else:
        raise Exception(f"生成失败: {response.json()['message']}")

# 获取笑话列表
def get_jokes(page=1, size=10):
    url = f'http://localhost:8000/api/v1/jokes/?page={page}&size={size}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"获取失败: {response.json()['message']}")
```

## 🔄 版本更新

当前版本: v1.0.0

### 更新日志

- v1.0.0 (2023-12-22)
  - 初始版本发布
  - 支持笑话生成、用户管理、分享统计
  - 集成阿里千问API
  - 完整的错误处理和限流机制

## 📞 技术支持

如有API使用问题，请联系技术支持团队或查看项目文档。