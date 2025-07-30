from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, JSON, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.core.config import settings
from app.models.analysis import AnalysisStatus, AnalysisType
import enum

# 创建数据库引擎
engine = create_engine(settings.DATABASE_URL)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

class AnalysisModel(Base):
    """分析任务数据库模型"""
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    url = Column(String, nullable=False)
    analysis_type = Column(Enum(AnalysisType), default=AnalysisType.FULL)
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING)
    result = Column(JSON, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    progress = Column(Integer, default=0)
    
    def __repr__(self):
        return f"<Analysis(task_id='{self.task_id}', status='{self.status}')>"

class UserModel(Base):
    """用户数据库模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<User(email='{self.email}', username='{self.username}')>"

class AnalysisHistoryModel(Base):
    """分析历史记录数据库模型"""
    __tablename__ = "analysis_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    task_id = Column(String, index=True)
    url = Column(String, nullable=False)
    analysis_type = Column(Enum(AnalysisType))
    status = Column(Enum(AnalysisStatus))
    result_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<AnalysisHistory(task_id='{self.task_id}', url='{self.url}')>"

# 创建数据库表
def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

# 获取数据库会话
def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 数据库操作函数
def save_analysis_result(db, task_id: str, result: dict, status: AnalysisStatus, message: str):
    """保存分析结果"""
    analysis = db.query(AnalysisModel).filter(AnalysisModel.task_id == task_id).first()
    if analysis:
        analysis.result = result
        analysis.status = status
        analysis.message = message
        analysis.completed_at = datetime.utcnow()
        analysis.progress = 100
        db.commit()
    return analysis

def update_analysis_status(db, task_id: str, status: AnalysisStatus, message: str, progress: int = None):
    """更新分析状态"""
    analysis = db.query(AnalysisModel).filter(AnalysisModel.task_id == task_id).first()
    if analysis:
        analysis.status = status
        analysis.message = message
        if progress is not None:
            analysis.progress = progress
        db.commit()
    return analysis

def get_analysis_by_task_id(db, task_id: str):
    """根据任务ID获取分析结果"""
    return db.query(AnalysisModel).filter(AnalysisModel.task_id == task_id).first()

def get_user_analysis_history(db, user_id: int, limit: int = 10):
    """获取用户分析历史"""
    return db.query(AnalysisHistoryModel).filter(
        AnalysisHistoryModel.user_id == user_id
    ).order_by(AnalysisHistoryModel.created_at.desc()).limit(limit).all() 