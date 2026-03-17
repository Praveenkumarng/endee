import React, { useState, useCallback } from 'react';
import { Upload, X, Image as ImageIcon, CheckCircle, Cloud } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const ImageUpload = ({ onImageSelect, selectedImage, onClear }) => {
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageSelect(e.dataTransfer.files[0]);
    }
  }, [onImageSelect]);

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      onImageSelect(e.target.files[0]);
    }
  };

  return (
    <AnimatePresence mode="wait">
      {selectedImage ? (
        <motion.div
          key="preview"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className="card relative"
        >
          <button
            onClick={onClear}
            className="absolute top-4 right-4 z-10 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          
          <div className="mb-4">
            <div className="inline-flex items-center space-x-2 px-3 py-1.5 bg-[#E8F5EC] text-[#3FB075] rounded-full text-sm font-semibold">
              <CheckCircle className="w-4 h-4" />
              <span>Image Loaded</span>
            </div>
          </div>
          
          <img
            src={URL.createObjectURL(selectedImage)}
            alt="Selected"
            className="w-full h-auto rounded-[16px] mb-4"
          />
          
          <div className="flex items-center justify-between p-4 bg-[#F9FAFB] rounded-[16px]">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-[#3FB075] rounded-[12px] flex items-center justify-center">
                <ImageIcon className="w-5 h-5 text-white" />
              </div>
              <div>
                <p className="font-semibold text-[#1A1A1A] text-sm truncate max-w-xs">
                  {selectedImage.name}
                </p>
                <p className="text-xs text-[#7C8A98]">
                  {(selectedImage.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>
          </div>
        </motion.div>
      ) : (
        <motion.div
          key="upload"
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.95 }}
          className={`${dragActive ? 'upload-area-active' : 'upload-area'}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <label className="cursor-pointer block">
            <div className="flex flex-col items-center space-y-4">
              <div className="w-20 h-20 bg-[#E8F5EC] rounded-full flex items-center justify-center">
                <Cloud className="w-10 h-10 text-[#3FB075]" />
              </div>
              
              <div className="text-center">
                <p className="text-lg font-semibold text-[#1A1A1A] mb-1">
                  Drag your cotton leaf image here
                </p>
                <p className="text-sm text-[#7C8A98]">or <span className="text-[#3FB075] font-semibold">Browse</span></p>
              </div>
              
              <p className="text-xs text-[#7C8A98]">Supports: JPG, PNG</p>
            </div>
            
            <input
              type="file"
              className="hidden"
              accept="image/*"
              onChange={handleChange}
            />
          </label>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default ImageUpload;
