"""
AI服务 - 阿里千问API集成
"""
import json
import random
import asyncio
from typing import Optional, Dict, Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import JokeGenerationException, APIKeyException

logger = get_logger(__name__)


class AIService:
    """AI服务类"""
    
    def __init__(self):
        self.api_key = settings.QWEN_API_KEY
        self.api_url = settings.QWEN_API_URL
        self.model = settings.QWEN_MODEL
        
        # 备用笑话库
        self.fallback_jokes = [
            "为什么程序员喜欢冷笑话？因为它们像代码一样冷！",
            "有一天，一个程序员对他的妻子说：'去超市买一斤苹果，如果有鸡蛋的话，买十个。'程序员回来了，手里拿着十斤苹果。妻子问：'你怎么买了这么多苹果？'程序员：'因为他们有鸡蛋。'",
            "为什么程序员总是分不清万圣节和圣诞节？因为 Oct 31 == Dec 25！",
            "程序员的三大美德：懒惰、急躁和傲慢。懒惰使你写出高效的程序，急躁使你写出快速的程序，傲慢使你写出别人不敢质疑的程序。",
            "为什么程序员讨厌大自然？因为大自然有太多的bugs。",
            "一个程序员走进一家酒吧，要了1024杯啤酒。酒保问：'为什么要这么多？'程序员说：'因为1024是2的10次方，很完美的数字！'",
            "为什么程序员总是搞混圣诞节和万圣节？因为Dec 25 = Oct 31！",
            "程序员最讨厌的事情是什么？写文档。第二讨厌的是什么？别人不写文档。",
            "为什么程序员喜欢黑暗？因为光会产生bug！",
            "一个程序员的妻子让他去买牛奶，如果有鸡蛋的话买一打。他回来时买了一打牛奶。妻子问为什么，他说：'因为有鸡蛋。'"
        ]
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_joke(
        self,
        prompt: str,
        temperature: float = 0.8,
        max_tokens: int = 200
    ) -> str:
        """生成笑话"""
        
        # 如果没有API密钥，使用备用笑话
        if not self.api_key or self.api_key == "your_qwen_api_key_here":
            logger.warning("未配置阿里千问API密钥，使用备用笑话")
            return self._get_fallback_joke()
        
        try:
            return await self._call_qwen_api(prompt, temperature, max_tokens)
        except Exception as e:
            logger.error(f"调用阿里千问API失败: {e}")
            logger.info("使用备用笑话")
            return self._get_fallback_joke()
    
    async def _call_qwen_api(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """调用阿里千问API"""
        
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
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.8,
                "repetition_penalty": 1.1
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 401:
                    raise APIKeyException("API密钥无效")
                
                if response.status_code != 200:
                    raise JokeGenerationException(f"API调用失败，状态码: {response.status_code}")
                
                result = response.json()
                
                # 解析响应
                if 'output' in result and 'choices' in result['output']:
                    choices = result['output']['choices']
                    if choices and len(choices) > 0:
                        content = choices[0].get('message', {}).get('content', '')
                        if content:
                            return self._clean_joke_content(content)
                
                # 如果解析失败，抛出异常
                raise JokeGenerationException("API响应格式异常")
                
            except httpx.TimeoutException:
                raise JokeGenerationException("API调用超时")
            except httpx.RequestError as e:
                raise JokeGenerationException(f"API请求错误: {str(e)}")
    
    def _get_fallback_joke(self) -> str:
        """获取备用笑话"""
        return random.choice(self.fallback_jokes)
    
    def _clean_joke_content(self, content: str) -> str:
        """清理笑话内容"""
        # 移除多余的空白字符
        content = content.strip()
        
        # 移除可能的引号
        if content.startswith('"') and content.endswith('"'):
            content = content[1:-1]
        if content.startswith("'") and content.endswith("'"):
            content = content[1:-1]
        
        # 确保内容不为空
        if not content:
            return self._get_fallback_joke()
        
        return content
    
    async def test_api_connection(self) -> Dict[str, Any]:
        """测试API连接"""
        if not self.api_key or self.api_key == "your_qwen_api_key_here":
            return {
                "status": "error",
                "message": "API密钥未配置",
                "fallback_available": True
            }
        
        try:
            joke = await self.generate_joke("请生成一个简单的测试笑话")
            return {
                "status": "success",
                "message": "API连接正常",
                "test_joke": joke
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"API连接失败: {str(e)}",
                "fallback_available": True
            }