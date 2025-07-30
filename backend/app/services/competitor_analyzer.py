import httpx
import asyncio
from typing import Dict, Any, List
from bs4 import BeautifulSoup
import openai
from app.core.config import settings
from app.models.analysis import CompetitorAnalysis
import json
import re
from urllib.parse import urlparse

class CompetitorAnalyzer:
    """竞争分析器"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.competitor_detection_keywords = [
            "competitor", "alternative", "vs", "compare", "similar",
            "competition", "rival", "opponent", "challenger"
        ]
    
    async def analyze(self, url: str) -> CompetitorAnalysis:
        """
        分析指定URL的竞争环境
        
        Args:
            url: 要分析的网址
            
        Returns:
            CompetitorAnalysis: 竞争分析结果
        """
        try:
            # 1. 提取网站内容和行业信息
            website_content = await self._extract_website_content(url)
            industry_info = await self._identify_industry(url, website_content)
            
            # 2. 识别竞争对手
            competitors = await self._identify_competitors(website_content, industry_info)
            
            # 3. 分析竞争格局
            competitive_landscape = await self._analyze_competitive_landscape(competitors, industry_info)
            
            # 4. 产品对比分析
            product_comparison = await self._analyze_product_comparison(competitors, website_content)
            
            # 5. 营销策略分析
            marketing_strategies = await self._analyze_marketing_strategies(competitors)
            
            # 6. 竞争优势分析
            competitive_advantages = await self._analyze_competitive_advantages(website_content, competitors)
            
            # 7. 市场定位分析
            market_positioning = await self._analyze_market_positioning(website_content, competitors)
            
            return CompetitorAnalysis(
                competitors=competitors,
                competitive_landscape=competitive_landscape,
                product_comparison=product_comparison,
                marketing_strategies=marketing_strategies,
                competitive_advantages=competitive_advantages,
                market_positioning=market_positioning
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
            
            # 提取竞争对手相关关键词
            competitor_keywords = self._extract_competitor_keywords(main_content)
            
            return {
                "title": title,
                "description": description,
                "content": main_content[:5000],
                "competitor_keywords": competitor_keywords,
                "url": url
            }
    
    def _extract_competitor_keywords(self, content: str) -> List[str]:
        """提取竞争对手相关关键词"""
        keywords = []
        content_lower = content.lower()
        for word in self.competitor_detection_keywords:
            if word.lower() in content_lower:
                keywords.append(word)
        
        return keywords
    
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
        - market_players: 主要市场参与者
        """
        
        response = await self._call_openai(prompt)
        return json.loads(response)
    
    async def _identify_competitors(self, website_content: Dict[str, Any], industry_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """识别竞争对手"""
        prompt = f"""
        基于以下信息，识别主要竞争对手：
        
        网站内容: {website_content['content'][:2000]}
        行业信息: {json.dumps(industry_info, ensure_ascii=False)}
        竞争对手关键词: {website_content['competitor_keywords']}
        
        请识别并分析主要竞争对手，包括：
        1. 直接竞争对手
        2. 间接竞争对手
        3. 潜在竞争对手
        4. 每个竞争对手的基本信息
        
        请以JSON格式返回结果，包含competitors数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        # 补充竞争对手数据
        competitors = analysis_data.get("competitors", [])
        for competitor in competitors:
            competitor.update({
                "market_share": await self._estimate_market_share(competitor),
                "strengths": await self._analyze_competitor_strengths(competitor),
                "weaknesses": await self._analyze_competitor_weaknesses(competitor)
            })
        
        return competitors
    
    async def _analyze_competitive_landscape(self, competitors: List[Dict[str, Any]], industry_info: Dict[str, Any]) -> Dict[str, Any]:
        """分析竞争格局"""
        prompt = f"""
        基于以下竞争对手信息，分析竞争格局：
        
        竞争对手: {json.dumps(competitors, ensure_ascii=False)}
        行业信息: {json.dumps(industry_info, ensure_ascii=False)}
        
        请分析竞争格局，包括：
        1. 市场集中度
        2. 竞争强度
        3. 进入壁垒
        4. 替代品威胁
        5. 竞争策略类型
        
        请以JSON格式返回结果。
        """
        
        response = await self._call_openai(prompt)
        return json.loads(response)
    
    async def _analyze_product_comparison(self, competitors: List[Dict[str, Any]], website_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """产品对比分析"""
        prompt = f"""
        基于以下信息，进行产品对比分析：
        
        竞争对手: {json.dumps(competitors, ensure_ascii=False)}
        网站内容: {website_content['content'][:1500]}
        
        请对比分析产品/服务，包括：
        1. 功能特性对比
        2. 价格策略对比
        3. 用户体验对比
        4. 技术优势对比
        5. 服务支持对比
        
        请以JSON格式返回结果，包含product_comparison数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("product_comparison", [])
    
    async def _analyze_marketing_strategies(self, competitors: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """营销策略分析"""
        prompt = f"""
        基于以下竞争对手信息，分析营销策略：
        
        竞争对手: {json.dumps(competitors, ensure_ascii=False)}
        
        请分析营销策略，包括：
        1. 品牌定位策略
        2. 内容营销策略
        3. 社交媒体策略
        4. 广告投放策略
        5. 客户获取策略
        
        请以JSON格式返回结果，包含marketing_strategies数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("marketing_strategies", [])
    
    async def _analyze_competitive_advantages(self, website_content: Dict[str, Any], competitors: List[Dict[str, Any]]) -> List[str]:
        """竞争优势分析"""
        prompt = f"""
        基于以下信息，分析竞争优势：
        
        网站内容: {website_content['content'][:2000]}
        竞争对手: {json.dumps(competitors, ensure_ascii=False)}
        
        请识别和分析竞争优势，包括：
        1. 技术优势
        2. 成本优势
        3. 差异化优势
        4. 网络效应
        5. 品牌优势
        
        请以JSON格式返回结果，包含competitive_advantages数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("competitive_advantages", [])
    
    async def _analyze_market_positioning(self, website_content: Dict[str, Any], competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """市场定位分析"""
        prompt = f"""
        基于以下信息，分析市场定位：
        
        网站内容: {website_content['content'][:2000]}
        竞争对手: {json.dumps(competitors, ensure_ascii=False)}
        
        请分析市场定位，包括：
        1. 目标市场定位
        2. 价值主张
        3. 品牌形象
        4. 差异化策略
        5. 市场地位评估
        
        请以JSON格式返回结果。
        """
        
        response = await self._call_openai(prompt)
        return json.loads(response)
    
    async def _estimate_market_share(self, competitor: Dict[str, Any]) -> str:
        """估算市场份额"""
        # 这里可以集成市场数据API
        return "需要进一步分析"
    
    async def _analyze_competitor_strengths(self, competitor: Dict[str, Any]) -> List[str]:
        """分析竞争对手优势"""
        prompt = f"""
        分析竞争对手 {competitor.get('name', 'Unknown')} 的优势：
        
        竞争对手信息: {json.dumps(competitor, ensure_ascii=False)}
        
        请识别该竞争对手的主要优势。
        请以JSON格式返回结果，包含strengths数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("strengths", [])
    
    async def _analyze_competitor_weaknesses(self, competitor: Dict[str, Any]) -> List[str]:
        """分析竞争对手劣势"""
        prompt = f"""
        分析竞争对手 {competitor.get('name', 'Unknown')} 的劣势：
        
        竞争对手信息: {json.dumps(competitor, ensure_ascii=False)}
        
        请识别该竞争对手的主要劣势。
        请以JSON格式返回结果，包含weaknesses数组。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return analysis_data.get("weaknesses", [])
    
    async def _fallback_analysis(self, url: str) -> CompetitorAnalysis:
        """备用分析方案"""
        prompt = f"""
        基于URL {url}，分析该网站的竞争环境。
        请提供合理的竞争分析，包括竞争对手、竞争格局等。
        以JSON格式返回。
        """
        
        response = await self._call_openai(prompt)
        analysis_data = json.loads(response)
        
        return CompetitorAnalysis(
            competitors=analysis_data.get("competitors", []),
            competitive_landscape=analysis_data.get("competitive_landscape", {}),
            product_comparison=analysis_data.get("product_comparison", []),
            marketing_strategies=analysis_data.get("marketing_strategies", []),
            competitive_advantages=analysis_data.get("competitive_advantages", []),
            market_positioning=analysis_data.get("market_positioning", {})
        )
    
    async def _call_openai(self, prompt: str) -> str:
        """调用OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一个专业的竞争分析师，擅长分析市场竞争环境、竞争对手和竞争策略。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            # 返回默认分析结果
            return json.dumps({
                "competitors": [{"name": "主要竞争对手", "type": "直接竞争"}],
                "competitive_landscape": {"market_concentration": "中等", "competition_intensity": "高"},
                "product_comparison": [{"aspect": "功能", "comparison": "需要详细分析"}],
                "marketing_strategies": [{"strategy": "品牌营销", "effectiveness": "需要评估"}],
                "competitive_advantages": ["技术优势", "成本优势"],
                "market_positioning": {"target_market": "需要分析", "value_proposition": "需要明确"}
            }) 