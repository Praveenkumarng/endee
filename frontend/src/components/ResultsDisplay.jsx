import React from 'react';
import SeverityIndicator from './SeverityIndicator';
import { AlertCircle, CheckCircle, Leaf, Clock, Zap, Award, Sparkles, Rocket } from 'lucide-react';
import { motion } from 'framer-motion';

const ResultsDisplay = ({ results, imageUrl }) => {
  if (!results) return null;

  const { detections, severity, recommendations, inference_time_ms } = results;

  const getConfidenceGradient = (confidence) => {
    if (confidence > 0.8) return 'from-green-400 to-emerald-500';
    if (confidence > 0.6) return 'from-yellow-400 to-amber-500';
    return 'from-orange-500 to-red-500';
  };

  const getPriorityConfig = (priority) => {
    const configs = {
      high: { gradient: 'from-red-500 to-rose-600', label: '🚨 HIGH PRIORITY', emoji: '🔴' },
      medium: { gradient: 'from-yellow-500 to-amber-600', label: '⚠️ MEDIUM', emoji: '🟡' },
      low: { gradient: 'from-green-500 to-emerald-600', label: '✅ LOW', emoji: '🟢' }
    };
    return configs[priority] || configs.medium;
  };

  return (
    <div className="space-y-10">
      {/* Image with Stats */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9, rotate: -5 }}
        animate={{ opacity: 1, scale: 1, rotate: 0 }}
        transition={{ duration: 0.6, type: "spring" }}
        className="card-rainbow border-neon relative overflow-hidden group"
      >
        <div className="relative">
          <img src={imageUrl} alt="Analysis" className="w-full rounded-3xl border-4 border-white/30" />

          {/* Stats Overlay */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-black/90 via-black/70 to-transparent rounded-b-3xl"
          >
            <div className="grid grid-cols-3 gap-6 text-white">
              {[
                { icon: Leaf, value: detections.length, label: 'Detections', gradient: 'from-green-400 to-emerald-500' },
                { icon: Zap, value: `${inference_time_ms.toFixed(0)}ms`, label: 'Speed', gradient: 'from-yellow-400 to-orange-500' },
                { icon: Award, value: severity.category, label: 'Severity', gradient: 'from-purple-400 to-pink-500' }
              ].map((stat, idx) => {
                const Icon = stat.icon;
                return (
                  <motion.div
                    key={idx}
                    whileHover={{ scale: 1.1 }}
                    className="text-center"
                  >
                    <div className={`w-12 h-12 mx-auto mb-2 bg-gradient-to-r ${stat.gradient} rounded-full flex items-center justify-center shadow-neon`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <p className="text-3xl font-black neon-text">{stat.value}</p>
                    <p className="text-sm opacity-90 font-bold">{stat.label}</p>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Severity */}
      <SeverityIndicator severity={severity} />

      {/* Detections */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="card-rainbow border-neon"
      >
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-4xl font-black text-white neon-text">🔬 Detected Diseases</h3>
          <motion.span
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="px-6 py-3 bg-gradient-to-r from-green-500 to-emerald-600 text-white font-black text-xl rounded-full shadow-neon border-3 border-white/50"
          >
            {detections.length} Found
          </motion.span>
        </div>

        {detections.length > 0 ? (
          <div className="space-y-6">
            {detections.map((detection, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.5 + index * 0.1, type: "spring" }}
                whileHover={{ scale: 1.03, x: 10 }}
                className={`p-8 rounded-3xl border-4 border-white/30 relative overflow-hidden ${detection.class_name === 'Healthy Leaf'
                    ? 'bg-gradient-to-r from-green-500/30 to-emerald-500/30'
                    : 'bg-gradient-to-r from-red-500/30 to-rose-500/30'
                  } shadow-neon`}
              >
                <div className="relative z-10 flex items-center justify-between">
                  <div className="flex items-center space-x-6">
                    <motion.div
                      whileHover={{ rotate: 360, scale: 1.2 }}
                      transition={{ duration: 0.6 }}
                      className={`p-5 rounded-2xl shadow-neon-strong border-3 border-white/50 ${detection.class_name === 'Healthy Leaf'
                          ? 'bg-gradient-to-r from-green-500 to-emerald-600'
                          : 'bg-gradient-to-r from-red-500 to-rose-600'
                        }`}
                    >
                      <Leaf className="w-10 h-10 text-white" />
                    </motion.div>
                    <div>
                      <p className="text-3xl font-black text-white neon-text">{detection.class_name}</p>
                      <p className="text-xl text-white/90 font-bold mt-1">
                        🎯 Confidence: {(detection.confidence * 100).toFixed(1)}%
                      </p>
                    </div>
                  </div>

                  {/* Confidence Bar */}
                  <div className="flex items-center space-x-6">
                    <div className="w-40 h-5 bg-black/30 rounded-full overflow-hidden border-3 border-white/30">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${detection.confidence * 100}%` }}
                        transition={{ duration: 1.5, delay: 0.5 + index * 0.1 }}
                        className={`h-full bg-gradient-to-r ${getConfidenceGradient(detection.confidence)} relative`}
                      >
                        <motion.div
                          animate={{ x: ['-100%', '200%'] }}
                          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                          className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent"
                        />
                      </motion.div>
                    </div>
                    <span className="text-4xl font-black text-white neon-text">
                      {(detection.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <CheckCircle className="w-24 h-24 text-green-400 mx-auto mb-6 animate-pulse" />
            <p className="text-3xl font-black text-white neon-text">✅ No diseases detected!</p>
            <p className="text-white/80 text-xl font-bold mt-3">The leaf appears to be healthy! 🌿</p>
          </div>
        )}
      </motion.div>

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="card-rainbow border-neon"
        >
          <div className="flex items-center space-x-4 mb-8">
            <div className="p-4 bg-gradient-to-r from-blue-500 to-cyan-600 rounded-2xl shadow-neon-strong">
              <Rocket className="w-8 h-8 text-white" />
            </div>
            <h3 className="text-4xl font-black text-white neon-text">💊 Treatment Recommendations</h3>
          </div>

          <div className="space-y-6">
            {recommendations.map((rec, index) => {
              const priorityConfig = getPriorityConfig(rec.priority);

              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + index * 0.1, type: "spring" }}
                  whileHover={{ scale: 1.02, x: 10 }}
                  className={`p-8 bg-gradient-to-r ${priorityConfig.gradient} rounded-3xl border-4 border-white/30 relative overflow-hidden shadow-neon-strong`}
                >
                  <div className="relative z-10">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center space-x-4 mb-3">
                          <h4 className="text-3xl font-black text-white neon-text">{rec.title}</h4>
                          <span className="px-5 py-2 bg-white/20 backdrop-blur-sm border-3 border-white/50 rounded-full text-sm font-black text-white">
                            {priorityConfig.label}
                          </span>
                        </div>
                        <p className="text-white text-xl font-bold leading-relaxed">{rec.description}</p>
                      </div>
                    </div>

                    {/* Additional Info */}
                    {(rec.dosage || rec.frequency) && (
                      <div className="mt-6 pt-6 border-t-4 border-white/30 grid grid-cols-2 gap-6">
                        {rec.dosage && (
                          <div>
                            <p className="text-sm font-black text-white/80 mb-2">💊 Dosage</p>
                            <p className="text-lg font-black text-white">{rec.dosage}</p>
                          </div>
                        )}
                        {rec.frequency && (
                          <div>
                            <p className="text-sm font-black text-white/80 mb-2">⏰ Frequency</p>
                            <p className="text-lg font-black text-white">{rec.frequency}</p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default ResultsDisplay;
