import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Video, Sparkles, TrendingUp, Shield, Zap, ArrowRight, Leaf } from 'lucide-react';
import { motion } from 'framer-motion';

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#F9FAFB] via-[#E8F5EC]/30 to-[#F9FAFB]">
      {/* Header */}
      <header className="navbar px-8 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#3FB075] to-[#27C091] rounded-[16px] flex items-center justify-center">
              <Leaf className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-[#1A1A1A]">CottonVision AI</span>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            {['Home', 'Dashboard', 'Upload', 'Live', 'About'].map((item) => (
              <button
                key={item}
                onClick={() => navigate(item === 'Home' ? '/' : `/${item.toLowerCase()}`)}
                className="text-[#7C8A98] hover:text-[#3FB075] font-medium transition-colors"
              >
                {item}
              </button>
            ))}
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-8 py-20">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Column */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-8"
          >
            <div className="space-y-4">
              <h1 className="text-6xl font-bold text-[#1A1A1A] leading-tight">
                Real-Time Cotton Leaf
                <br />
                <span className="gradient-text">Disease Detection</span>
              </h1>
              <p className="text-xl text-[#7C8A98] leading-relaxed">
                AI-powered diagnosis using YOLOv9
              </p>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/live')}
                className="btn-primary flex items-center space-x-2 text-lg"
              >
                <span>Start Detection</span>
                <ArrowRight className="w-5 h-5" />
              </button>
              <button
                onClick={() => navigate('/upload')}
                className="btn-secondary text-lg"
              >
                Upload Image
              </button>
            </div>
          </motion.div>

          {/* Right Column - Illustration */}
          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            className="relative"
          >
            <div className="relative w-full h-96 bg-gradient-to-br from-[#E8F5EC] to-white rounded-[32px] flex items-center justify-center overflow-hidden">
              {/* Floating Leaf Animation */}
              <motion.div
                animate={{ y: [0, -20, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
                className="relative"
              >
                <Leaf className="w-48 h-48 text-[#3FB075]" />
                {/* Bounding Box Simulation */}
                <div className="absolute inset-0 border-4 border-[#3FB075] rounded-[20px] m-4"></div>
              </motion.div>
              
              {/* Floating Shapes */}
              <div className="absolute top-10 right-10 w-20 h-20 bg-[#3FB075]/10 rounded-full blur-xl"></div>
              <div className="absolute bottom-10 left-10 w-32 h-32 bg-[#27C091]/10 rounded-full blur-xl"></div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="max-w-7xl mx-auto px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            { icon: Zap, title: 'Real-Time', desc: '>30 FPS detection speed' },
            { icon: Shield, title: '94% Accuracy', desc: 'YOLOv9 powered' },
            { icon: TrendingUp, title: 'Smart Analysis', desc: 'Severity detection' },
            { icon: Sparkles, title: 'Recommendations', desc: 'Expert treatment advice' }
          ].map((feature, idx) => {
            const Icon = feature.icon;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: idx * 0.1 }}
                className="card-hover text-center"
              >
                <div className="w-16 h-16 bg-[#E8F5EC] rounded-[20px] flex items-center justify-center mx-auto mb-4">
                  <Icon className="w-8 h-8 text-[#3FB075]" />
                </div>
                <h3 className="text-lg font-semibold text-[#1A1A1A] mb-2">{feature.title}</h3>
                <p className="text-sm text-[#7C8A98]">{feature.desc}</p>
              </motion.div>
            );
          })}
        </div>
      </section>
    </div>
  );
};

export default Home;
