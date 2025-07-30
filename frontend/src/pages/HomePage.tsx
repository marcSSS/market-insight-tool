import React from 'react';
import { Link } from 'react-router-dom';
import { 
  ChartBarIcon, 
  UserGroupIcon, 
  TrophyIcon,
  ArrowRightIcon,
  GlobeAltIcon,
  LightBulbIcon,
  ShieldCheckIcon,
  ClockIcon
} from '@heroicons/react/24/outline';

const HomePage: React.FC = () => {
  const features = [
    {
      icon: ChartBarIcon,
      title: "市场趋势分析",
      description: "深入分析市场规模、CAGR和关键驱动因素，把握行业发展脉搏",
      color: "bg-blue-500"
    },
    {
      icon: UserGroupIcon,
      title: "用户画像分析",
      description: "精准识别目标用户群体，分析需求痛点和行为模式",
      color: "bg-green-500"
    },
    {
      icon: TrophyIcon,
      title: "竞争分析",
      description: "全面分析竞争对手，识别市场机会和竞争优势",
      color: "bg-purple-500"
    }
  ];

  const benefits = [
    {
      icon: GlobeAltIcon,
      title: "北美市场专注",
      description: "专门针对北美市场的数据和分析模型"
    },
    {
      icon: LightBulbIcon,
      title: "AI智能分析",
      description: "基于先进AI技术的深度市场洞察"
    },
    {
      icon: ShieldCheckIcon,
      title: "数据安全",
      description: "企业级数据安全保障和隐私保护"
    },
    {
      icon: ClockIcon,
      title: "快速分析",
      description: "几分钟内完成深度市场分析报告"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              北美市场洞察工具
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-blue-100">
              输入任意网址，获得深度市场分析、用户画像和竞争洞察
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/analyze"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors inline-flex items-center justify-center"
              >
                开始分析
                <ArrowRightIcon className="ml-2 h-5 w-5" />
              </Link>
              <button className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-colors">
                查看演示
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              三大核心分析功能
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              我们的AI驱动分析引擎能够从任意网址中提取关键信息，为您提供全面的市场洞察
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-8 rounded-xl bg-gray-50 hover:bg-gray-100 transition-colors">
                <div className={`inline-flex p-4 rounded-full ${feature.color} text-white mb-6`}>
                  <feature.icon className="h-8 w-8" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              为什么选择我们
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              专业的市场分析工具，帮助您做出明智的商业决策
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {benefits.map((benefit, index) => (
              <div key={index} className="text-center">
                <div className="inline-flex p-4 rounded-full bg-blue-100 text-blue-600 mb-6">
                  <benefit.icon className="h-8 w-8" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">
                  {benefit.title}
                </h3>
                <p className="text-gray-600">
                  {benefit.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            立即开始您的市场分析
          </h2>
          <p className="text-xl mb-8 text-blue-100">
            只需输入网址，几分钟内获得专业的市场洞察报告
          </p>
          <Link
            to="/analyze"
            className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors inline-flex items-center"
          >
            免费开始分析
            <ArrowRightIcon className="ml-2 h-5 w-5" />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 