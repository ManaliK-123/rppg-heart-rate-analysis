#!/usr/bin/env python
"""
Post-Training Verification Checklist
====================================
Comprehensive verification after PhysNet recovery training completes.

Usage:
    python verify_training_complete.py

Checks:
1. Checkpoint files exist and are non-empty
2. Training history CSV is complete
3. Training curves can be plotted
4. Ready for evaluation
"""

import os
import json
import csv
from pathlib import Path
from datetime import datetime

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_file_exists_and_nonempty(filepath, description):
    """Check if a file exists and is non-empty."""
    if not os.path.exists(filepath):
        print(f"❌ FAILED: {description}")
        print(f"   File not found: {filepath}")
        return False
    
    size = os.path.getsize(filepath)
    if size == 0:
        print(f"❌ FAILED: {description}")
        print(f"   File is empty: {filepath}")
        return False
    
    print(f"✅ PASSED: {description}")
    print(f"   Location: {filepath}")
    print(f"   Size: {size:,} bytes")
    return True

def verify_checkpoint_integrity():
    """Verify checkpoint files can be loaded."""
    print_section("Checkpoint Integrity Check")
    
    try:
        import torch
        checkpoint_path = "outputs/models/physnet_ubfc_best.pt"
        
        if not os.path.exists(checkpoint_path):
            print(f"❌ FAILED: Checkpoint not found at {checkpoint_path}")
            return False
        
        checkpoint = torch.load(checkpoint_path, map_location='cpu')
        print(f"✅ Checkpoint loaded successfully")
        print(f"   Keys: {', '.join(checkpoint.keys())}")
        
        if 'model_state_dict' not in checkpoint:
            print(f"❌ FAILED: 'model_state_dict' not found in checkpoint")
            return False
        
        print(f"✅ Model state dict present")
        print(f"   Number of parameters: {len(checkpoint['model_state_dict'])}")
        
        return True
    except Exception as e:
        print(f"❌ ERROR loading checkpoint: {e}")
        return False

def verify_training_history():
    """Verify training history CSV is complete."""
    print_section("Training History Verification")
    
    history_path = "outputs/reports/train_history.csv"
    
    if not os.path.exists(history_path):
        print(f"❌ FAILED: Training history not found at {history_path}")
        return False
    
    try:
        with open(history_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        print(f"✅ Training history loaded")
        print(f"   Total epochs: {len(rows)}")
        
        if len(rows) == 0:
            print(f"⚠️  WARNING: No training epochs recorded")
            return False
        
        # Print summary of first and last epoch
        first_epoch = rows[0]
        last_epoch = rows[-1]
        
        print(f"\n   First epoch:")
        print(f"     Epoch: {first_epoch.get('epoch', 'N/A')}")
        print(f"     Train Loss: {first_epoch.get('train_loss', 'N/A')}")
        print(f"     Val Loss: {first_epoch.get('val_loss', 'N/A')}")
        print(f"     MAE: {first_epoch.get('mae', 'N/A')} BPM")
        
        print(f"\n   Last epoch:")
        print(f"     Epoch: {last_epoch.get('epoch', 'N/A')}")
        print(f"     Train Loss: {last_epoch.get('train_loss', 'N/A')}")
        print(f"     Val Loss: {last_epoch.get('val_loss', 'N/A')}")
        print(f"     MAE: {last_epoch.get('mae', 'N/A')} BPM")
        print(f"     Pearson r: {last_epoch.get('pearson', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"❌ ERROR reading training history: {e}")
        return False

def verify_dataset_accessibility():
    """Verify UBFC dataset is still accessible."""
    print_section("Dataset Accessibility Check")
    
    raw_dir = "D:\\dataset"
    
    if not os.path.exists(raw_dir):
        print(f"❌ FAILED: Dataset not found at {raw_dir}")
        return False
    
    print(f"✅ Dataset directory exists: {raw_dir}")
    
    # Count subject directories
    subjects = [d for d in os.listdir(raw_dir) if os.path.isdir(os.path.join(raw_dir, d))]
    print(f"   Total subjects: {len(subjects)}")
    
    # Verify test split subjects exist
    test_subjects = ['subject12', 'subject18', 'subject20', 'subject23', 'subject3', 'subject11', 'subject48']
    test_found = [s for s in test_subjects if s in subjects]
    print(f"   Test subjects found: {len(test_found)}/{len(test_subjects)}")
    
    if len(test_found) == len(test_subjects):
        print(f"✅ All test subjects accessible")
        return True
    else:
        print(f"⚠️  Missing test subjects: {set(test_subjects) - set(test_found)}")
        return False

def verify_configs():
    """Verify config files are correct."""
    print_section("Configuration Verification")
    
    import yaml
    
    configs_to_check = {
        'configs/default.yaml': ['training', 'directories'],
        'configs/ubfc.yaml': ['dataset_name', 'raw_dir', 'splits'],
    }
    
    all_ok = True
    for config_path, required_keys in configs_to_check.items():
        if not os.path.exists(config_path):
            print(f"❌ Config not found: {config_path}")
            all_ok = False
            continue
        
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            missing = [k for k in required_keys if k not in config]
            if missing:
                print(f"❌ Missing keys in {config_path}: {missing}")
                all_ok = False
            else:
                print(f"✅ {config_path} is valid")
        except Exception as e:
            print(f"❌ Error reading {config_path}: {e}")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """Print final summary."""
    print_section("Final Verification Summary")
    
    passed = sum(results.values())
    total = len(results)
    pct = (passed / total * 100) if total > 0 else 0
    
    print(f"Results: {passed}/{total} checks passed ({pct:.0f}%)\n")
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {check_name}")
    
    if passed == total:
        print(f"\n🎉 All verification checks passed! Ready for evaluation.")
        print(f"\nNext step: Run the full evaluation pipeline:")
        print(f"  python run_full_ubfc_eval.py")
    else:
        print(f"\n⚠️  Some checks failed. Please review the issues above.")

def main():
    print(f"\n{'='*70}")
    print(f"Post-Training Verification Checklist")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    results = {
        'Checkpoint Best': check_file_exists_and_nonempty('outputs/models/physnet_ubfc_best.pt', 'Best checkpoint exists'),
        'Checkpoint Latest': check_file_exists_and_nonempty('outputs/models/physnet_ubfc_latest.pt', 'Latest checkpoint exists'),
        'Training History': check_file_exists_and_nonempty('outputs/reports/train_history.csv', 'Training history exists'),
        'Checkpoint Integrity': verify_checkpoint_integrity(),
        'Training History Content': verify_training_history(),
        'Dataset Accessible': verify_dataset_accessibility(),
        'Configs Valid': verify_configs(),
    }
    
    print_summary(results)
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return 0 if sum(results.values()) == len(results) else 1

if __name__ == '__main__':
    exit(main())
