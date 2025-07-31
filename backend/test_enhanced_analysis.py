#!/usr/bin/env python3
"""
测试增强版分析引擎
"""

import asyncio
import json
from analysis_engine import analysis_engine
from data_serializer import DataSerializer

async def test_analysis():
    """测试分析功能"""
    
    test_urls = [
        "https://www.apple.com",
        "https://www.tesla.com", 
        "https://www.amazon.com"
    ]
    
    for url in test_urls:
        print(f"\n{'='*50}")
        print(f"测试URL: {url}")
        print(f"{'='*50}")
        
        try:
            # 执行分析
            result = await analysis_engine.analyze_url(url)
            
            # 序列化结果
            serialized = DataSerializer.serialize_analysis_result(result)
            
            # 打印关键信息
            print(f"市场类别: {result['category']}")
            print(f"市场规模: {result['market_trends']['market_size'].value}")
            print(f"CAGR: {result['market_trends']['cagr'].value}")
            print(f"竞争对手数量: {len(result['competition']['top_competitors'])}")
            print(f"战略建议模块: {list(result['strategic_recommendations'].keys())}")
            
            # 验证数据源
            print(f"\n数据源验证:")
            for source in result['market_trends']['market_size'].sources:
                print(f"  - {source.name}: {source.confidence}")
            
            print("✅ 分析成功")
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_analysis()) 