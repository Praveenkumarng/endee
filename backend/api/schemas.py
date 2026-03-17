"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Detection(BaseModel):
    """Single detection result"""
    class_id: int = Field(..., description="Class ID (0-3)")
    class_name: str = Field(..., description="Disease name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    bbox: List[float] = Field(..., description="Bounding box [x1, y1, x2, y2]")
    bbox_normalized: List[float] = Field(..., description="Normalized bbox [x1, y1, x2, y2]")

class SeverityInfo(BaseModel):
    """Severity analysis information"""
    category: str = Field(..., description="Severity category: Mild, Moderate, Severe, or Healthy")
    percentage: float = Field(..., ge=0.0, le=100.0, description="Infected area percentage")
    infected_area: float = Field(..., description="Estimated infected area in pixels")
    total_area: float = Field(..., description="Total image area in pixels")
    description: str = Field(..., description="Human-readable severity description")

class Recommendation(BaseModel):
    """Treatment recommendation"""
    type: str = Field(..., description="Recommendation type: chemical, organic, or prevention")
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation")
    priority: str = Field(..., description="Priority: high, medium, or low")

class PredictionResponse(BaseModel):
    """Response for image prediction"""
    success: bool = Field(..., description="Whether prediction was successful")
    timestamp: str = Field(..., description="Prediction timestamp")
    filename: str = Field(..., description="Uploaded filename")
    detections: List[Detection] = Field(..., description="List of detections")
    num_detections: int = Field(..., description="Number of detections")
    severity: SeverityInfo = Field(..., description="Severity analysis")
    recommendations: List[Recommendation] = Field(..., description="Treatment recommendations")
    inference_time_ms: float = Field(..., description="Inference time in milliseconds")

class HealthResponse(BaseModel):
    """Response for health check"""
    status: str = Field(..., description="System status: healthy or degraded")
    timestamp: str = Field(..., description="Check timestamp")
    model_loaded: bool = Field(..., description="Whether model is loaded")
    version: str = Field(..., description="API version")
    model_info: Optional[Dict[str, Any]] = Field(None, description="Model information")

class HistoryRecord(BaseModel):
    """Single prediction history record"""
    timestamp: str
    filename: str
    predictions: List[Detection]
    severity: SeverityInfo

class HistoryResponse(BaseModel):
    """Response for prediction history"""
    success: bool
    count: int
    history: List[Dict[str, Any]]

class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    timestamp: str = Field(..., description="Error timestamp")
