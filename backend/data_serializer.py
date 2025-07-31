from typing import Dict, Any, List
from dataclasses import asdict
from analysis_engine import InsightPoint, DataSource

class DataSerializer:
    """数据序列化工具"""
    
    @staticmethod
    def serialize_insight_point(insight: InsightPoint) -> Dict[str, Any]:
        """序列化洞察点"""
        return {
            "value": insight.value,
            "sources": [
                {
                    "name": source.name,
                    "url": source.url,
                    "confidence": source.confidence,
                    "data_type": source.data_type,
                    "timestamp": source.timestamp
                } for source in insight.sources
            ],
            "confidence": insight.confidence,
            "description": insight.description
        }
    
    @staticmethod
    def serialize_market_trends(market_trends: Dict[str, Any]) -> Dict[str, Any]:
        """序列化市场趋势数据"""
        return {
            "market_size": DataSerializer.serialize_insight_point(market_trends["market_size"]),
            "cagr": DataSerializer.serialize_insight_point(market_trends["cagr"]),
            "key_drivers": [
                DataSerializer.serialize_insight_point(driver) 
                for driver in market_trends["key_drivers"]
            ]
        }
    
    @staticmethod
    def serialize_user_profiles(user_profiles: Dict[str, Any]) -> Dict[str, Any]:
        """序列化用户画像数据"""
        return {
            "existing_users": {
                "demographics": DataSerializer.serialize_insight_point(user_profiles["existing_users"]["demographics"]),
                "pain_points": [
                    DataSerializer.serialize_insight_point(point)
                    for point in user_profiles["existing_users"]["pain_points"]
                ],
                "behaviors": DataSerializer.serialize_insight_point(user_profiles["existing_users"]["behaviors"])
            },
            "potential_users": {
                "demographics": DataSerializer.serialize_insight_point(user_profiles["potential_users"]["demographics"]),
                "pain_points": [
                    DataSerializer.serialize_insight_point(point)
                    for point in user_profiles["potential_users"]["pain_points"]
                ],
                "behaviors": DataSerializer.serialize_insight_point(user_profiles["potential_users"]["behaviors"])
            }
        }
    
    @staticmethod
    def serialize_competition(competition: Dict[str, Any]) -> Dict[str, Any]:
        """序列化竞争分析数据"""
        return {
            "top_competitors": [
                {
                    "name": comp["name"],
                    "market_share": DataSerializer.serialize_insight_point(comp["market_share"]),
                    "core_advantages": [
                        DataSerializer.serialize_insight_point(advantage)
                        for advantage in comp["core_advantages"]
                    ],
                    "website_traffic": DataSerializer.serialize_insight_point(comp["website_traffic"]),
                    "trends_score": DataSerializer.serialize_insight_point(comp["trends_score"])
                } for comp in competition["top_competitors"]
            ]
        }
    
    @staticmethod
    def serialize_strategic_recommendations(recommendations: Dict[str, Any]) -> Dict[str, Any]:
        """序列化战略建议数据"""
        result = {
            "strategy": [
                DataSerializer.serialize_insight_point(rec)
                for rec in recommendations["strategy"]
            ],
            "product": [
                DataSerializer.serialize_insight_point(rec)
                for rec in recommendations["product"]
            ],
            "marketing": [
                DataSerializer.serialize_insight_point(rec)
                for rec in recommendations["marketing"]
            ],
            "gtm": [
                DataSerializer.serialize_insight_point(rec)
                for rec in recommendations["gtm"]
            ],
            "user_acquisition": [
                DataSerializer.serialize_insight_point(rec)
                for rec in recommendations["user_acquisition"]
            ]
        }
        
        # 添加新的战略建议字段
        if "strategic_summary" in recommendations:
            result["strategic_summary"] = DataSerializer.serialize_insight_point(recommendations["strategic_summary"])
        
        if "marketing_opportunities" in recommendations:
            result["marketing_opportunities"] = [
                DataSerializer.serialize_insight_point(opp)
                for opp in recommendations["marketing_opportunities"]
            ]
        
        if "potential_user_opportunities" in recommendations:
            result["potential_user_opportunities"] = [
                DataSerializer.serialize_insight_point(opp)
                for opp in recommendations["potential_user_opportunities"]
            ]
        
        return result
    
    @staticmethod
    def serialize_analysis_result(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """序列化完整分析结果"""
        return {
            "url": analysis_result["url"],
            "category": analysis_result["category"],
            "analysis_timestamp": analysis_result["analysis_timestamp"],
            "market_trends": DataSerializer.serialize_market_trends(analysis_result["market_trends"]),
            "user_profiles": DataSerializer.serialize_user_profiles(analysis_result["user_profiles"]),
            "competition": DataSerializer.serialize_competition(analysis_result["competition"]),
            "strategic_recommendations": DataSerializer.serialize_strategic_recommendations(
                analysis_result["strategic_recommendations"]
            )
        } 