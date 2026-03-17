import React from 'react';
import { AlertTriangle, CheckCircle, AlertCircle, XCircle, TrendingUp, Activity, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

const SeverityIndicator = ({ severity }) => {
  const getSeverityConfig = (category) => {
    const configs = {
      'Healthy': {
        icon: CheckCircle,
        gradient: 'from-green-400 via-emerald-500 to-teal-500',
        label: '✅ Healthy Leaf',
        emoji: '🌿'
      },
      'Mild': {
        icon: AlertCircle,
        gradient: 'from-yellow-400 via-amber-500 to-orange-500',
        label: '⚠️ Mild Infection',
        emoji: '🟡'
      },
      'Moderate': {
        icon: AlertTriangle,
        gradient: 'from-orange-500 via-red-500 to-rose-500',
        label: '🔶 Moderate Infection',
        emoji: '🟠'
      },
      'Severe': {
        icon: XCircle,
        gradient: 'from-red-500 via-rose-600 to-pink-600',
        label: '🚨 Severe Infection',
        emoji: '🔴'
      }
    };
    return configs[category] || configs['Healthy'];
  };

  const config = getSeverityConfig(severity.category);
  const Icon = config.icon;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8, y: 30 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.6, type: "spring" }}
      className={`card-rainbow border-neon relative overflow-hidden animate-pulse-glow`}
    >
      {/* Rotating Background */}
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        className={`absolute inset-0 bg-gradient-to-r ${config.gradient} opacity-20`}
      />

      <div className="relative z-10">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-5">
            <motion.div
              initial={{ scale: 0, rotate: -180 }}
              animate={{ scale: 1, rotate: 0 }}
              transition={{ delay: 0.3, type: "spring" }}
              whileHover={{ scale: 1.2, rotate: 360 }}
              className={`p-4 bg-gradient-to-r ${config.gradient} rounded-3xl shadow-neon-strong border-4 border-white/50`}
            >
              <Icon className="w-12 h-12 text-white" />
            </motion.div>
            <div>
              <h3 className="text-4xl font-black text-white neon-text">{config.label}</h3>
              <p className="text-xl text-white/90 font-bold mt-2">{severity.description}</p>
            </div>
          </div>
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.4, type: "spring" }}
            className="text-7xl font-black text-white neon-text"
          >
            {severity.percentage.toFixed(1)}%
          </motion.div>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xl font-black text-white">🎯 Infection Level</span>
            <span className="text-xl font-black text-white">
              {severity.percentage < 10 ? '🟢 Low' : severity.percentage < 30 ? '🟡 Medium' : '🔴 High'}
            </span>
          </div>
          <div className="h-6 bg-black/30 rounded-full overflow-hidden border-3 border-white/30">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${severity.percentage}%` }}
              transition={{ duration: 2, ease: "easeOut" }}
              className={`h-full bg-gradient-to-r ${config.gradient} relative`}
            >
              <motion.div
                animate={{
                  x: ['-100%', '200%'],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "linear"
                }}
                className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent"
              />
            </motion.div>
          </div>
        </div>

        {/* Statistics Grid */}
        <div className="grid grid-cols-2 gap-6">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.5 }}
            whileHover={{ scale: 1.05 }}
            className="p-6 glass rounded-2xl border-neon"
          >
            <div className="flex items-center space-x-3 mb-3">
              <Activity className="w-7 h-7 text-white" />
              <p className="text-lg font-black text-white">📊 Infected Area</p>
            </div>
            <p className="text-4xl font-black text-white neon-text">
              {severity.infected_area.toFixed(0)} <span className="text-xl">px²</span>
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.6 }}
            whileHover={{ scale: 1.05 }}
            className="p-6 glass rounded-2xl border-neon"
          >
            <div className="flex items-center space-x-3 mb-3">
              <TrendingUp className="w-7 h-7 text-white" />
              <p className="text-lg font-black text-white">📐 Total Area</p>
            </div>
            <p className="text-4xl font-black text-white neon-text">
              {severity.total_area.toFixed(0)} <span className="text-xl">px²</span>
            </p>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );
};

export default SeverityIndicator;
