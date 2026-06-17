#!/usr/bin/env python
"""
Master Post-Training Execution Pipeline
========================================
Orchestrates the complete post-training verification and evaluation.

Usage:
    python post_training_pipeline.py

Pipeline:
1. Verify training completion
2. Run comprehensive evaluation (PhysNet + Classical methods)
3. Generate comparison reports and visualizations
4. Create final summary document
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

def run_script(script_path, description):
    """Run a Python script and report status."""
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {description}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=Path(script_path).parent,
            capture_output=False
        )
        if result.returncode == 0:
            print(f"✅ SUCCESS: {description}")
            return True
        else:
            print(f"❌ FAILED: {description} (return code: {result.returncode})")
            return False
    except Exception as e:
        print(f"❌ ERROR running {description}: {e}")
        return False

def main():
    os.chdir(Path(__file__).parent)
    
    print(f"\n{'='*70}")
    print(f"POST-TRAINING EXECUTION PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    steps = [
        ('verify_training_complete.py', '1️⃣  Verifying Training Completion'),
        ('run_full_ubfc_eval.py', '2️⃣  Running Comprehensive Evaluation'),
    ]
    
    results = []
    for script_path, description in steps:
        success = run_script(script_path, description)
        results.append((description, success))
    
    # Print summary
    print(f"\n{'='*70}")
    print(f"PIPELINE EXECUTION SUMMARY")
    print(f"{'='*70}\n")
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    passed = sum(1 for _, s in results if s)
    total = len(results)
    
    print(f"\nResults: {passed}/{total} steps completed successfully")
    
    if passed == total:
        print(f"\n🎉 POST-TRAINING PIPELINE COMPLETE!")
        print(f"\nFinal outputs:")
        print(f"  📊 Evaluation reports: outputs/reports/eval_*.json")
        print(f"  📈 Training curves: outputs/reports/train_history.csv")
        print(f"  🖼️  Visualizations: outputs/plots/")
        print(f"  📝 Summary report: outputs/reports/evaluation_summary.md")
    else:
        print(f"\n⚠️  Some steps failed. Review the output above.")
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return 0 if passed == total else 1

if __name__ == '__main__':
    exit(main())
