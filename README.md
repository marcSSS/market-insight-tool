# 🚀 北美市场洞察工具

一个基于AI的智能市场分析平台，帮助用户快速分析任意网站的市场趋势、用户画像和竞争格局。

## ✨ 核心功能

- 🔍 **智能网站分析**: 输入任意URL，自动分析网站内容
- 📊 **市场趋势分析**: 市场规模、CAGR、关键驱动因素
- 👥 **用户画像分析**: 目标用户、需求痛点、行为特征
- 🏆 **竞争分析**: 竞争对手分析、优势劣势对比
- 📈 **实时进度**: 动态显示分析进度
- 📋 **详细报告**: 结构化的分析结果展示

## 🛠️ 技术栈

- **后端**: FastAPI (Python)
- **前端**: HTML + JavaScript + Tailwind CSS
- **部署**: Vercel (前端) + Railway (后端)
- **AI**: OpenAI API (计划集成)

## 🚀 快速开始

### 本地开发

1. **克隆仓库**
```bash
git clone https://github.com/your-username/market-insight-tool.git
cd market-insight-tool
```

2. **启动后端**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python test_server_fixed.py
```

3. **启动前端**
```bash
cd frontend
python3 -m http.server 3000
```

4. **访问应用**
- 前端: http://localhost:3000/analyze.html
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 生产部署

#### 方案一：Vercel + Railway (推荐)

1. **部署后端到Railway**
   - 注册 [Railway](https://railway.app)
   - 连接GitHub仓库
   - 自动部署完成

2. **部署前端到Vercel**
   - 注册 [Vercel](https://vercel.com)
   - 连接GitHub仓库
   - 自动部署完成

3. **配置环境变量**
   - 在Railway中设置后端环境变量
   - 在Vercel中更新API地址

#### 方案二：Docker部署

```bash
# 构建并运行
docker-compose -f docker-compose.prod.yml up -d

# 访问应用
http://localhost
```

## 📁 项目结构

```
market-insight-tool/
├── backend/                 # 后端API服务
│   ├── production.py       # 生产环境配置
│   ├── test_server_fixed.py # 开发测试服务器
│   └── requirements.txt    # Python依赖
├── frontend/               # 前端静态文件
│   ├── analyze.html       # 主分析页面
│   ├── test.html          # 测试页面
│   └── ...                # 其他静态资源
├── vercel.json            # Vercel配置
├── railway.json           # Railway配置
├── docker-compose.prod.yml # Docker生产配置
├── Dockerfile             # Docker镜像配置
└── deploy.sh              # 部署脚本
```

## 🔧 API接口

### 分析接口

**POST** `/api/analyze`
```json
{
  "url": "https://example.com",
  "analysis_type": "full"
}
```

**GET** `/api/analysis/{task_id}`
```json
{
  "task_id": "uuid",
  "status": "completed",
  "progress": 100,
  "result": {
    "market_trends": {...},
    "user_profile": {...},
    "competitor_analysis": {...}
  }
}
```

### 健康检查

**GET** `/health`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00",
  "environment": "production"
}
```

## 🎯 使用示例

1. **访问分析页面**: https://your-app.vercel.app/analyze
2. **输入网站URL**: 例如 `https://www.apple.com`
3. **选择分析类型**: 完整分析、市场分析、用户分析、竞争分析
4. **查看实时进度**: 动态进度条显示分析状态
5. **获取分析结果**: 详细的市场洞察报告

## 🔮 计划功能

- [ ] 真实AI分析集成 (OpenAI API)
- [ ] 用户认证系统
- [ ] 分析历史记录
- [ ] PDF报告导出
- [ ] 多语言支持
- [ ] 移动端优化

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系我们

- **项目地址**: https://github.com/your-username/market-insight-tool
- **问题反馈**: https://github.com/your-username/market-insight-tool/issues
- **邮箱**: support@your-domain.com

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！ 