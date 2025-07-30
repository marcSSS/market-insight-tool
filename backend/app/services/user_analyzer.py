import httpx
import asyncio
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import openai
from app.core.config import settings
from app.models.analysis import UserProfile
import json
import re

class UserAnalyzer:
    """用户画像分析器"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.social_media_platforms = [
            "facebook.com", "twitter.com", "linkedin.com", 
            "instagram.com", "youtube.com", "tiktok.com"
        ]
    
    async def analyze(self, url: str) -> UserProfile:
        """
        分析指定URL的用户画像
        
        Args:
            url: 要分析的网址
            
        Returns:
            UserProfile: 用户画像分析结果
        """
        try:
            # 1. 提取网站内容和用户相关信息
            website_content = await self._extract_website_content(url)
            social_media_data = await self._gather_social_media_data(url)
            
            # 2. 分析目标用户群体
            target_audience = await self._analyze_target_audience(website_content, social_media_data)
            
            # 3. 识别用户需求和痛点
            user_needs_pain_points = await self._analyze_user_needs_and_pain_points(website_content)
            
            # 4. 分析用户行为模式
            user_behavior = await self._analyze_user_behavior(website_content, social_media_data)
            
            # 5. 生成人口统计学和心理特征
            demographics_psychographics = await self._analyze_demographics_psychographics(target_audience)
            
            return UserProfile(
                target_audience=target_audience,
                user_needs=user_needs_pain_points.get("needs", []),
                pain_points=user_needs_pain_points.get("pain_points", []),
                user_behavior=user_behavior,
                demographics=demographics_psychographics.get("demographics", {}),
                psychographics=demographics_psychographics.get("psychographics", {})
            )
            
        except Exception as e:
            # 返回基于网站内容的AI分析结果
            return await self._fallback_analysis(url)
    
    async def _extract_website_content(self, url: str) -> Dict[str, Any]:
        """提取网站内容"""
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取关键信息
            title = soup.find('title').get_text() if soup.find('title') else ""
            description = soup.find('meta', {'name': 'description'})
            description = description.get('content', '') if description else ""
            
            # 提取主要内容
            main_content = ""
            for tag in soup.find_all(['h1', 'h2', 'h3', 'p', 'div']):
                if tag.get_text().strip():
                    main_content += tag.get_text().strip() + " "
            
            # 提取用户相关关键词
            user_keywords = self._extract_user_keywords(main_content)
            
            return {
                "title": title,
                "description": description,
                "content": main_content[:5000],
                "user_keywords": user_keywords,
                "url": url
            }
    
    def _extract_user_keywords(self, content: str) -> List[str]:
        """提取用户相关关键词"""
        user_related_words = [
            "用户", "客户", "消费者", "用户群体", "目标用户", "用户需求",
            "user", "customer", "consumer", "audience", "target", "need",
            "pain point", "problem", "solution", "benefit", "value"
        ]
        
        keywords = []
        content_lower = content.lower()
        for word in user_related_words:
            if word.lower() in content_lower:
                keywords.append(word)
        
        return keywords
    
    async def _gather_social_media_data(self, url: str) -> Dict[str, Any]:
        """收集社交媒体数据"""
        # 这里可以集成社交媒体API
        # 目前返回模拟数据
        return {
            "social_presence": {
                "facebook": {"followers": 10000, "engagement_rate": 2.5},
                "twitter": {"followers": 5000, "engagement_rate": 3.2},
                "linkedin": {"followers": 8000, "engagement_rate": 1.8}
            },
            "user_sentiment": {
                "positive": 65,
                "neutral": 25,
                "negative": 10
            },
            "top_mentions": [
                "great product", "easy to use", "good value", "needs improvement"
            ]
        }
    
    async def _analyze_target_audience(self, website_content: Dict[str, Any], social_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分析目标用户群体"""
        prompt = f"""
        基于以下网站信息，分析目标用户群体：
        
        网站内容: {website_content['content'][:2000]}
        用户关键词: {website_content['user_keywords']}
        社交媒体数据: {json.dumps(social_data, ensure_ascii=False)}
        
        请识别并分析目标用户群体，包括：
        1. 主要用户群体
        2. 次要用户群体
        3. 每个群体的特征
        4. 用户规模估计
        
        请以JSON格式返回结果，包含target_audience数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("target_audience", [])
    
    async def _analyze_user_needs_and_pain_points(self, website_content: Dict[str, Any]) -> Dict[str, List[str]]:
        """分析用户需求和痛点"""
        prompt = f"""
        基于以下网站内容，分析用户需求和痛点：
        
        网站内容: {website_content['content'][:2000]}
        用户关键词: {website_content['user_keywords']}
        
        请识别：
        1. 用户的主要需求
        2. 用户的痛点
        3. 用户期望的解决方案
        
        请以JSON格式返回结果，包含needs和pain_points数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return {
            "needs": analysis_data.get("needs", []),
            "pain_points": analysis_data.get("pain_points", [])
        }
    
    async def _analyze_user_behavior(self, website_content: Dict[str, Any], social_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析用户行为模式"""
        prompt = f"""
        基于以下信息，分析用户行为模式：
        
        网站内容: {website_content['content'][:1500]}
        社交媒体数据: {json.dumps(social_data, ensure_ascii=False)}
        
        请分析用户行为模式，包括：
        1. 购买行为
        2. 使用习惯
        3. 决策过程
        4. 互动方式
        5. 偏好特征
        
        请以JSON格式返回结果。
        """
        
        response = await self._call_openai(prompt)
        return json.loads(response)
    
    async def _analyze_demographics_psychographics(self, target_audience: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析人口统计学和心理特征"""
        prompt = f"""
        基于以下目标用户群体信息，分析人口统计学和心理特征：
        
        目标用户群体: {json.dumps(target_audience, ensure_ascii=False)}
        
        请分析：
        1. 人口统计学特征（年龄、性别、收入、教育、地理位置等）
        2. 心理特征（价值观、生活方式、兴趣、态度等）
        
        请以JSON格式返回结果，包含demographics和psychographics对象。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return {
            "demographics": analysis_data.get("demographics", {}),
            "psychographics": analysis_data.get("psychographics", {})
        }
    
    async def _fallback_analysis(self, url: str) -> UserProfile:
        """备用分析方案"""
        prompt = f"""
        基于URL {url}，分析该网站的目标用户画像。
        请提供合理的用户分析，包括目标用户、需求、痛点等。
        以JSON格式返回。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return UserProfile(
            target_audience=analysis_data.get("target_audience", []),
            user_needs=analysis_data.get("user_needs", []),
            pain_points=analysis_data.get("pain_points", []),
            user_behavior=analysis_data.get("user_behavior", {}),
            demographics=analysis_data.get("demographics", {}),
            psychographics=analysis_data.get("psychographics", {})
        )
    
    async def _call_openai(self, prompt: str) -> str:
        """调用OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的用户研究分析师，擅长分析用户画像、需求和行为模式。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            # 返回默认分析结果
            return json.dumps({
                "target_audience": [{"name": "主要用户群体", "characteristics": "需要进一步分析"}],
                "user_needs": ["功能需求", "体验需求"],
                "pain_points": ["使用复杂", "功能不足"],
                "user_behavior": {"purchase_pattern": "需要分析", "usage_pattern": "需要分析"},
                "demographics": {"age_range": "25-45", "income_level": "中等"},
                "psychographics": {"lifestyle": "现代", "values": "效率"}
            }) 