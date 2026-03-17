import React, { useState, useRef, useCallback, useEffect } from 'react';
import Webcam from 'react-webcam';
import { CameraOff, Play, Pause, Sparkles, Activity, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import { useTranslation } from 'react-i18next';
import { predictFrame } from '../services/api';

const Detection = () => {
  const webcamRef = useRef(null);
  const [isActive, setIsActive] = useState(false);
  const [results, setResults] = useState(null);
  const [fps, setFps] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const { t } = useTranslation();

  const capture = useCallback(async () => {
    if (!webcamRef.current || !isActive || isProcessing) return;

    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    setIsProcessing(true);
    try {
      const blob = await fetch(imageSrc).then(r => r.blob());
      const startTime = performance.now();
      const response = await predictFrame(blob, 0.25);
      const endTime = performance.now();

      const inferenceTime = endTime - startTime;
      setFps(Math.round(1000 / inferenceTime));
      setResults(response);
    } catch (error) {
      console.error('Detection error:', error);
    } finally {
      setIsProcessing(false);
    }
  }, [isActive, isProcessing]);

  useEffect(() => {
    if (isActive) {
      const interval = setInterval(capture, 1000); // Capture every second
      return () => clearInterval(interval);
    }
  }, [isActive, capture]);

  const toggleCamera = () => {
    setIsActive(!isActive);
    if (!isActive) {
      setResults(null);
      setFps(0);
    }
  };

  return (
    <div className="min-h-screen flex flex-col animate-fade-in">
      <Navbar />

      <div className="flex-1 container pt-2 pb-4">
        <div className="max-w-6xl mx-auto space-y-8">
          <div className="text-center space-y-4">
            <div className="inline-flex items-center space-x-2 px-6 py-3 glass rounded-full mb-4">
              <Activity className="w-5 h-5 text-green-600 animate-pulse" />
              <span className="text-sm font-semibold text-gray-700">{t('detect.liveResults')}</span>
            </div>

            <h1 className="text-4xl md:text-5xl font-black">
              <span className="gradient-text">{t('detect.title')}</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              {t('detect.subtitle')}
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Camera Feed */}
            <div className="lg:col-span-2 space-y-6">
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="card-glow relative overflow-hidden rounded-2xl"
              >
                <div className="relative aspect-video bg-gray-900 rounded-2xl overflow-hidden">
                  <AnimatePresence mode="wait">
                    {isActive ? (
                      <motion.div
                        key="camera"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="w-full h-full"
                      >
                        <Webcam
                          ref={webcamRef}
                          screenshotFormat="image/jpeg"
                          className="w-full h-full object-cover"
                          videoConstraints={{
                            facingMode: "environment"
                          }}
                        />
                      </motion.div>
                    ) : (
                      <motion.div
                        key="placeholder"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="flex flex-col items-center justify-center h-full"
                      >
                        <motion.div
                          animate={{
                            scale: [1, 1.1, 1],
                          }}
                          transition={{
                            duration: 2,
                            repeat: Infinity,
                            ease: "easeInOut"
                          }}
                          className="p-8 bg-gray-800 rounded-full mb-6"
                        >
                          <CameraOff className="w-24 h-24 text-gray-600" />
                        </motion.div>
                        <p className="text-gray-500 text-xl font-semibold">{t('detect.cameraOff')}</p>
                        <p className="text-gray-600 mt-2">{t('detect.startToSee')}</p>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* FPS Counter */}
                  <AnimatePresence>
                    {isActive && fps > 0 && (
                      <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        className="absolute top-4 right-4 px-6 py-3 glass rounded-xl font-mono flex items-center space-x-2"
                      >
                        <Zap className="w-5 h-5 text-green-500" />
                        <span className="text-2xl font-black text-white">{fps}</span>
                        <span className="text-sm text-gray-300">FPS</span>
                      </motion.div>
                    )}
                  </AnimatePresence>

                  {/* Processing Indicator */}
                  <AnimatePresence>
                    {isProcessing && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute top-4 left-4 px-4 py-2 bg-green-500/90 backdrop-blur-sm rounded-xl flex items-center space-x-2"
                      >
                        <Sparkles className="w-5 h-5 text-white animate-spin" />
                        <span className="text-white font-semibold">Processing...</span>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>

              {/* Control Button */}
              <motion.button
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                onClick={toggleCamera}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`w-full flex items-center justify-center space-x-3 text-lg font-bold py-6 rounded-2xl shadow-xl transition-all duration-300 ${isActive
                  ? 'bg-gradient-to-r from-red-500 to-rose-600 text-white hover:shadow-2xl'
                  : 'bg-gradient-to-r from-green-600 to-emerald-600 text-white hover:shadow-2xl'
                  }`}
              >
                {isActive ? (
                  <>
                    <Pause className="w-6 h-6" />
                    <span>{t('detect.stop')}</span>
                  </>
                ) : (
                  <>
                    <Play className="w-6 h-6" />
                    <span>{t('detect.start')}</span>
                  </>
                )}
              </motion.button>
            </div>

            {/* Results Panel */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.4 }}
              className="space-y-6"
            >
              <div className="card-glow rounded-2xl p-6 bg-white/50">
                <div className="flex items-center space-x-3 mb-6">
                  <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
                    <Activity className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-800">{t('detect.liveResults')}</h3>
                </div>

                <AnimatePresence mode="wait">
                  {results && results.detections ? (
                    <motion.div
                      key="results"
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      className="space-y-4"
                    >
                      {/* Detections Count */}
                      <div className="p-5 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl border-2 border-green-200">
                        <p className="text-sm font-semibold text-gray-600 mb-1">{t('results.detections')}</p>
                        <p className="text-4xl font-black gradient-text">
                          {results.detections.length}
                        </p>
                      </div>

                      {/* Severity */}
                      <div className="p-5 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border-2 border-blue-200">
                        <p className="text-sm font-semibold text-gray-600 mb-1">{t('results.severity')}</p>
                        <p className="text-3xl font-black text-gray-800">
                          {results.severity?.category || 'N/A'}
                        </p>
                        {results.severity?.percentage && (
                          <div className="mt-3 w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${results.severity.percentage}%` }}
                              className="h-full bg-gradient-to-r from-green-500 to-emerald-500"
                            />
                          </div>
                        )}
                      </div>

                      {/* Inference Time */}
                      <div className="p-5 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-2 border-purple-200">
                        <p className="text-sm font-semibold text-gray-600 mb-1">{t('results.inference')}</p>
                        <p className="text-3xl font-black text-gray-800">
                          {results.inference_time_ms?.toFixed(1)} <span className="text-lg">ms</span>
                        </p>
                      </div>

                      {/* Detected Diseases */}
                      {results.detections.length > 0 && (
                        <div className="p-5 bg-gradient-to-r from-orange-50 to-amber-50 rounded-xl border-2 border-orange-200">
                          <p className="text-sm font-semibold text-gray-600 mb-3">{t('results.detected')}</p>
                          <div className="space-y-2">
                            {results.detections.slice(0, 3).map((det, idx) => (
                              <div key={idx} className="flex items-center justify-between">
                                <span className="text-sm font-medium text-gray-700 truncate">
                                  {det.class_name}
                                </span>
                                <span className="text-sm font-bold text-gray-800">
                                  {(det.confidence * 100).toFixed(0)}%
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </motion.div>
                  ) : (
                    <motion.div
                      key="placeholder"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      exit={{ opacity: 0 }}
                      className="text-center py-12"
                    >
                      <motion.div
                        animate={{
                          rotate: 360,
                        }}
                        transition={{
                          duration: 3,
                          repeat: Infinity,
                          ease: "linear"
                        }}
                        className="w-20 h-20 mx-auto mb-4 bg-gradient-to-r from-gray-200 to-gray-300 rounded-full flex items-center justify-center"
                      >
                        <Activity className="w-10 h-10 text-gray-500" />
                      </motion.div>
                      <p className="text-gray-500 font-semibold">
                        {isActive ? t('detect.waiting') : t('detect.startToSee')}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>

              {/* Info Card */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="card bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 p-6 rounded-2xl"
              >
                <h4 className="font-bold text-gray-800 mb-3 flex items-center space-x-2">
                  <Sparkles className="w-5 h-5 text-green-600" />
                  <span>{t('detect.tips')}</span>
                </h4>
                <ul className="space-y-2 text-sm text-gray-700">
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 font-bold">•</span>
                    <span>{t('detect.tip1')}</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 font-bold">•</span>
                    <span>{t('detect.tip2')}</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 font-bold">•</span>
                    <span>{t('detect.tip3')}</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <span className="text-green-600 font-bold">•</span>
                    <span>{t('detect.tip4')}</span>
                  </li>
                </ul>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Detection;
