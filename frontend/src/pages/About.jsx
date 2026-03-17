import React from 'react';
import { Leaf, Shield, Zap, Users, CheckCircle } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { motion } from 'framer-motion';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import { useTranslation } from 'react-i18next';

const About = () => {
  const { t } = useTranslation();

  const features = [
    {
      icon: Zap,
      title: t('about.aiPowered'),
      description: t('about.aiDesc')
    },
    {
      icon: Shield,
      title: t('about.highAccuracy'),
      description: t('about.accuracyDesc')
    },
    {
      icon: Leaf,
      title: t('about.realtime'),
      description: t('about.realtimeDesc')
    },
    {
      icon: Users,
      title: t('about.expert'),
      description: t('about.expertDesc')
    }
  ];

  const diseases = [
    {
      name: t('disease.bacterialBlight'),
      symptoms: [
        "Angular water-soaked spots on leaves",
        "Lesions turn brown to black",
        "Premature leaf shedding"
      ]
    },
    {
      name: t('disease.fusariumWilt'),
      symptoms: [
        "Yellowing of leaves",
        "Wilting of plants",
        "Brown discoloration of stem tissues"
      ]
    },
    {
      name: t('disease.leafCurl'),
      symptoms: [
        "Upward curling of leaves",
        "Thickening of veins",
        "Stunted plant growth"
      ]
    }
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <div className="flex-1 container py-12">
        <div className="max-w-4xl mx-auto space-y-16">
          {/* Hero Section */}
          <div className="text-center space-y-6">
            <h1 className="text-4xl md:text-5xl font-bold">
              {t('about.title')} <span className="text-primary">{t('about.titleHighlight')}</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              {t('about.subtitle')}
            </p>
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="h-full">
                    <CardContent className="p-6 space-y-4">
                      <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
                        <Icon className="w-6 h-6 text-primary" />
                      </div>
                      <h3 className="text-xl font-bold">{feature.title}</h3>
                      <p className="text-muted-foreground">
                        {feature.description}
                      </p>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })}
          </div>

          {/* Diseases Section */}
          <div className="space-y-8">
            <h2 className="text-3xl font-bold text-center">{t('about.diseases')}</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {diseases.map((disease, index) => (
                <Card key={index}>
                  <CardContent className="p-6">
                    <h3 className="text-xl font-bold mb-4 text-primary">{disease.name}</h3>
                    <div className="space-y-2">
                      <p className="font-semibold text-sm text-muted-foreground">{t('about.symptoms')}</p>
                      <ul className="space-y-2">
                        {disease.symptoms.map((symptom, idx) => (
                          <li key={idx} className="flex items-start text-sm">
                            <CheckCircle className="w-4 h-4 text-green-500 mr-2 mt-0.5 shrink-0" />
                            <span>{symptom}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>

      <Footer />
    </div>
  );
};

export default About;
