from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any
import httpx
import asyncio
from datetime import datetime
import uuid

from app.core.config import settings
from app.services.market_analyzer import MarketAnalyzer
from app.services.user_analyzer import UserAnalyzer
from app.services.competitor_analyzer import CompetitorAnalyzer
from app.models.analysis import AnalysisRequest, AnalysisResponse, AnalysisStatus
from app.database.database import get_db, AnalysisModel
from app.celery_app import celery_app

app = FastAPI(
    title="北美市场洞察工具",
    description="智能分析任意网址的市场趋势、用户画像和竞争环境",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局分析器实例
market_analyzer = MarketAnalyzer()
user_analyzer = UserAnalyzer()
competitor_analyzer = CompetitorAnalyzer()

@app.get("/")
async def root():
    """健康检查端点"""
    return {"message": "北美市场洞察工具 API", "status": "running"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_url(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    分析指定URL的市场洞察
    
    Args:
        request: 包含要分析的URL
        background_tasks: 后台任务处理器
    
    Returns:
        AnalysisResponse: 分析任务ID和状态
    """
    try:
        # 验证URL可访问性
        async with httpx.AsyncClient() as client:
            response = await client.get(str(request.url), timeout=10.0)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="无法访问提供的URL")
        
        # 生成分析任务ID
        task_id = str(uuid.uuid4())
        
        # 启动后台分析任务
        background_tasks.add_task(
            perform_analysis,
            task_id=task_id,
            url=str(request.url),
            analysis_type=request.analysis_type
        )
        
        return AnalysisResponse(
            task_id=task_id,
            status=AnalysisStatus.PENDING,
            message="分析任务已启动",
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析任务启动失败: {str(e)}")

@app.get("/api/analysis/{task_id}", response_model=AnalysisResponse)
async def get_analysis_status(task_id: str):
    """
    获取分析任务状态和结果
    
    Args:
        task_id: 分析任务ID
    
    Returns:
        AnalysisResponse: 分析结果或状态
    """
    try:
        # 从数据库获取分析结果
        db = next(get_db())
        analysis = db.query(AnalysisModel).filter(AnalysisModel.task_id == task_id).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="分析任务不存在")
        
        return AnalysisResponse(
            task_id=task_id,
            status=analysis.status,
            result=analysis.result,
            message=analysis.message,
            created_at=analysis.created_at,
            completed_at=analysis.completed_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取分析结果失败: {str(e)}")

async def perform_analysis(task_id: str, url: str, analysis_type: str = "full"):
    """
    执行市场分析的后台任务
    
    Args:
        task_id: 任务ID
        url: 要分析的URL
        analysis_type: 分析类型 (market, user, competitor, full)
    """
    try:
        # 更新任务状态为进行中
        update_task_status(task_id, AnalysisStatus.PROCESSING, "开始分析...")
        
        results = {}
        
        # 根据分析类型执行相应的分析
        if analysis_type in ["market", "full"]:
            results["market_trends"] = await market_analyzer.analyze(url)
            update_task_status(task_id, AnalysisStatus.PROCESSING, "市场趋势分析完成")
        
        if analysis_type in ["user", "full"]:
            results["user_profile"] = await user_analyzer.analyze(url)
            update_task_status(task_id, AnalysisStatus.PROCESSING, "用户画像分析完成")
        
        if analysis_type in ["competitor", "full"]:
            results["competitor_analysis"] = await competitor_analyzer.analyze(url)
            update_task_status(task_id, AnalysisStatus.PROCESSING, "竞争分析完成")
        
        # 保存分析结果
        save_analysis_result(task_id, results, AnalysisStatus.COMPLETED, "分析完成")
        
    except Exception as e:
        save_analysis_result(task_id, {}, AnalysisStatus.FAILED, f"分析失败: {str(e)}")

def update_task_status(task_id: str, status: AnalysisStatus, message: str):
    """更新任务状态"""
    # 这里应该更新数据库中的任务状态
    pass

def save_analysis_result(task_id: str, results: Dict[str, Any], status: AnalysisStatus, message: str):
    """保存分析结果到数据库"""
    # 这里应该保存结果到数据库
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 