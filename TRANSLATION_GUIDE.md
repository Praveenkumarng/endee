# 🌍 Multi-Language Translation Guide

The Cotton Leaf Disease Detection System now supports multiple languages! Currently implemented:
- **English (en)**
- **Hindi (hi)**
- **Telugu (te)**

## 🚀 How it Works

We use `react-i18next` for internationalization.
- **Configuration**: `src/i18n.js`
- **Language Switcher**: `src/components/features/LanguageSwitcher.jsx`
- **Usage**: `useTranslation` hook in components

## ➕ Adding a New Language

1. **Open `src/i18n.js`**
2. **Add the new language code** to the `resources` object.
   Example for Spanish (`es`):
   ```javascript
   es: {
     translation: {
       "nav.home": "Inicio",
       "nav.dashboard": "Panel",
       // ... copy all keys from 'en' and translate
     }
   }
   ```
3. **Update `src/components/features/LanguageSwitcher.jsx`**
   Add the new language to the `languages` array:
   ```javascript
   const languages = [
     { code: 'en', name: 'English', flag: '🇬🇧' },
     { code: 'hi', name: 'हिंदी', flag: '🇮🇳' },
     { code: 'te', name: 'తెలుగు', flag: '🇮🇳' },
     { code: 'es', name: 'Español', flag: '🇪🇸' }, // Add this line
   ];
   ```

## 🔑 Translation Keys Structure

| Key Prefix | Usage |
|------------|-------|
| `nav.` | Navigation links and buttons |
| `landing.` | Landing page hero, stats, CTA |
| `feature.` | Feature descriptions |
| `upload.` | Upload page text and errors |
| `dashboard.` | Dashboard stats and charts |
| `detect.` | Live detection interface |
| `results.` | Results page and severity |
| `about.` | About page content |
| `disease.` | Disease names |
| `severity.` | Severity levels |
| `footer.` | Footer links and copyright |

## 📝 Example Usage in Components

```javascript
import { useTranslation } from 'react-i18next';

const MyComponent = () => {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('landing.title')}</h1>
      <p>{t('landing.subtitle')}</p>
    </div>
  );
};
```
