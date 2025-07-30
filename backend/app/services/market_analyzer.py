import httpx
import asyncio
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import openai
from app.core.config import settings
from app.models.analysis import MarketTrends
import json
import re

class MarketAnalyzer:
    """市场趋势分析器"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.market_data_sources = [
            "https://www.statista.com",
            "https://www.grandviewresearch.com",
            "https://www.marketsandmarkets.com",
            "https://www.ibisworld.com"
        ]
    
    async def analyze(self, url: str) -> MarketTrends:
        """
        分析指定URL的市场趋势
        
        Args:
            url: 要分析的网址
            
        Returns:
            MarketTrends: 市场趋势分析结果
        """
        try:
            # 1. 提取网站内容和行业信息
            website_content = await self._extract_website_content(url)
            industry_info = await self._identify_industry(url, website_content)
            
            # 2. 获取市场数据
            market_data = await self._gather_market_data(industry_info)
            
            # 3. 使用AI分析市场趋势
            market_trends = await self._analyze_market_trends(website_content, industry_info, market_data)
            
            return market_trends
            
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
            
            return {
                "title": title,
                "description": description,
                "content": main_content[:5000],  # 限制内容长度
                "url": url
            }
    
    async def _identify_industry(self, url: str, content: Dict[str, Any]) -> Dict[str, Any]:
        """识别行业类别"""
        prompt = f"""
        基于以下网站信息，识别该网站所属的行业类别：
        
        URL: {url}
        标题: {content['title']}
        描述: {content['description']}
        内容摘要: {content['content'][:1000]}
        
        请返回JSON格式的行业信息，包含：
        - industry_name: 行业名称
        - industry_category: 行业分类
        - key_products: 主要产品/服务
        - target_market: 目标市场
        """
        
        response = await self._call_openai(prompt)
        return json.loads(response)
    
    async def _gather_market_data(self, industry_info: Dict[str, Any]) -> Dict[str, Any]:
        """收集市场数据"""
        # 这里可以集成第三方市场数据API
        # 目前返回模拟数据
        return {
            "market_size": {
                "current": "$50B",
                "forecast_2025": "$75B",
                "forecast_2030": "$120B"
            },
            "growth_rate": {
                "cagr_5_year": 8.5,
                "annual_growth": 12.3
            },
            "key_players": [
                "Company A", "Company B", "Company C"
            ],
            "market_segments": [
                {"name": "Enterprise", "share": 45},
                {"name": "SMB", "share": 35},
                {"name": "Consumer", "share": 20}
            ]
        }
    
    async def _analyze_market_trends(self, content: Dict[str, Any], industry_info: Dict[str, Any], market_data: Dict[str, Any]) -> MarketTrends:
        """使用AI分析市场趋势"""
        prompt = f"""
        基于以下信息，分析北美市场的市场趋势：
        
        行业信息: {json.dumps(industry_info, ensure_ascii=False)}
        市场数据: {json.dumps(market_data, ensure_ascii=False)}
        网站内容: {content['content'][:2000]}
        
        请提供详细的市场趋势分析，包括：
        1. 市场规模评估
        2. CAGR计算
        3. 关键市场驱动因素
        4. 增长预测
        5. 市场细分分析
        6. 行业趋势
        
        请以JSON格式返回结果。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return MarketTrends(
            market_size=analysis_data.get("market_size", {}),
            cagr=analysis_data.get("cagr", 0.0),
            key_drivers=analysis_data.get("key_drivers", []),
            growth_forecast=analysis_data.get("growth_forecast", {}),
            market_segments=analysis_data.get("market_segments", []),
            industry_trends=analysis_data.get("industry_trends", [])
        )
    
    async def _fallback_analysis(self, url: str) -> MarketTrends:
        """备用分析方案"""
        prompt = f"""
        基于URL {url}，分析该网站可能涉及的市场趋势。
        请提供合理的市场分析，包括市场规模、增长率、驱动因素等。
        以JSON格式返回。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return MarketTrends(
            market_size=analysis_data.get("market_size", {"current": "N/A"}),
            cagr=analysis_data.get("cagr", 0.0),
            key_drivers=analysis_data.get("key_drivers", []),
            growth_forecast=analysis_data.get("growth_forecast", {}),
            market_segments=analysis_data.get("market_segments", []),
            industry_trends=analysis_data.get("industry_trends", [])
        )
    
    async def _call_openai(self, prompt: str) -> str:
        """调用OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的市场分析师，擅长分析北美市场的趋势和机会。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            # 返回默认分析结果
            return json.dumps({
                "market_size": {"current": "需要进一步分析"},
                "cagr": 5.0,
                "key_drivers": ["技术创新", "市场需求增长"],
                "growth_forecast": {"2025": "稳定增长"},
                "market_segments": [{"name": "主要市场", "share": 100}],
                "industry_trends": ["数字化转型", "可持续发展"]
            }) 