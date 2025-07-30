#!/bin/bash

# 北美市场洞察工具 - 简化启动脚本

echo "🚀 启动北美市场洞察工具（简化版）..."

# 设置Node.js路径
export PATH="/opt/homebrew/bin:$PATH"

# 检查后端服务
echo "📡 检查后端服务..."
if curl -s http://localhost:8000/ > /dev/null; then
    echo "✅ 后端服务运行正常"
else
    echo "⚠️  后端服务未运行，正在启动..."
    cd backend
    source venv/bin/activate
    python test_server_fixed.py &
    cd ..
    sleep 3
fi

# 启动前端服务
echo "🌐 启动前端服务..."
cd frontend
python3 -m http.server 3000 &
cd ..

echo ""
echo "🎉 北美市场洞察工具启动完成！"
echo ""
echo "📱 前端应用: http://localhost:3000/test.html"
echo "🔍 分析页面: http://localhost:3000/analyze.html"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "💡 提示:"
echo "   - 访问前端页面查看应用界面"
echo "   - 后端API已配置OpenAI密钥"
echo "   - 按 Ctrl+C 停止服务"
echo "" 