import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, Upload, Video, BarChart3, Info, Leaf } from 'lucide-react';

const Sidebar = () => {
  const navItems = [
    { to: '/', icon: Home, label: 'Home' },
    { to: '/dashboard', icon: BarChart3, label: 'Dashboard' },
    { to: '/upload', icon: Upload, label: 'Upload Image' },
    { to: '/live', icon: Video, label: 'Live Detection' },
    { to: '/about', icon: Info, label: 'About' },
  ];

  return (
    <aside className="w-64 sidebar flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-green-600 to-emerald-600 rounded-xl flex items-center justify-center">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900">Cotton Vision</h1>
            <p className="text-xs text-gray-500">AI Disease Detection</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                isActive ? 'sidebar-item-active' : 'sidebar-item'
              }
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="card bg-gradient-to-br from-green-50 to-emerald-50 border-green-200">
          <p className="text-sm font-semibold text-green-900 mb-1">Need Help?</p>
          <p className="text-xs text-green-700">Check our documentation</p>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
