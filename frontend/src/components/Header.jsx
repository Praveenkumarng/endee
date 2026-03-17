import React from 'react';
import { NavLink } from 'react-router-dom';
import { Leaf } from 'lucide-react';

const Header = () => {
  return (
    <header className="glass-card sticky top-0 z-50 border-b">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900">Cotton Vision</h1>
              <p className="text-xs text-gray-500">AI Disease Detection</p>
            </div>
          </div>

          <nav className="hidden md:flex items-center space-x-1">
            {[
              { to: '/', label: 'Home' },
              { to: '/upload', label: 'Upload' },
              { to: '/live', label: 'Live Detection' },
              { to: '/about', label: 'About' }
            ].map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `px-4 py-2 rounded-lg font-medium transition-colors ${
                    isActive
                      ? 'bg-green-50 text-green-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;
