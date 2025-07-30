# 开发指南

## 项目概述

北美市场洞察工具是一个基于AI的智能分析平台，能够分析任意网址并提供市场趋势、用户画像和竞争分析。

## 技术架构

### 后端技术栈
- **框架**: FastAPI (Python)
- **数据库**: PostgreSQL
- **缓存**: Redis
- **任务队列**: Celery
- **AI服务**: OpenAI GPT-4
- **部署**: Docker

### 前端技术栈
- **框架**: React 18 + TypeScript
- **样式**: Tailwind CSS
- **状态管理**: React Hooks
- **路由**: React Router
- **HTTP客户端**: Axios
- **UI组件**: Headless UI + Heroicons

## 开发环境设置

### 1. 克隆项目
```bash
git clone <repository-url>
cd market-intelligence-tool
```

### 2. 环境变量配置
创建 `.env` 文件：
```bash
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 数据库配置
DATABASE_URL=postgresql://user:password@localhost/market_intelligence

# Redis配置
REDIS_URL=redis://localhost:6379

# 应用配置
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 3. 使用Docker启动开发环境
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f backend
```

### 4. 本地开发设置

#### 后端开发
```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发
```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

## 项目结构

```
market-intelligence-tool/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务服务
│   │   └── database/       # 数据库配置
│   ├── main.py            # 主应用入口
│   ├── requirements.txt   # Python依赖
│   └── Dockerfile         # 后端Docker配置
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── components/    # React组件
│   │   ├── pages/         # 页面组件
│   │   ├── services/      # API服务
│   │   └── utils/         # 工具函数
│   ├── package.json       # Node.js依赖
│   └── Dockerfile         # 前端Docker配置
├── docs/                  # 项目文档
├── docker-compose.yml     # Docker编排配置
└── README.md             # 项目说明
```

## API文档

启动后端服务后，访问以下地址查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 主要API端点

#### 1. 启动分析任务
```http
POST /api/analyze
Content-Type: application/json

{
  "url": "https://example.com",
  "analysis_type": "full"
}
```

#### 2. 获取分析结果
```http
GET /api/analysis/{task_id}
```

#### 3. 获取分析历史
```http
GET /api/history
```

## 开发规范

### 代码风格

#### Python (后端)
- 使用 Black 进行代码格式化
- 遵循 PEP 8 规范
- 使用类型注解
- 编写文档字符串

#### TypeScript (前端)
- 使用 ESLint + Prettier
- 遵循 Airbnb 代码规范
- 使用 TypeScript 严格模式
- 组件使用函数式编程

### Git工作流
1. 创建功能分支: `git checkout -b feature/feature-name`
2. 提交更改: `git commit -m "feat: add new feature"`
3. 推送分支: `git push origin feature/feature-name`
4. 创建Pull Request

### 提交信息规范
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm test
```

## 部署

### 生产环境部署
```bash
# 构建生产镜像
docker-compose -f docker-compose.prod.yml build

# 启动生产服务
docker-compose -f docker-compose.prod.yml up -d
```

### 环境变量配置
生产环境需要配置以下环境变量：
- `OPENAI_API_KEY`: OpenAI API密钥
- `DATABASE_URL`: 生产数据库连接
- `REDIS_URL`: 生产Redis连接
- `SECRET_KEY`: 应用密钥
- `DEBUG`: 设置为False

## 故障排除

### 常见问题

1. **数据库连接失败**
   - 检查PostgreSQL服务是否启动
   - 验证数据库连接字符串
   - 确认数据库用户权限

2. **Redis连接失败**
   - 检查Redis服务是否启动
   - 验证Redis连接配置
   - 确认网络连接

3. **OpenAI API调用失败**
   - 检查API密钥是否正确
   - 确认API配额是否充足
   - 验证网络连接

4. **前端无法连接后端**
   - 检查后端服务是否启动
   - 验证API地址配置
   - 确认CORS设置

### 日志查看
```bash
# 查看所有服务日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend

# 实时查看日志
docker-compose logs -f
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License 