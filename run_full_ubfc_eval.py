#!/usr/bin/env python
"""
Full UBFC Test Split Evaluation Pipeline
==========================================
Runs comprehensive evaluation for all methods (Green, POS, CHROM, PhysNet) on UBFC test split.

Usage:
    python run_full_ubfc_eval.py

Outputs:
    - outputs/reports/eval_*_ubfc_test.json (per-method metrics)
    - outputs/reports/eval_*_ubfc_test.csv (per-clip results)
    - outputs/plots/ (comparison charts and visualizations)
    - outputs/reports/evaluation_summary.md (summary report)
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_command(cmd, description):
    """Run a command and report status."""
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ ERROR: {description} failed with return code {result.returncode}")
        return False
    print(f"✅ SUCCESS: {description}")
    return True

def generate_summary_report():
    """Generate markdown summary report of all evaluations."""
    reports_dir = "outputs/reports"
    summary_path = os.path.join(reports_dir, "evaluation_summary.md")
    
    methods = ['physnet', 'green', 'pos', 'chrom']
    results = {}
    
    for method in methods:
        json_path = os.path.join(reports_dir, f'eval_{method}_ubfc_test.json')
        if os.path.exists(json_path):
            with open(json_path, 'r') as f:
                results[method.upper()] = json.load(f)
    
    if not results:
        print("⚠️  No evaluation results found!")
        return
    
    # Write summary
    with open(summary_path, 'w') as f:
        f.write("# UBFC Test Split - Comprehensive Evaluation Report\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Overall Performance Comparison\n\n")
        f.write("| Method | MAE (BPM) | RMSE (BPM) | Pearson r | Within 3 BPM | Within 5 BPM | BA Bias | BA LoA |\n")
        f.write("|--------|-----------|-----------|-----------|--------------|-------------|---------|--------|\n")
        
        for method in methods:
            if method.upper() in results:
                metrics = results[method.upper()]['overall']
                f.write(f"| {method.upper():8} | {metrics['mae']:9.2f} | {metrics['rmse']:9.2f} | {metrics['pearson']:9.4f} | {metrics['pct_within_3']:10.1f}% | {metrics['pct_within_5']:11.1f}% | {metrics['ba_bias']:+7.2f} | {metrics['ba_loa_lower']:+6.2f} to {metrics['ba_loa_upper']:+6.2f} |\n")
        
        f.write("\n## Key Findings\n\n")
        
        # Find best method per metric
        maes = {m: results[m]['overall']['mae'] for m in results}
        rmses = {m: results[m]['overall']['rmse'] for m in results}
        pearsons = {m: results[m]['overall']['pearson'] for m in results}
        within_3 = {m: results[m]['overall']['pct_within_3'] for m in results}
        
        if maes:
            best_mae = min(maes, key=maes.get)
            f.write(f"- **Best MAE**: {best_mae} ({maes[best_mae]:.2f} BPM)\n")
        
        if rmses:
            best_rmse = min(rmses, key=rmses.get)
            f.write(f"- **Best RMSE**: {best_rmse} ({rmses[best_rmse]:.2f} BPM)\n")
        
        if pearsons:
            best_pearson = max(pearsons, key=pearsons.get)
            f.write(f"- **Best Correlation**: {best_pearson} (r={pearsons[best_pearson]:.4f})\n")
        
        if within_3:
            best_within_3 = max(within_3, key=within_3.get)
            f.write(f"- **Best HR within 3 BPM**: {best_within_3} ({within_3[best_within_3]:.1f}%)\n")
        
        f.write("\n## Per-Subject Performance\n\n")
        for method in methods:
            if method.upper() in results and 'per_subject' in results[method.upper()]:
                f.write(f"### {method.upper()}\n\n")
                f.write("| Subject | Clips | MAE (BPM) | RMSE (BPM) |\n")
                f.write("|---------|-------|-----------|------------|\n")
                
                per_subj = results[method.upper()]['per_subject']
                for subject_id in sorted(per_subj.keys()):
                    metrics = per_subj[subject_id]
                    f.write(f"| {subject_id} | {metrics['num_clips']:5} | {metrics['mae']:9.2f} | {metrics['rmse']:10.2f} |\n")
                
                f.write("\n")
        
        f.write("## Visualizations\n\n")
        f.write("Generated plots saved to `outputs/plots/`:\n")
        f.write("- `ubfc_test_scatter_pred_vs_gt.png` - Predicted vs Ground Truth HR\n")
        f.write("- `ubfc_test_bland_altman.png` - Bland-Altman plot\n")
        f.write("- `ubfc_test_error_histogram.png` - Error distribution\n")
        f.write("- `ubfc_test_per_subject_mae.png` - Per-subject MAE comparison\n")
        f.write("- `classical_vs_deep_comparison.png` - Methods comparison chart\n")
        f.write("- `classical_*/` - Classical method specific plots\n")
    
    print(f"✅ Summary report saved: {summary_path}")

def main():
    os.chdir(Path(__file__).parent)
    
    print(f"\n{'='*70}")
    print(f"UBFC Full Evaluation Pipeline")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    # Ensure directories exist
    os.makedirs("outputs/reports", exist_ok=True)
    os.makedirs("outputs/plots", exist_ok=True)
    
    # 1. Evaluate PhysNet
    success = run_command(
        "python -m src.evaluation.evaluate --dataset ubfc --split test --checkpoint outputs/models/physnet_ubfc_best.pt",
        "1. Evaluating PhysNet on UBFC Test Split"
    )
    if not success:
        print("⚠️  PhysNet evaluation failed, continuing with classical methods...")
    
    # 2. Evaluate Green
    success = run_command(
        "python -m src.evaluation.evaluate_classical --dataset ubfc --method green --split test",
        "2. Evaluating Green (Classical) on UBFC Test Split"
    )
    if not success:
        print("⚠️  Green evaluation failed")
    
    # 3. Evaluate POS
    success = run_command(
        "python -m src.evaluation.evaluate_classical --dataset ubfc --method pos --split test",
        "3. Evaluating POS (Classical) on UBFC Test Split"
    )
    if not success:
        print("⚠️  POS evaluation failed")
    
    # 4. Evaluate CHROM
    success = run_command(
        "python -m src.evaluation.evaluate_classical --dataset ubfc --method chrom --split test",
        "4. Evaluating CHROM (Classical) on UBFC Test Split"
    )
    if not success:
        print("⚠️  CHROM evaluation failed")
    
    # 5. Generate comparison chart
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 5. Generating Comparison Chart")
    print(f"{'='*70}")
    try:
        from src.evaluation.compare_models import compare_models
        compare_models("outputs/reports", "outputs/plots")
        print("✅ Comparison chart generated")
    except Exception as e:
        print(f"⚠️  Comparison chart generation failed: {e}")
    
    # 6. Generate summary report
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 6. Generating Summary Report")
    print(f"{'='*70}")
    generate_summary_report()
    
    print(f"\n{'='*70}")
    print(f"✅ EVALUATION PIPELINE COMPLETE")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    print(f"\nResults saved to:")
    print(f"  - outputs/reports/eval_*.json (per-method metrics)")
    print(f"  - outputs/reports/eval_*.csv (per-clip results)")
    print(f"  - outputs/reports/evaluation_summary.md (comprehensive report)")
    print(f"  - outputs/plots/ (all visualizations)")

if __name__ == '__main__':
    main()
