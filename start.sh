#!/bin/bash

# 北美市场洞察工具 - 快速启动脚本

echo "🚀 启动北美市场洞察工具..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  未找到.env文件，创建默认配置..."
    cat > .env << EOF
# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here

# 数据库配置
DATABASE_URL=postgresql://user:password@postgres:5432/market_intelligence

# Redis配置
REDIS_URL=redis://redis:6379

# 应用配置
SECRET_KEY=your_secret_key_here
DEBUG=True
EOF
    echo "📝 请编辑.env文件，设置您的OpenAI API密钥"
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "📊 检查服务状态..."
docker-compose ps

# 显示访问信息
echo ""
echo "🎉 北美市场洞察工具启动完成！"
echo ""
echo "📱 前端应用: http://localhost:3000"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "   - 首次使用请访问前端应用"
echo "   - 确保已在.env文件中设置OpenAI API密钥"
echo "   - 查看日志: docker-compose logs -f"
echo "   - 停止服务: docker-compose down"
echo "" 