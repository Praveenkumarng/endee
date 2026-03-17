import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { CheckCircle, AlertTriangle, Download, RefreshCw, FileText, Leaf, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import { useTranslation } from 'react-i18next';
import { Progress } from '@/components/ui/progress';
import ExpertChat from '@/components/ExpertChat';

const Results = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { results, imageUrl } = location.state || {};
  const { t } = useTranslation();

  if (!results) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">No results found</h2>
          <Button onClick={() => navigate('/upload')}>Go back to Upload</Button>
        </div>
      </div>
    );
  }

  const { detections, inference_time_ms, filename, severity, recommendations } = results;

  const disease = detections[0]?.class_name || "Healthy";
  const confidence = detections[0]?.confidence ? (detections[0].confidence * 100).toFixed(1) : 0;

  const isHealthy = disease.toLowerCase().includes('healthy');

  // Helper to get translation key for disease
  const getDiseaseTranslation = (className) => {
    const map = {
      'Bacterial Blight': 'disease.bacterialBlight',
      'Fusarium Wilt': 'disease.fusariumWilt',
      'Leaf Curl Virus': 'disease.leafCurl',
      'Healthy Leaf': 'disease.healthy'
    };
    return map[className] || className;
  };

  // Helper to get recommendation text (try i18n first, then fallback to backend text)
  const getRecTitle = (rec) => {
    const key = `rec.${rec.id}.title`;
    const translated = t(key);
    return translated !== key ? translated : rec.title;
  };

  const getRecDesc = (rec) => {
    const key = `rec.${rec.id}.desc`;
    const translated = t(key);
    return translated !== key ? translated : rec.description;
  };

  const getSeverityColor = (category) => {
    switch (category?.toLowerCase()) {
      case 'severe':
        return 'bg-red-100 text-red-700';
      case 'moderate':
        return 'bg-yellow-100 text-yellow-700';
      case 'mild':
        return 'bg-green-100 text-green-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 container pt-2 pb-4">
        <div className="max-w-[1600px] mx-auto">
          <Button
            variant="ghost"
            className="mb-4"
            onClick={() => navigate('/upload')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {t('results.uploadAnother')}
          </Button>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
            {/* Main Content: Image, Detections, Recommendations (8 Columns) */}
            <div className="lg:col-span-8 space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Image & Severity */}
                <div className="space-y-6">
                  <Card>
                    <CardHeader className="pb-3">
                      <CardTitle className="text-xl">{t('results.analyzed')}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="relative aspect-square rounded-xl overflow-hidden border-2 border-dashed bg-muted/30">
                        <img
                          src={imageUrl}
                          alt="Analyzed cotton leaf"
                          className="w-full h-full object-cover"
                        />
                        {detections.map((det, idx) => (
                          <div
                            key={idx}
                            className="absolute border-2 border-primary bg-primary/20 rounded-sm"
                            style={{
                              left: `${det.bbox[0]}px`,
                              top: `${det.bbox[1]}px`,
                              width: `${det.bbox[2] - det.bbox[0]}px`,
                              height: `${det.bbox[3] - det.bbox[1]}px`,
                            }}
                          />
                        ))}
                      </div>
                    </CardContent>
                  </Card>

                  {!isHealthy && severity && (
                    <Card>
                      <CardHeader className="pb-3">
                        <CardTitle className="text-xl">{t('results.severity')}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-4">
                          <div className="flex justify-between items-center">
                            <span className="font-semibold text-lg">
                              {t(`severity.${severity.category.toLowerCase()}`, severity.category)}
                            </span>
                            <span className={`px-4 py-1.5 rounded-full text-sm font-bold ${getSeverityColor(severity.category)} shadow-sm`}>
                              {severity.percentage.toFixed(1)}% {t('results.infected')}
                            </span>
                          </div>
                          <Progress value={severity.percentage} className="h-2.5 shadow-inner" />
                        </div>
                      </CardContent>
                    </Card>
                  )}
                </div>

                {/* Detection Results */}
                <div className="space-y-6">
                  <Card className="h-full">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-xl">{t('results.title')}</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        {detections.map((det, idx) => (
                          <div key={idx} className="flex items-start justify-between p-4 bg-muted/40 border border-border/50 rounded-xl transition-all hover:bg-muted/60">
                            <div>
                              <h4 className="font-bold text-lg leading-tight">
                                {t(getDiseaseTranslation(det.class_name))}
                              </h4>
                              <p className="text-sm text-muted-foreground mt-1.5 flex items-center gap-1.5">
                                <span className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                                {t('results.confidence')}: {(det.confidence * 100).toFixed(1)}%
                              </p>
                            </div>
                            {det.class_name === 'Healthy Leaf' ? (
                              <div className="bg-green-100 p-2 rounded-lg">
                                <CheckCircle2 className="w-6 h-6 text-green-600" />
                              </div>
                            ) : (
                              <div className="bg-yellow-100 p-2 rounded-lg">
                                <AlertTriangle className="w-6 h-6 text-yellow-600" />
                              </div>
                            )}
                          </div>
                        ))}

                        {detections.length === 0 && (
                          <div className="text-center py-12 text-muted-foreground bg-muted/20 rounded-xl border border-dashed">
                            <Bot className="w-12 h-12 mx-auto mb-3 opacity-20" />
                            <p>{t('results.noDetections')}</p>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </div>

              {/* Recommendations (Bottom of Main Area) */}
              {!isHealthy && recommendations && recommendations.length > 0 && (
                <Card className="border-primary/20 shadow-sm bg-gradient-to-br from-background to-primary/5">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-xl flex items-center gap-2">
                       <Leaf className="w-5 h-5 text-primary" />
                       {t('results.recommendations')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {recommendations.map((rec, idx) => (
                        <div key={idx} className="flex gap-4 p-4 bg-background/60 rounded-xl border border-border/50 shadow-sm hover:shadow-md transition-shadow">
                          <div className="mt-0.5 bg-primary/10 p-2.5 rounded-xl h-fit ring-1 ring-primary/20">
                            {rec.type === 'chemical' ? <FileText className="w-5 h-5 text-primary" /> : <Leaf className="w-5 h-5 text-primary" />}
                          </div>
                          <div>
                            <h4 className="font-bold mb-1.5 text-foreground">{getRecTitle(rec)}</h4>
                            <p className="text-sm text-muted-foreground leading-relaxed italic">{getRecDesc(rec)}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Sidebar: Expert AI Chat (4 Columns) */}
            <div className="lg:col-span-4 h-full">
              {!isHealthy && disease && (
                <div className="sticky top-4 h-[calc(100vh-120px)] min-h-[600px]">
                  <ExpertChat diseaseName={disease} />
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default Results;
