"""
AI服务测试
"""
import pytest
from unittest.mock import AsyncMock, patch

from app.services.ai_service import AIService


class TestAIService:
    """AI服务测试类"""
    
    @pytest.fixture
    def ai_service(self):
        """AI服务fixture"""
        return AIService()
    
    def test_fallback_joke(self, ai_service):
        """测试备用笑话"""
        joke = ai_service._get_fallback_joke()
        
        assert isinstance(joke, str)
        assert len(joke) > 0
        assert joke in ai_service.fallback_jokes
    
    def test_clean_joke_content(self, ai_service):
        """测试清理笑话内容"""
        # 测试带引号的内容
        content1 = '"这是一个笑话"'
        cleaned1 = ai_service._clean_joke_content(content1)
        assert cleaned1 == "这是一个笑话"
        
        # 测试带单引号的内容
        content2 = "'这是另一个笑话'"
        cleaned2 = ai_service._clean_joke_content(content2)
        assert cleaned2 == "这是另一个笑话"
        
        # 测试空内容
        content3 = ""
        cleaned3 = ai_service._clean_joke_content(content3)
        assert cleaned3 in ai_service.fallback_jokes
        
        # 测试正常内容
        content4 = "这是一个正常的笑话"
        cleaned4 = ai_service._clean_joke_content(content4)
        assert cleaned4 == "这是一个正常的笑话"
    
    @pytest.mark.asyncio
    async def test_generate_joke_without_api_key(self, ai_service):
        """测试没有API密钥时生成笑话"""
        # 模拟没有API密钥的情况
        ai_service.api_key = None
        
        joke = await ai_service.generate_joke("生成一个笑话")
        
        assert isinstance(joke, str)
        assert len(joke) > 0
        assert joke in ai_service.fallback_jokes
    
    @pytest.mark.asyncio
    async def test_api_connection_test_without_key(self, ai_service):
        """测试没有API密钥时的连接测试"""
        ai_service.api_key = None
        
        result = await ai_service.test_api_connection()
        
        assert result["status"] == "error"
        assert "API密钥未配置" in result["message"]
        assert result["fallback_available"] == True
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_generate_joke_with_mock_api(self, mock_post, ai_service):
        """测试使用模拟API生成笑话"""
        # 设置API密钥
        ai_service.api_key = "test_api_key"
        
        # 模拟API响应
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "output": {
                "choices": [
                    {
                        "message": {
                            "content": "这是一个AI生成的笑话"
                        }
                    }
                ]
            }
        }
        mock_post.return_value = mock_response
        
        joke = await ai_service.generate_joke("生成一个笑话")
        
        assert joke == "这是一个AI生成的笑话"
        mock_post.assert_called_once()
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_generate_joke_api_error(self, mock_post, ai_service):
        """测试API错误时的处理"""
        # 设置API密钥
        ai_service.api_key = "test_api_key"
        
        # 模拟API错误响应
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        joke = await ai_service.generate_joke("生成一个笑话")
        
        # 应该返回备用笑话
        assert isinstance(joke, str)
        assert len(joke) > 0
        assert joke in ai_service.fallback_jokes
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_generate_joke_timeout(self, mock_post, ai_service):
        """测试API超时处理"""
        import httpx
        
        # 设置API密钥
        ai_service.api_key = "test_api_key"
        
        # 模拟超时异常
        mock_post.side_effect = httpx.TimeoutException("Request timeout")
        
        joke = await ai_service.generate_joke("生成一个笑话")
        
        # 应该返回备用笑话
        assert isinstance(joke, str)
        assert len(joke) > 0
        assert joke in ai_service.fallback_jokes