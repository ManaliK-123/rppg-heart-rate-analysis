# Remote Photoplethysmography Based Heart Rate Estimation Using Classical Signal Processing and Deep Spatiotemporal Learning

This repository implements a complete computer vision and deep learning pipeline for non-contact heart rate estimation from facial video using Remote Photoplethysmography (rPPG). It features classical rPPG baselines (Green, CHROM, POS), region-of-interest (ROI) extraction using MediaPipe FaceMesh, a real-time webcam demo, dataset loaders, deep learning models (PhysNet), evaluation metrics, and export tools.

> [!WARNING]
> **Medical Disclaimer**: This project is a research prototype for non-contact pulse-rate estimation. It is not a certified medical device and must not be used for diagnosis or emergency care.

## Local Development Stack
- **OS**: Windows 11 (x64)
- **Python**: 3.11 (via Miniconda or Conda)
- **Frameworks**: PyTorch, MediaPipe, OpenCV, SciPy, NumPy, Pandas, Matplotlib, scikit-learn, PyYAML, pytest

## Repository Structure
```text
rppg-heart-rate-ai/
    README.md
    requirements.txt
    environment.yml
    .gitignore
    configs/
        default.yaml
        ubfc.yaml
        pure.yaml
        cohface.yaml
    data/
        raw/
        processed/
        splits/
    src/
        main.py
        utils/
            device.py
            config.py
            logger.py
            seed.py
        preprocessing/
            video_reader.py
            face_detector.py
            roi_extractor.py
            skin_mask.py
            signal_processing.py
        classical/
            green.py
            chrom.py
            pos.py
            evm.py
        datasets/
            common.py
            ubfc_loader.py
            pure_loader.py
            cohface_loader.py
        models/
            physnet.py
            efficient_phys.py
            losses.py
        training/
            train.py
            validate.py
            scheduler.py
        evaluation/
            metrics.py
            bland_altman.py
            statistical_tests.py
            plots.py
        realtime/
            webcam_demo.py
        export/
            export_torchscript.py
            export_onnx.py
            export_optional_runtime.py
    notebooks/
        01_dataset_check.ipynb
        02_classical_baselines.ipynb
        03_model_training.ipynb
        04_results_analysis.ipynb
    experiments/
    outputs/
        models/
        plots/
        reports/
    tests/
        test_pos.py
        test_chrom.py
        test_metrics.py
        test_losses.py
```

## Setup Instructions

### 1. Environment Setup
Create the conda environment and activate it:
```powershell
conda env create -f environment.yml
conda activate rppg-heart-rate-ai
```
Or install dependencies via pip:
```powershell
pip install -r requirements.txt
```

### 2. Device Validation
Verify PyTorch environment and CUDA capability:
```powershell
python src/utils/device.py
```

### 3. Run Webcam Demo
To test classical algorithms (POS/CHROM/Green) on real-time webcam feed:
```powershell
# Using POS algorithm
python src/realtime/webcam_demo.py --method pos --webcam_id 0 --window_len 250

# Using CHROM algorithm
python src/realtime/webcam_demo.py --method chrom --webcam_id 0 --window_len 250

# Using Green-channel algorithm
python src/realtime/webcam_demo.py --method green --webcam_id 0 --window_len 250
```

### 4. Running Tests
Run pytest to verify metrics and algorithms:
```powershell
pytest
```

## Storage & Privacy Rules
- **Free Space Check**: Ensure at least 250 GB of free space is available before downloading datasets. If space is tight, use an external SSD.
- **Privacy Rule**: Do not store full-face raw video by default. The configuration flag `store_raw_video` is set to `false` by default. Only anonymous subject IDs, ROI traces, extracted RGB signals, predicted BVP signals, and metrics should be saved.
