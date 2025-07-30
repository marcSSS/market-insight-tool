#!/bin/bash

# 北美市场洞察工具 - 生产环境部署脚本

set -e  # 遇到错误立即退出

echo "🚀 开始部署北美市场洞察工具..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker未安装，请先安装Docker${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose未安装，请先安装Docker Compose${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker环境检查通过${NC}"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p ssl
mkdir -p logs

# 检查SSL证书
if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
    echo -e "${YELLOW}⚠️  SSL证书不存在，将使用自签名证书${NC}"
    echo "生成自签名SSL证书..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout ssl/key.pem \
        -out ssl/cert.pem \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
fi

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose -f docker-compose.prod.yml down || true

# 构建新镜像
echo "🔨 构建Docker镜像..."
docker-compose -f docker-compose.prod.yml build --no-cache

# 启动服务
echo "🚀 启动服务..."
docker-compose -f docker-compose.prod.yml up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ 服务启动成功！${NC}"
else
    echo -e "${RED}❌ 服务启动失败，请检查日志${NC}"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
fi

# 显示服务信息
echo ""
echo -e "${GREEN}🎉 部署完成！${NC}"
echo ""
echo "📊 服务信息："
echo "   🌐 前端访问: https://your-domain.com"
echo "   🔧 API地址: https://your-domain.com/api"
echo "   📚 API文档: https://your-domain.com/docs"
echo "   💚 健康检查: https://your-domain.com/health"
echo ""
echo "📋 管理命令："
echo "   查看日志: docker-compose -f docker-compose.prod.yml logs -f"
echo "   停止服务: docker-compose -f docker-compose.prod.yml down"
echo "   重启服务: docker-compose -f docker-compose.prod.yml restart"
echo ""
echo -e "${YELLOW}⚠️  注意：请将 'your-domain.com' 替换为您的实际域名${NC}" 