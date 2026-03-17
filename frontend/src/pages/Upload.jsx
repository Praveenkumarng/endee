import React, { useState } from 'react';
import { Loader2, AlertCircle, Sparkles, ArrowRight, Leaf, Upload as UploadIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Card } from '@/components/ui/card';
import { motion, AnimatePresence } from 'framer-motion';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import UploadBox from '@/components/features/UploadBox';
import { predictImage } from '@/services/api';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

const Upload = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { t } = useTranslation();

  const handleImageSelect = (file) => {
    setSelectedImage(file);
    setError(null);
  };

  const handleClear = () => {
    setSelectedImage(null);
    setError(null);
  };

  const handleAnalyze = async () => {
    if (!selectedImage) return;

    setLoading(true);
    setError(null);

    try {
      const response = await predictImage(selectedImage, 0.25);
      navigate('/results', { state: { results: response, imageUrl: URL.createObjectURL(selectedImage) } });
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100">
      <Navbar />

      <div className="flex-1 container flex items-center justify-center py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-5xl"
        >
          <Card className="grid grid-cols-1 lg:grid-cols-2 overflow-hidden shadow-xl border-0">
            {/* Left Panel - Visual & Info */}
            <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent p-8 lg:p-12 flex flex-col justify-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-10 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl" />
                <div className="absolute bottom-10 left-10 w-48 h-48 bg-green-400/10 rounded-full blur-3xl" />
              </div>

              <div className="relative z-10 space-y-6">
                <div className="w-16 h-16 bg-white rounded-2xl shadow-sm flex items-center justify-center">
                  <Leaf className="w-8 h-8 text-primary" />
                </div>

                <div>
                  <h1 className="text-3xl font-bold mb-3 text-gray-900">
                    {t('upload.title')}
                  </h1>
                  <p className="text-lg text-muted-foreground leading-relaxed">
                    {t('upload.subtitle')}
                  </p>
                </div>

                <div className="space-y-4 pt-4">
                  <div className="flex items-center space-x-3 text-sm text-muted-foreground">
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm">
                      <Sparkles className="w-4 h-4 text-primary" />
                    </div>
                    <span>AI-Powered Analysis</span>
                  </div>
                  <div className="flex items-center space-x-3 text-sm text-muted-foreground">
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center shadow-sm">
                      <UploadIcon className="w-4 h-4 text-primary" />
                    </div>
                    <span>Instant Results</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Panel - Upload Action */}
            <div className="p-8 lg:p-12 bg-white flex flex-col justify-center">
              <div className="max-w-md mx-auto w-full space-y-6">
                <UploadBox
                  onImageSelect={handleImageSelect}
                  selectedImage={selectedImage}
                  onClear={handleClear}
                />

                <AnimatePresence mode="wait">
                  {selectedImage && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -10 }}
                    >
                      <Button
                        onClick={handleAnalyze}
                        disabled={loading}
                        className="w-full h-12 text-lg shadow-lg shadow-primary/20 hover:shadow-primary/30 transition-all"
                        size="lg"
                      >
                        {loading ? (
                          <>
                            <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                            {t('upload.analyzing')}
                          </>
                        ) : (
                          <>
                            <Sparkles className="w-5 h-5 mr-2" />
                            {t('upload.analyze')}
                            <ArrowRight className="w-5 h-5 ml-2" />
                          </>
                        )}
                      </Button>
                    </motion.div>
                  )}
                </AnimatePresence>

                <AnimatePresence>
                  {error && (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                    >
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertTitle>{t('upload.error')}</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </div>
          </Card>
        </motion.div>
      </div>
      <Footer />
    </div>
  );
};

export default Upload;
