import React from 'react';
import { TrendingUp, Activity, CheckCircle, AlertTriangle, Leaf, Zap } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import StatsCard from '@/components/features/StatsCard';
import { useTranslation } from 'react-i18next';

const Dashboard = () => {
  const { t } = useTranslation();

  const stats = [
    { title: t('dashboard.totalScans'), value: '1,234', icon: Activity, trend: '+12%', delay: 0 },
    { title: t('dashboard.detected'), value: '456', icon: AlertTriangle, trend: '+8%', delay: 0.1 },
    { title: t('dashboard.accuracy'), value: '94.2%', icon: CheckCircle, trend: '+2.1%', delay: 0.2 },
    { title: t('dashboard.responseTime'), value: '28ms', icon: Zap, trend: '-5ms', delay: 0.3 },
  ];

  const recentScans = [
    { id: 1, disease: t('disease.bacterialBlight'), confidence: 92.5, severity: t('severity.moderate'), time: '2 min ago' },
    { id: 2, disease: t('disease.healthy'), confidence: 98.1, severity: t('severity.healthy'), time: '5 min ago' },
    { id: 3, disease: t('disease.fusariumWilt'), confidence: 87.3, severity: t('severity.mild'), time: '12 min ago' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 container pt-2 pb-4">
        <div className="space-y-8">
          <div>
            <h1 className="text-4xl font-bold mb-2">{t('dashboard.title')}</h1>
            <p className="text-muted-foreground">{t('dashboard.subtitle')}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {stats.map((stat, index) => (
              <StatsCard key={index} {...stat} />
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>{t('dashboard.recentScans')}</CardTitle>
                  <CardDescription>{t('dashboard.recentDesc')}</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {recentScans.map((scan) => (
                      <motion.div
                        key={scan.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: scan.id * 0.1 }}
                        className="flex items-center justify-between p-4 rounded-lg bg-muted/50 hover:bg-muted transition-colors"
                      >
                        <div className="flex items-center space-x-4">
                          <div className="w-10 h-10 bg-primary/10 rounded-lg flex items-center justify-center">
                            <Leaf className="w-5 h-5 text-primary" />
                          </div>
                          <div>
                            <p className="font-semibold">{scan.disease}</p>
                            <p className="text-sm text-muted-foreground">{scan.time}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className="text-sm font-semibold">{scan.confidence}%</p>
                          <span className={`text-xs px-2 py-1 rounded-full ${scan.severity === t('severity.healthy') ? 'bg-green-100 text-green-700' :
                            scan.severity === t('severity.mild') ? 'bg-yellow-100 text-yellow-700' :
                              'bg-orange-100 text-orange-700'
                            }`}>
                            {scan.severity}
                          </span>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>{t('dashboard.distribution')}</CardTitle>
                <CardDescription>{t('dashboard.distributionDesc')}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {[
                    { name: t('disease.bacterialBlight'), percentage: 35, color: 'bg-red-500' },
                    { name: t('disease.fusariumWilt'), percentage: 28, color: 'bg-orange-500' },
                    { name: t('disease.leafCurl'), percentage: 22, color: 'bg-yellow-500' },
                    { name: t('disease.healthy'), percentage: 15, color: 'bg-green-500' },
                  ].map((disease, index) => (
                    <div key={index}>
                      <div className="flex items-center justify-between mb-2 text-sm">
                        <span className="font-medium">{disease.name}</span>
                        <span className="font-semibold">{disease.percentage}%</span>
                      </div>
                      <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${disease.percentage}%` }}
                          transition={{ duration: 1, delay: index * 0.1 }}
                          className={`h-full ${disease.color}`}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default Dashboard;
