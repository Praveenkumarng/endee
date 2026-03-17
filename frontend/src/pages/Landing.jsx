import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Video, Sparkles, TrendingUp, Shield, Zap, ArrowRight, Leaf, Activity, CheckCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { motion } from 'framer-motion';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import { useTranslation } from 'react-i18next';

const Landing = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const features = [
    {
      icon: Zap,
      title: t('feature.realtime.title'),
      description: t('feature.realtime.desc')
    },
    {
      icon: Shield,
      title: t('feature.accuracy.title'),
      description: t('feature.accuracy.desc')
    },
    {
      icon: TrendingUp,
      title: t('feature.analysis.title'),
      description: t('feature.analysis.desc')
    },
    {
      icon: Sparkles,
      title: t('feature.recommendations.title'),
      description: t('feature.recommendations.desc')
    }
  ];

  const stats = [
    { value: '>90%', label: t('landing.accuracy'), icon: CheckCircle },
    { value: '>30', label: t('landing.fps'), icon: Activity },
    { value: '4', label: t('landing.diseases'), icon: Leaf }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <section className="container pt-2 pb-20 md:pt-6 md:pb-32">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            <div className="inline-flex items-center space-x-2 px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-semibold">
              <Sparkles className="w-4 h-4" />
              <span>{t('landing.badge')}</span>
            </div>

            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              {t('landing.title')}
              <br />
              <span className="text-primary">{t('landing.titleHighlight')}</span>
            </h1>

            <p className="text-xl text-muted-foreground leading-relaxed">
              {t('landing.subtitle')}
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <Button
                onClick={() => navigate('/upload')}
                size="lg"
                className="text-lg"
              >
                <Upload className="w-5 h-5 mr-2" />
                {t('landing.uploadBtn')}
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
              <Button
                onClick={() => navigate('/detect')}
                variant="outline"
                size="lg"
                className="text-lg"
              >
                <Video className="w-5 h-5 mr-2" />
                {t('landing.liveBtn')}
              </Button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative"
          >
            <div className="relative w-full h-96 bg-gradient-to-br from-primary/10 to-primary/5 rounded-3xl flex items-center justify-center overflow-hidden">
              <motion.div
                animate={{ y: [0, -20, 0] }}
                transition={{ duration: 3, repeat: Infinity, ease: "easeInOut" }}
              >
                <Leaf className="w-48 h-48 text-primary" />
              </motion.div>

              <div className="absolute top-10 right-10 w-20 h-20 bg-primary/20 rounded-full blur-xl"></div>
              <div className="absolute bottom-10 left-10 w-32 h-32 bg-primary/20 rounded-full blur-xl"></div>
            </div>
          </motion.div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
          {stats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 + index * 0.1, duration: 0.5 }}
              >
                <Card>
                  <CardContent className="pt-6 text-center">
                    <Icon className="w-8 h-8 text-primary mx-auto mb-2" />
                    <div className="text-4xl font-bold text-primary mb-2">{stat.value}</div>
                    <div className="text-muted-foreground">{stat.label}</div>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Features */}
      <section className="bg-muted/50 py-20">
        <div className="container">
          <div className="text-center mb-12">
            <h2 className="text-4xl font-bold mb-4">{t('landing.featuresTitle')}</h2>
            <p className="text-xl text-muted-foreground">{t('landing.featuresSubtitle')}</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1, duration: 0.5 }}
                >
                  <Card className="h-full hover:shadow-lg transition-shadow">
                    <CardHeader>
                      <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mb-4">
                        <Icon className="w-6 h-6 text-primary" />
                      </div>
                      <CardTitle className="text-xl">{feature.title}</CardTitle>
                      <CardDescription>{feature.description}</CardDescription>
                    </CardHeader>
                  </Card>
                </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="container py-20">
        <Card className="bg-gradient-to-br from-primary/10 to-primary/5 border-primary/20">
          <CardContent className="text-center py-12">
            <h2 className="text-4xl font-bold mb-4">{t('landing.ctaTitle')}</h2>
            <p className="text-xl text-muted-foreground mb-8">
              {t('landing.ctaSubtitle')}
            </p>
            <Button size="lg" onClick={() => navigate('/upload')}>
              {t('landing.ctaBtn')}
            </Button>
          </CardContent>
        </Card>
      </section>

      <Footer />
    </div>
  );
};

export default Landing;
