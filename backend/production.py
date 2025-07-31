import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uuid
from datetime import datetime
from analysis_engine import analysis_engine
from data_serializer import DataSerializer

app = FastAPI(
    title="Insight.AI",
    description="AI驱动的市场分析平台",
    version="1.0.0"
)

# 生产环境CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://market-insight-tool.vercel.app",  # Vercel域名
        "https://market-insight-tool-be7lq85ov-marcs-projects-794138a8.vercel.app",  # Vercel预览域名
        "http://localhost:3000",  # 本地开发
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 存储任务状态 (生产环境建议使用Redis)
task_status = {}

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "message": "Insight.AI API", 
        "status": "running",
        "version": "1.0.0",
        "environment": "production"
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "environment": "production"
    }

@app.post("/api/analyze")
async def analyze_url(request: dict):
    """分析API"""
    task_id = str(uuid.uuid4())
    
    # 初始化任务状态
    task_status[task_id] = {
        "status": "processing",
        "progress": 0,
        "message": "正在初始化分析...",
        "created_at": datetime.now().isoformat(),
        "url": request.get("url", ""),
        "analysis_type": request.get("analysis_type", "full")
    }
    
    # 启动异步任务
    asyncio.create_task(process_analysis(task_id))
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "分析任务已启动",
        "created_at": task_status[task_id]["created_at"]
    }

async def process_analysis(task_id: str):
    """使用新的分析引擎处理分析"""
    steps = [
        ("正在访问网站...", 10),
        ("正在识别市场类别...", 20),
        ("正在分析市场趋势...", 35),
        ("正在分析用户画像...", 50),
        ("正在分析竞争格局...", 70),
        ("正在生成战略建议...", 85),
        ("正在验证数据来源...", 95),
        ("分析完成！", 100)
    ]
    
    for message, progress in steps:
        task_status[task_id]["message"] = message
        task_status[task_id]["progress"] = progress
        await asyncio.sleep(1.5)
    
    # 使用新的分析引擎进行分析
    url = task_status[task_id]["url"]
    try:
        analysis_result = await analysis_engine.analyze_url(url)
        serialized_result = DataSerializer.serialize_analysis_result(analysis_result)
        
        task_status[task_id]["status"] = "completed"
        task_status[task_id]["progress"] = 100
        task_status[task_id]["completed_at"] = datetime.now().isoformat()
        task_status[task_id]["result"] = serialized_result
        
    except Exception as e:
        task_status[task_id]["status"] = "error"
        task_status[task_id]["error"] = str(e)
        task_status[task_id]["completed_at"] = datetime.now().isoformat()

@app.get("/api/analysis/{task_id}")
async def get_analysis_result(task_id: str):
    """获取分析结果"""
    if task_id not in task_status:
        return {"error": "任务不存在"}
    
    task_info = task_status[task_id]
    
    if task_info["status"] == "processing":
        return {
            "task_id": task_id,
            "status": "processing",
            "progress": task_info["progress"],
            "message": task_info["message"],
            "url": task_info["url"],
            "analysis_type": task_info["analysis_type"]
        }
    
    if task_info["status"] == "completed":
        return {
            "task_id": task_id,
            "status": "completed",
            "progress": 100,
            "url": task_info["url"],
            "analysis_type": task_info["analysis_type"],
            "completed_at": task_info["completed_at"],
            "result": task_info["result"]
        }
    
    if task_info["status"] == "error":
        return {
            "task_id": task_id,
            "status": "error",
            "error": task_info["error"],
            "completed_at": task_info["completed_at"]
        }

# 旧的生成函数已删除，现在使用新的分析引擎

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 
