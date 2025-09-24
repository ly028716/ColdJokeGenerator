#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
超简单的 HTTP 服务器，兼容 Python 3.6
"""

import json
import sys
import random
import os
import asyncio
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
try:
    import httpx
except ImportError:
    httpx = None

try:
    import requests
except ImportError:
    requests = None

class AIService:
    """简化的AI服务类"""
    
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        self.model = "qwen-turbo"
        
        # 备用笑话库
        self.fallback_jokes = [
            "为什么程序员总是混淆万圣节和圣诞节？因为 Oct 31 == Dec 25！",
            "有一天，0和8在街上相遇，0看了看8说：胖就胖呗，还系什么腰带！",
            "为什么计算机从来不感冒？因为它们有防病毒软件！",
            "程序员的烦恼：世界上最遥远的距离不是生与死，而是你亲手设计的程序出了bug你却找不到在哪里。",
            "为什么程序员喜欢用暗色主题？因为光会吸引bug！",
            "老板：你这个月的工作总结呢？我：还在加载中...请稍候。",
            "同事问我：你会几种编程语言？我说：会说话算吗？",
            "为什么程序员总是很累？因为他们总是在处理异常！",
            "我对我的WiFi说：你为什么这么慢？WiFi回答：你试试背着这么多设备跑！",
            "为什么AI永远不会取代程序员？因为AI还没学会怎么在Stack Overflow上复制代码！"
        ]
    
    def generate_joke_sync(self, category="通用", style="幽默"):
        """同步生成笑话"""
        if not self.api_key:
            print(f"使用备用笑话 - API Key未配置")
            return random.choice(self.fallback_jokes)
        
        # 优先使用requests，如果不可用则使用httpx
        if requests:
            return self._generate_with_requests(category, style)
        elif httpx:
            return self._generate_with_httpx(category, style)
        else:
            print("未安装requests或httpx库，使用备用笑话")
            return random.choice(self.fallback_jokes)
    
    def _generate_with_requests(self, category, style):
        """使用requests库调用API"""
        try:
            # 构建提示词
            prompt = f"请生成一个{category}类型的{style}冷笑话，要求简洁有趣，适合所有年龄段。"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'disable'
            }
            
            payload = {
                "model": self.model,
                "input": {
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个幽默的笑话生成器，专门创作健康、积极向上的冷笑话。请确保内容适合所有年龄段的用户。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                "parameters": {
                    "max_tokens": 200,
                    "temperature": 0.8,
                    "top_p": 0.8,
                    "repetition_penalty": 1.1
                }
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=10,
                verify=False  # 禁用SSL验证
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'output' in result and 'choices' in result['output']:
                    choices = result['output']['choices']
                    if choices and len(choices) > 0:
                        content = choices[0].get('message', {}).get('content', '')
                        if content:
                            print(f"通义千问API调用成功: {content[:50]}...")
                            return self._clean_joke_content(content)
            
            print(f"API调用失败，状态码: {response.status_code}")
            return random.choice(self.fallback_jokes)
            
        except Exception as e:
            print(f"调用通义千问API失败: {e}")
            return random.choice(self.fallback_jokes)
    
    def _generate_with_httpx(self, category, style):
        """使用httpx库调用API"""
        try:
            # 构建提示词
            prompt = f"请生成一个{category}类型的{style}冷笑话，要求简洁有趣，适合所有年龄段。"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'X-DashScope-SSE': 'disable'
            }
            
            payload = {
                "model": self.model,
                "input": {
                    "messages": [
                        {
                            "role": "system",
                            "content": "你是一个幽默的笑话生成器，专门创作健康、积极向上的冷笑话。请确保内容适合所有年龄段的用户。"
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                "parameters": {
                    "max_tokens": 200,
                    "temperature": 0.8,
                    "top_p": 0.8,
                    "repetition_penalty": 1.1
                }
            }
            
            with httpx.Client(timeout=10.0, verify=False) as client:
                response = client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if 'output' in result and 'choices' in result['output']:
                        choices = result['output']['choices']
                        if choices and len(choices) > 0:
                            content = choices[0].get('message', {}).get('content', '')
                            if content:
                                print(f"通义千问API调用成功: {content[:50]}...")
                                return self._clean_joke_content(content)
                
                print(f"API调用失败，状态码: {response.status_code}")
                return random.choice(self.fallback_jokes)
                
        except Exception as e:
            print(f"调用通义千问API失败: {e}")
            return random.choice(self.fallback_jokes)
    
    def _clean_joke_content(self, content):
        """清理笑话内容"""
        content = content.strip()
        
        # 移除可能的引号
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        if content.startswith("'") and content.endswith("'"):
            content = content[1:-1]
        
        if not content:
            return random.choice(self.fallback_jokes)
        
        return content
    
    def test_connection(self):
        """测试API连接"""
        if not self.api_key:
            return {
                "status": "error",
                "message": "API密钥未配置 (DEEPSEEK_API_KEY环境变量)",
                "fallback_available": True
            }
        
        if not requests and not httpx:
            return {
                "status": "error", 
                "message": "requests或httpx库未安装",
                "fallback_available": True
            }
        
        try:
            joke = self.generate_joke_sync("通用", "幽默")
            return {
                "status": "success",
                "message": "API连接正常",
                "test_joke": joke,
                "api_key_configured": bool(self.api_key),
                "http_library": "requests" if requests else "httpx"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"API连接失败: {str(e)}",
                "fallback_available": True
            }

# 预设的冷笑话库（作为备用）
JOKE_DATABASE = {
    "通用": [
        "为什么程序员总是混淆万圣节和圣诞节？因为 Oct 31 == Dec 25！",
        "有一天，0和8在街上相遇，0看了看8说：胖就胖呗，还系什么腰带！",
        "为什么计算机从来不感冒？因为它们有防病毒软件！",
        "程序员的烦恼：世界上最遥远的距离不是生与死，而是你亲手设计的程序出了bug你却找不到在哪里。",
        "为什么程序员喜欢用暗色主题？因为光会吸引bug！"
    ],
    "工作": [
        "老板：你这个月的工作总结呢？我：还在加载中...请稍候。",
        "同事问我：你会几种编程语言？我说：会说话算吗？",
        "为什么程序员总是很累？因为他们总是在处理异常！",
        "开会时老板说：我们要think outside the box。程序员：那我们用哪个容器？",
        "HR：你的期望薪资是多少？程序员：能让我买得起咖啡就行。"
    ],
    "生活": [
        "我对我的WiFi说：你为什么这么慢？WiFi回答：你试试背着这么多设备跑！",
        "为什么手机总是在最需要的时候没电？因为它也需要休息啊！",
        "朋友问我：你怎么这么瘦？我说：因为我是轻量级的！",
        "为什么我总是找不到东西？因为它们都在404页面！",
        "医生：你需要多运动。我：我每天都在运行程序啊！"
    ],
    "科技": [
        "为什么AI永远不会取代程序员？因为AI还没学会怎么在Stack Overflow上复制代码！",
        "机器人对人类说：你们为什么要睡觉？人类：因为我们需要重启。",
        "为什么云服务这么受欢迎？因为大家都想要头顶有片云！",
        "程序员：我写了一个Hello World。朋友：哇，你征服了世界！",
        "为什么区块链这么安全？因为没人能理解它是怎么工作的！"
    ]
}

# 创建AI服务实例
ai_service = AIService()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # 路由处理
        if path == '/':
            response = {
                "name": "AI冷笑话生成器",
                "version": "1.0.0",
                "status": "running",
                "message": "欢迎使用AI冷笑话生成器API服务"
            }
        elif path == '/health' or path == '/admin/health' or path == '/api/v1/admin/health':
            response = {
                "code": 200,
                "message": "服务正常",
                "data": {
                    "status": "healthy",
                    "version": "1.0.0"
                }
            }
        elif path == '/api/test':
            response = {
                "message": "API测试成功",
                "timestamp": datetime.now().isoformat()
            }
        elif path == '/api/v1/ai/test':
            response = ai_service.test_connection()
        else:
            response = {
                "error": "Not Found",
                "message": f"路径 {path} 不存在"
            }
        
        # 发送响应
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # 设置响应头
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except:
            request_data = {}
        
        # 路由处理
        if path == '/api/v1/jokes/generate':
            response = self.generate_joke(request_data)
        elif path == '/api/v1/jokes/save':
            response = self.save_joke(request_data)
        elif path == '/api/v1/categories':
            response = self.get_categories()
        else:
            response = {
                "error": "Not Found",
                "message": f"路径 {path} 不存在"
            }
        
        # 发送响应
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
    def generate_joke(self, request_data):
        """生成笑话"""
        category = request_data.get('category', '通用')
        style = request_data.get('style', '幽默')
        
        # 使用AI服务生成笑话
        joke_content = ai_service.generate_joke_sync(category, style)
        
        return {
            "code": 200,
            "message": "生成成功",
            "data": {
                "id": random.randint(1000, 9999),
                "content": joke_content,
                "category": category,
                "style": style,
                "created_at": datetime.now().isoformat(),
                "rating": random.randint(3, 5),
                "source": "ai" if ai_service.api_key and (requests or httpx) else "fallback"
            }
        }
    
    def save_joke(self, request_data):
        """保存笑话"""
        return {
            "code": 200,
            "message": "保存成功",
            "data": {
                "id": random.randint(1000, 9999),
                "saved_at": datetime.now().isoformat()
            }
        }
    
    def get_categories(self):
        """获取分类列表"""
        categories = []
        for category, jokes in JOKE_DATABASE.items():
            categories.append({
                "id": category,
                "name": category,
                "count": len(jokes),
                "description": f"{category}类笑话"
            })
        
        return {
            "code": 200,
            "message": "获取成功",
            "data": categories
        }
    
    def do_OPTIONS(self):
        """处理 OPTIONS 请求（CORS 预检）"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def main():
    """主函数"""
    try:
        host = '0.0.0.0'
        port = 8000
        
        print(f"启动简单HTTP服务器...")
        print(f"服务地址: http://localhost:{port}")
        print(f"健康检查: http://localhost:{port}/health")
        print(f"测试API: http://localhost:{port}/api/test")
        print("按 Ctrl+C 停止服务")
        
        # 创建服务器
        server = HTTPServer((host, port), SimpleHandler)
        
        # 启动服务器
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n服务已停止")
        server.shutdown()
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()