import React from 'react';
import { Link } from 'react-router-dom';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            北美市场洞察工具
          </Link>
          <nav className="flex space-x-8">
            <Link to="/" className="text-gray-700 hover:text-blue-600">
              首页
            </Link>
            <Link to="/analyze" className="text-gray-700 hover:text-blue-600">
              开始分析
            </Link>
            <Link to="/history" className="text-gray-700 hover:text-blue-600">
              分析历史
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header; 