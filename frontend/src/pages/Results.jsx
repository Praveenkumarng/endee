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

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Column 1: Image & Severity */}
            <div className="space-y-6">
              <Card className="h-fit">
                <CardHeader>
                  <CardTitle>{t('results.analyzed')}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="relative aspect-square rounded-lg overflow-hidden border-2 border-dashed">
                    <img
                      src={imageUrl}
                      alt="Analyzed cotton leaf"
                      className="w-full h-full object-cover"
                    />
                    {detections.map((det, idx) => (
                      <div
                        key={idx}
                        className="absolute border-2 border-primary bg-primary/20"
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

              {/* Severity Score */}
              {!isHealthy && severity && (
                <Card>
                  <CardHeader>
                    <CardTitle>{t('results.severity')}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex justify-between items-center">
                        <span className="font-medium">
                          {t(`severity.${severity.category.toLowerCase()}`, severity.category)}
                        </span>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(severity.category)}`}>
                          {severity.percentage.toFixed(1)}% {t('results.infected')}
                        </span>
                      </div>
                      <Progress value={severity.percentage} className="h-2" />
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>

            {/* Column 2: Detection Results */}
            <div className="space-y-6">
              <Card className="h-full">
                <CardHeader>
                  <CardTitle>{t('results.title')}</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-6">
                    {detections.map((det, idx) => (
                      <div key={idx} className="flex items-start justify-between p-4 bg-secondary/50 rounded-lg">
                        <div>
                          <h4 className="font-semibold text-lg">
                            {t(getDiseaseTranslation(det.class_name))}
                          </h4>
                          <p className="text-sm text-muted-foreground mt-1">
                            {t('results.confidence')}: {(det.confidence * 100).toFixed(1)}%
                          </p>
                        </div>
                        {det.class_name === 'Healthy Leaf' ? (
                          <CheckCircle2 className="w-6 h-6 text-green-500" />
                        ) : (
                          <AlertTriangle className="w-6 h-6 text-yellow-500" />
                        )}
                      </div>
                    ))}

                    {detections.length === 0 && (
                      <div className="text-center p-8 text-muted-foreground">
                        <p>{t('results.noDetections')}</p>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Column 3: Recommendations */}
            <div className="space-y-6">
              {!isHealthy && recommendations && recommendations.length > 0 && (
                <Card className="h-full">
                  <CardHeader>
                    <CardTitle>{t('results.recommendations')}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {recommendations.map((rec, idx) => (
                        <div key={idx} className="flex gap-3">
                          <div className="mt-1 bg-primary/10 p-2 rounded-lg h-fit">
                            {rec.type === 'chemical' ? <FileText className="w-4 h-4 text-primary" /> : <Leaf className="w-4 h-4 text-primary" />}
                          </div>
                          <div>
                            <h4 className="font-medium mb-1">{getRecTitle(rec)}</h4>
                            <p className="text-sm text-muted-foreground">{getRecDesc(rec)}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
              
              {/* Expert AI Chat Interface */}
              {!isHealthy && disease && (
                 <ExpertChat diseaseName={disease} />
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
