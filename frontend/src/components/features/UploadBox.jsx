import React, { useState, useCallback } from 'react';
import { Upload, X, Image as ImageIcon } from 'lucide-react';
import { Button } from '@/components/ui/button';

const UploadBox = ({ onImageSelect, selectedImage, onClear }) => {
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

  if (selectedImage) {
    return (
      <div className="relative p-4 border rounded-lg bg-muted/30">
        <Button
          onClick={onClear}
          variant="destructive"
          size="icon"
          className="absolute -top-2 -right-2 z-10 h-8 w-8 rounded-full shadow-md"
        >
          <X className="h-4 w-4" />
        </Button>

        <img
          src={URL.createObjectURL(selectedImage)}
          alt="Selected"
          className="w-full h-48 object-cover rounded-lg mb-4 shadow-sm"
        />

        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-primary/10 rounded-lg flex items-center justify-center">
            <ImageIcon className="w-4 h-4 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium text-sm truncate">{selectedImage.name}</p>
            <p className="text-xs text-muted-foreground">
              {(selectedImage.size / 1024).toFixed(2)} KB
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${dragActive
          ? 'border-primary bg-primary/5 scale-[1.02]'
          : 'border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50'
        }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <label className="cursor-pointer block">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center animate-pulse">
            <Upload className="w-8 h-8 text-primary" />
          </div>

          <div>
            <p className="text-lg font-semibold mb-1">
              Drop image here
            </p>
            <p className="text-sm text-muted-foreground">
              or <span className="text-primary font-semibold hover:underline">browse</span> to upload
            </p>
          </div>

          <p className="text-xs text-muted-foreground bg-muted px-3 py-1 rounded-full">
            JPG, PNG • Max 10MB
          </p>
        </div>

        <input
          type="file"
          className="hidden"
          accept="image/*"
          onChange={handleChange}
        />
      </label>
    </div>
  );
};

export default UploadBox;
