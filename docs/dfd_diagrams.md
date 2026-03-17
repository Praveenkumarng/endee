# Data Flow Diagrams

## DFD Level 0 (Context Diagram)

```mermaid
graph LR
    U[User] -->|Upload Image| S[Cotton Disease Detection System]
    S -->|Disease Report| U
    S -->|Store Logs| D[(Prediction Logs)]
```

## DFD Level 1 (Major Processes)

```mermaid
graph TB
    U[User] -->|Image| P1[1.0 Image Upload]
    P1 -->|Validated Image| P2[2.0 Disease Detection]
    P2 -->|Detections| P3[3.0 Severity Analysis]
    P3 -->|Severity Info| P4[4.0 Generate Recommendations]
    P4 -->|Results| P5[5.0 Display Results]
    P5 -->|Report| U
    P2 -->|Prediction Data| D1[(Logs)]
    P3 -->|Severity Data| D1
```

## DFD Level 2 (Detailed Processes)

### 2.0 Disease Detection (Detailed)

```mermaid
graph TB
    I[Input Image] --> P21[2.1 Preprocess Image]
    P21 -->|Normalized Image| P22[2.2 Run YOLO Inference]
    P22 -->|Raw Predictions| P23[2.3 Apply NMS]
    P23 -->|Filtered Boxes| P24[2.4 Post-process Results]
    P24 -->|Detections| O[Output]
    M[(Model Weights)] --> P22
```

### 3.0 Severity Analysis (Detailed)

```mermaid
graph TB
    D[Detections] --> P31[3.1 Calculate Infected Area]
    P31 --> P32[3.2 Determine Severity Category]
    P32 --> P33[3.3 Generate Description]
    P33 --> O[Severity Info]
```

### 4.0 Generate Recommendations (Detailed)

```mermaid
graph TB
    S[Severity Info] --> P41[4.1 Identify Diseases]
    D[Detections] --> P41
    P41 --> P42[4.2 Lookup Treatments]
    P42 --> P43[4.3 Prioritize by Severity]
    P43 --> O[Recommendations]
    DB[(Treatment Database)] --> P42
```

## Data Stores

1. **Model Weights**: Pre-trained YOLOv9 model
2. **Prediction Logs**: JSON file with historical predictions
3. **Treatment Database**: In-memory dictionary of recommendations

## External Entities

1. **User**: Interacts via web browser or PC app
2. **Camera**: Provides live video feed (optional)
