/**
 * API Service Module
 * Handles all API calls to the backend
 */

import axios from 'axios';
import i18n from '../i18n';

// API base URL - adjust based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000, // 30 seconds
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor
apiClient.interceptors.request.use(
    (config) => {
        // Add any auth tokens here if needed
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle errors globally
        if (error.response) {
            // Server responded with error
            console.error('API Error:', error.response.data);
        } else if (error.request) {
            // Request made but no response
            console.error('Network Error:', error.message);
        } else {
            // Something else happened
            console.error('Error:', error.message);
        }
        return Promise.reject(error);
    }
);

/**
 * Health check endpoint
 */
export const checkHealth = async () => {
    try {
        const response = await apiClient.get('/health');
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * Predict disease from image file
 * @param {File} file - Image file
 * @param {number} confThreshold - Confidence threshold (0-1)
 */
export const predictImage = async (file, confThreshold = 0.25) => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        // Get current language from i18n
        const language = i18n.language || 'en';

        const response = await apiClient.post(
            `/predict-image?conf_threshold=${confThreshold}&language=${language}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );

        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * Predict disease from video frame
 * @param {Blob} frameBlob - Video frame as blob
 * @param {number} confThreshold - Confidence threshold
 */
export const predictFrame = async (frameBlob, confThreshold = 0.25) => {
    try {
        const formData = new FormData();
        formData.append('file', frameBlob, 'frame.jpg');

        // Get current language from i18n
        const language = i18n.language || 'en';

        const response = await apiClient.post(
            `/predict-image?conf_threshold=${confThreshold}&language=${language}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );

        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * Get prediction history
 * @param {number} limit - Number of records to fetch
 */
export const getHistory = async (limit = 50) => {
    try {
        const response = await apiClient.get(`/history?limit=${limit}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * Get statistics
 */
export const getStatistics = async () => {
    try {
        const response = await apiClient.get('/stats');
        return response.data;
    } catch (error) {
        throw error;
    }
};

/**
 * PC app endpoint (same as predict-image but dedicated)
 * @param {File} file - Image file
 * @param {number} confThreshold - Confidence threshold
 */
export const pcAppPredict = async (file, confThreshold = 0.25) => {
    try {
        const formData = new FormData();
        formData.append('file', file);

        // Get current language from i18n
        const language = i18n.language || 'en';

        const response = await apiClient.post(
            `/pc-app-endpoint?conf_threshold=${confThreshold}&language=${language}`,
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            }
        );

        return response.data;
    } catch (error) {
        throw error;
    }
};

export default {
    checkHealth,
    predictImage,
    predictFrame,
    getHistory,
    getStatistics,
    pcAppPredict,
};
