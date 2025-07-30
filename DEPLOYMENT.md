# 🚀 北美市场洞察工具 - 部署指南

## 📋 部署方案概览

### 方案一：Vercel + Railway (推荐新手)
- **前端**: Vercel (免费)
- **后端**: Railway (免费额度)
- **数据库**: Railway PostgreSQL
- **优点**: 免费、简单、自动HTTPS

### 方案二：AWS/GCP/Azure (推荐生产)
- **前端**: S3/Cloud Storage + CloudFront
- **后端**: EC2/Compute Engine + Load Balancer
- **数据库**: RDS/Cloud SQL
- **优点**: 稳定、可扩展、企业级

### 方案三：Docker + 云服务器 (推荐学习)
- **服务器**: 阿里云/腾讯云/华为云
- **部署**: Docker + Nginx
- **优点**: 完全控制、成本可控

---

## 🎯 方案一：Vercel + Railway 部署

### 1. 准备前端部署

#### 创建Vercel配置文件
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/*.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-railway-app.railway.app/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

#### 部署步骤
1. 注册 [Vercel](https://vercel.com)
2. 连接GitHub仓库
3. 配置构建设置
4. 部署完成

### 2. 准备后端部署

#### 创建Railway配置文件
```json
// railway.json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python production.py",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

#### 部署步骤
1. 注册 [Railway](https://railway.app)
2. 连接GitHub仓库
3. 设置环境变量
4. 部署完成

---

## 🏢 方案二：AWS部署

### 1. 准备AWS资源

#### 创建EC2实例
```bash
# 启动EC2实例
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.micro \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx
```

#### 配置安全组
- 开放端口: 22 (SSH), 80 (HTTP), 443 (HTTPS)
- 限制访问来源

### 2. 部署应用

#### 连接到服务器
```bash
ssh -i your-key.pem ubuntu@your-server-ip
```

#### 安装Docker
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 部署应用
```bash
# 克隆代码
git clone https://github.com/your-username/market-insight-tool.git
cd market-insight-tool

# 运行部署脚本
chmod +x deploy.sh
./deploy.sh
```

---

## 🐳 方案三：Docker部署

### 1. 本地测试部署

#### 构建镜像
```bash
# 构建Docker镜像
docker build -t market-insight-tool .

# 运行容器
docker run -d -p 8000:8000 --name market-insight-api market-insight-tool
```

#### 使用Docker Compose
```bash
# 启动所有服务
docker-compose -f docker-compose.prod.yml up -d

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 停止服务
docker-compose -f docker-compose.prod.yml down
```

### 2. 云服务器部署

#### 选择云服务器
- **阿里云**: ECS (2核4G起步)
- **腾讯云**: CVM (2核4G起步)
- **华为云**: ECS (2核4G起步)

#### 部署步骤
1. 购买云服务器
2. 配置安全组
3. 连接服务器
4. 安装Docker
5. 运行部署脚本

---

## 🔧 环境配置

### 1. 环境变量

#### 生产环境变量
```bash
# .env.production
ENVIRONMENT=production
PORT=8000
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=your-database-url
REDIS_URL=your-redis-url
```

#### 设置环境变量
```bash
# 在服务器上设置
export ENVIRONMENT=production
export OPENAI_API_KEY=your-openai-api-key

# 或在Docker Compose中设置
environment:
  - ENVIRONMENT=production
  - OPENAI_API_KEY=${OPENAI_API_KEY}
```

### 2. 域名配置

#### 购买域名
- 阿里云万网
- 腾讯云域名
- GoDaddy

#### 配置DNS
```
A记录: @ -> 你的服务器IP
A记录: www -> 你的服务器IP
CNAME记录: api -> your-domain.com
```

### 3. SSL证书

#### 使用Let's Encrypt (免费)
```bash
# 安装Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo crontab -e
# 添加: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 📊 监控和维护

### 1. 日志管理

#### 查看日志
```bash
# Docker日志
docker-compose -f docker-compose.prod.yml logs -f

# 应用日志
tail -f logs/app.log

# Nginx日志
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

#### 日志轮转
```bash
# 配置logrotate
sudo nano /etc/logrotate.d/market-insight

# 内容:
/path/to/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

### 2. 性能监控

#### 系统监控
```bash
# 安装htop
sudo apt-get install htop

# 监控系统资源
htop

# 监控磁盘使用
df -h

# 监控内存使用
free -h
```

#### 应用监控
```bash
# 健康检查
curl -f http://localhost/health

# API响应时间
curl -w "@curl-format.txt" -o /dev/null -s "http://localhost/api/analyze"
```

### 3. 备份策略

#### 数据库备份
```bash
# 创建备份脚本
#!/bin/bash
BACKUP_DIR="/backup/database"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump $DATABASE_URL > $BACKUP_DIR/backup_$DATE.sql

# 添加到crontab
0 2 * * * /path/to/backup.sh
```

#### 文件备份
```bash
# 备份配置文件
tar -czf backup_$(date +%Y%m%d).tar.gz /etc/nginx /etc/ssl

# 上传到云存储
aws s3 cp backup_$(date +%Y%m%d).tar.gz s3://your-backup-bucket/
```

---

## 🚨 故障排除

### 1. 常见问题

#### 服务无法启动
```bash
# 检查端口占用
netstat -tulpn | grep :8000

# 检查Docker状态
docker ps -a
docker logs container_name

# 检查系统资源
top
df -h
```

#### API响应慢
```bash
# 检查网络延迟
ping your-domain.com

# 检查数据库连接
psql $DATABASE_URL -c "SELECT 1;"

# 检查Redis连接
redis-cli ping
```

### 2. 性能优化

#### 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_analysis_task_id ON analysis_tasks(task_id);
CREATE INDEX idx_analysis_created_at ON analysis_tasks(created_at);

-- 优化查询
EXPLAIN ANALYZE SELECT * FROM analysis_tasks WHERE task_id = 'xxx';
```

#### 缓存优化
```python
# 使用Redis缓存
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 缓存分析结果
def get_cached_analysis(task_id):
    result = r.get(f"analysis:{task_id}")
    if result:
        return json.loads(result)
    return None
```

---

## 📞 技术支持

### 联系方式
- **邮箱**: support@your-domain.com
- **文档**: https://docs.your-domain.com
- **GitHub**: https://github.com/your-username/market-insight-tool

### 社区支持
- **Stack Overflow**: 使用标签 `market-insight-tool`
- **GitHub Issues**: 报告bug和功能请求
- **Discord**: 加入开发者社区

---

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✅ 初始版本发布
- ✅ 基础市场分析功能
- ✅ 动态进度显示
- ✅ 详细结果展示

### 计划功能
- 🔄 真实AI分析集成
- 🔄 用户认证系统
- 🔄 分析历史记录
- 🔄 导出PDF报告 