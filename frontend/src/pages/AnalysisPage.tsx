import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-hot-toast';
import { 
  MagnifyingGlassIcon,
  ChartBarIcon,
  UserGroupIcon,
  TrophyIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';
import axios from 'axios';

interface AnalysisRequest {
  url: string;
  analysis_type: 'market' | 'user' | 'competitor' | 'full';
  custom_parameters?: any;
}

const AnalysisPage: React.FC = () => {
  const navigate = useNavigate();
  const [url, setUrl] = useState('');
  const [analysisType, setAnalysisType] = useState<'market' | 'user' | 'competitor' | 'full'>('full');
  const [isLoading, setIsLoading] = useState(false);

  const analysisTypes = [
    {
      id: 'full',
      name: '完整分析',
      description: '市场趋势、用户画像和竞争分析',
      icon: ChartBarIcon,
      color: 'bg-blue-500'
    },
    {
      id: 'market',
      name: '市场趋势分析',
      description: '市场规模、CAGR和关键驱动因素',
      icon: ChartBarIcon,
      color: 'bg-green-500'
    },
    {
      id: 'user',
      name: '用户画像分析',
      description: '目标用户群体和需求痛点',
      icon: UserGroupIcon,
      color: 'bg-purple-500'
    },
    {
      id: 'competitor',
      name: '竞争分析',
      description: '竞争对手和竞争格局分析',
      icon: TrophyIcon,
      color: 'bg-orange-500'
    }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) {
      toast.error('请输入要分析的网址');
      return;
    }

    // 验证URL格式
    try {
      new URL(url);
    } catch {
      toast.error('请输入有效的网址');
      return;
    }

    setIsLoading(true);

    try {
      const request: AnalysisRequest = {
        url: url.trim(),
        analysis_type: analysisType
      };

      const response = await axios.post('/api/analyze', request);
      
      if (response.data.task_id) {
        toast.success('分析任务已启动，正在处理中...');
        navigate(`/results/${response.data.task_id}`);
      } else {
        toast.error('启动分析任务失败');
      }
    } catch (error: any) {
      console.error('Analysis error:', error);
      toast.error(error.response?.data?.detail || '分析请求失败，请稍后重试');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            市场洞察分析
          </h1>
          <p className="text-xl text-gray-600">
            输入任意网址，我们的AI将为您提供深度的市场分析报告
          </p>
        </div>

        {/* Analysis Form */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* URL Input */}
            <div>
              <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
                要分析的网址
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="url"
                  id="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
              <p className="mt-2 text-sm text-gray-500">
                请输入完整的网址，包括 http:// 或 https://
              </p>
            </div>

            {/* Analysis Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-4">
                选择分析类型
              </label>
              <div className="grid md:grid-cols-2 gap-4">
                {analysisTypes.map((type) => (
                  <div
                    key={type.id}
                    className={`relative p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                      analysisType === type.id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => setAnalysisType(type.id as any)}
                  >
                    <div className="flex items-start space-x-3">
                      <div className={`p-2 rounded-lg ${type.color} text-white`}>
                        <type.icon className="h-5 w-5" />
                      </div>
                      <div className="flex-1">
                        <h3 className="font-medium text-gray-900">{type.name}</h3>
                        <p className="text-sm text-gray-600 mt-1">{type.description}</p>
                      </div>
                      {analysisType === type.id && (
                        <div className="absolute top-2 right-2">
                          <div className="w-4 h-4 bg-blue-500 rounded-full flex items-center justify-center">
                            <div className="w-2 h-2 bg-white rounded-full"></div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <div className="pt-6">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    启动分析中...
                  </>
                ) : (
                  <>
                    开始分析
                    <ArrowRightIcon className="ml-2 h-5 w-5" />
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Features Preview */}
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">分析内容预览</h2>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center p-6 border border-gray-200 rounded-lg">
              <div className="inline-flex p-3 rounded-full bg-blue-100 text-blue-600 mb-4">
                <ChartBarIcon className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">市场趋势</h3>
              <p className="text-sm text-gray-600">
                市场规模、增长率、驱动因素、行业趋势
              </p>
            </div>
            <div className="text-center p-6 border border-gray-200 rounded-lg">
              <div className="inline-flex p-3 rounded-full bg-green-100 text-green-600 mb-4">
                <UserGroupIcon className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">用户画像</h3>
              <p className="text-sm text-gray-600">
                目标用户、需求痛点、行为模式、人口特征
              </p>
            </div>
            <div className="text-center p-6 border border-gray-200 rounded-lg">
              <div className="inline-flex p-3 rounded-full bg-purple-100 text-purple-600 mb-4">
                <TrophyIcon className="h-6 w-6" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">竞争分析</h3>
              <p className="text-sm text-gray-600">
                竞争对手、竞争格局、产品对比、营销策略
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalysisPage; 