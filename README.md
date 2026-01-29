# 🧠 MOVE  
### *Motor Output vs Visualized Execution*  
**A Neuron-Cortex–Visualized Machine Learning Model for Motor Imagery EEG**

---

## 🔥 Overview

**MOVE** is an end-to-end Brain–Computer Interface (BCI) pipeline that decodes **motor intention** from raw **64-channel EEG** and makes the decision process **interpretable and visualizable**.

Built for the **2026 Rice Datathon**, MOVE classifies **four motor imagery classes**—**Left Hand, Right Hand, Both Hands, Both Feet**—using a subject-independent machine learning pipeline grounded in neuroscience (Mu/Beta rhythms, ERD/ERS) and validated with strict cross-subject evaluation.

Beyond prediction, MOVE emphasizes **where in the cortex the decision comes from**, enabling real-world, safety-aware deployment.

---

## 🎯 What MOVE Does

- Decodes **motor imagery intention** from EEG  
- Outputs **class label + confidence**  
- Quantifies **signal quality** (artifact/spike awareness)  
- Enables **real-time visualization** of motor cortex activity  
- Supports **API-based deployment** for live BCI demos  

---

## 🧪 Dataset

- **EEG Channels:** 64 (BCI2000 system)  
- **Subjects:** 86  
- **Trials:** 7,000+  
- **Classes:**  
  - Left Hand  
  - Right Hand  
  - Both Hands  
  - Both Feet  

Each subject is treated as a **separate group** to ensure generalization to unseen users.

---

## 🛠️ Technical Pipeline

### 1️⃣ Data Aggregation & Integrity
- Custom loader merges per-subject `.npy` files into a unified tensor  
- Subject IDs tracked via a `groups` array  
- Prevents data leakage during evaluation  
- Memory-efficient loading for large EEG tensors  

### 2️⃣ Signal Preprocessing (Neuroscience-Driven)
Implemented using **MNE-Python**:
- **High-pass filter (1 Hz)** → removes drift & DC offset  
- **ICA artifact removal** → suppresses eye-blink contamination  
- **Band-pass filter (8–30 Hz)** → isolates **Mu & Beta** motor rhythms  
- **Spike / artifact scoring** → flags unreliable trials  

This preserves **motor ERD/ERS signatures** while suppressing noise.

### 3️⃣ Machine Learning Models

#### 🔹 Baseline: EEGNet (CNN for BCI)
- Temporal convolutions learn frequency filters  
- Depthwise spatial filters learn electrode importance (e.g., C3/C4)  
- Compact architecture prevents overfitting  

#### 🔹 Advanced: Filter-Bank Riemannian Pipeline
- Theta / Mu / Beta / Gamma band decomposition  
- Covariance estimation → Tangent Space projection  
- Logistic Regression classifier  
- Strong gains in subject-independent performance  

---

## 📊 Validation Strategy

- **5-Fold GroupKFold Cross-Validation**  
- Strict subject independence (no overlap)  
- Metrics:
  - Accuracy  
  - Balanced Accuracy  
  - F1-Score  
  - Confusion Analysis  
  - Confidence Distribution  

---

## 🧠 Results (Current Best)

- **Mean Balanced Accuracy:** ~**42–45%**  
- **Chance Level:** 25%  
- **Key Strength:** Hands vs Feet separation  
- **Main Confusion:** Both Hands vs Single Hand (expected motor cortex overlap)  

This performance is **competitive for subject-independent MI EEG**, especially without subject-specific calibration.

---

## 🔍 Interpretability (Core Strength)

MOVE prioritizes *explainability*, not just scores.

### ✔ Motor Cortex Evidence
- **C3, Cz, C4** identified as “Golden Channels”  
- Clear **ERD → ERS** patterns in Mu/Beta bands  
- Strong **contralateral activation**:
  - Left hand → Right hemisphere (C4)  
  - Right hand → Left hemisphere (C3)  

### ✔ Error Transparency
- Confusion matrices show *where* and *why* the model fails  
- Confidence scores enable **ABSTAIN gating** for safety-critical use  
- Low-confidence predictions can be rejected in real-world systems  

---

## 🌐 Real-World Deployment

MOVE is designed for **live BCI applications**:

- **FastAPI backend** exposes `/predict`  
- Accepts a single EEG trial (64×656)  
- Returns:
  - Label  
  - Confidence  
  - Class probabilities  
  - Artifact score  
  - Safety gate (ALLOW / ABSTAIN)  

### 🧠 Frontend Integration
- Connectable to a **3D motor cortex simulation** (Antigravity)  
- Visualizes predictions + confidence in real time  
- Demonstrates how ML decisions map to cortical regions  

---

## 🧰 Tech Stack

- **Languages:** Python  
- **EEG Processing:** MNE-Python  
- **ML / DL:** Scikit-Learn, TensorFlow/Keras  
- **BCI Models:** EEGNet, Riemannian Geometry  
- **Visualization:** Matplotlib, Seaborn, Three.js  
- **Deployment:** FastAPI, ngrok  
- **Platform:** Google Colab  

---

## 💻 How to Run (Google Colab)

### 1) Dataset Folder Structure
The notebook expects:
