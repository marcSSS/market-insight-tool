from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    """分析任务状态枚举"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class AnalysisType(str, Enum):
    """分析类型枚举"""
    MARKET = "market"
    USER = "user"
    COMPETITOR = "competitor"
    FULL = "full"

class AnalysisRequest(BaseModel):
    """分析请求模型"""
    url: HttpUrl = Field(..., description="要分析的网址")
    analysis_type: AnalysisType = Field(default=AnalysisType.FULL, description="分析类型")
    custom_parameters: Optional[Dict[str, Any]] = Field(default=None, description="自定义分析参数")

class MarketTrends(BaseModel):
    """市场趋势分析结果"""
    market_size: Dict[str, Any] = Field(..., description="市场规模数据")
    cagr: float = Field(..., description="复合年增长率")
    key_drivers: List[str] = Field(..., description="关键市场驱动因素")
    growth_forecast: Dict[str, Any] = Field(..., description="增长预测")
    market_segments: List[Dict[str, Any]] = Field(..., description="市场细分")
    industry_trends: List[str] = Field(..., description="行业趋势")

class UserProfile(BaseModel):
    """用户画像分析结果"""
    target_audience: List[Dict[str, Any]] = Field(..., description="目标用户群体")
    user_needs: List[str] = Field(..., description="用户需求")
    pain_points: List[str] = Field(..., description="用户痛点")
    user_behavior: Dict[str, Any] = Field(..., description="用户行为模式")
    demographics: Dict[str, Any] = Field(..., description="人口统计学特征")
    psychographics: Dict[str, Any] = Field(..., description="心理特征")

class CompetitorAnalysis(BaseModel):
    """竞争分析结果"""
    competitors: List[Dict[str, Any]] = Field(..., description="竞争对手列表")
    competitive_landscape: Dict[str, Any] = Field(..., description="竞争格局")
    product_comparison: List[Dict[str, Any]] = Field(..., description="产品对比")
    marketing_strategies: List[Dict[str, Any]] = Field(..., description="营销策略分析")
    competitive_advantages: List[str] = Field(..., description="竞争优势")
    market_positioning: Dict[str, Any] = Field(..., description="市场定位")

class AnalysisResult(BaseModel):
    """完整分析结果"""
    market_trends: Optional[MarketTrends] = Field(default=None, description="市场趋势分析")
    user_profile: Optional[UserProfile] = Field(default=None, description="用户画像分析")
    competitor_analysis: Optional[CompetitorAnalysis] = Field(default=None, description="竞争分析")
    summary: str = Field(..., description="分析总结")
    recommendations: List[str] = Field(..., description="建议和洞察")

class AnalysisResponse(BaseModel):
    """分析响应模型"""
    task_id: str = Field(..., description="分析任务ID")
    status: AnalysisStatus = Field(..., description="任务状态")
    result: Optional[AnalysisResult] = Field(default=None, description="分析结果")
    message: str = Field(..., description="状态消息")
    created_at: datetime = Field(..., description="创建时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    progress: Optional[int] = Field(default=None, description="进度百分比")

class AnalysisHistory(BaseModel):
    """分析历史记录"""
    id: int = Field(..., description="记录ID")
    task_id: str = Field(..., description="任务ID")
    url: str = Field(..., description="分析的URL")
    analysis_type: AnalysisType = Field(..., description="分析类型")
    status: AnalysisStatus = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    completed_at: Optional[datetime] = Field(default=None, description="完成时间")
    result_summary: Optional[str] = Field(default=None, description="结果摘要") 