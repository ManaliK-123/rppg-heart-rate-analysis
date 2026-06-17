#!/usr/bin/env python
"""
Training Monitoring and Management Console
===========================================
Interactive console for monitoring training progress and executing post-training tasks.

Usage:
    python monitor.py

Options:
    [1] Check training progress
    [2] View latest log entries
    [3] Check training loss trend
    [4] Verify dataset accessibility
    [5] Run post-training pipeline (ONLY if training is complete)
    [6] Exit
"""

import os
import csv
import subprocess
import time
from datetime import datetime
from pathlib import Path

class TrainingMonitor:
    def __init__(self):
        self.log_path = "recovery_training.log"
        self.history_path = "outputs/reports/train_history.csv"
        self.checkpoint_best = "outputs/models/physnet_ubfc_best.pt"
        self.checkpoint_latest = "outputs/models/physnet_ubfc_latest.pt"
    
    def print_header(self, title):
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    
    def check_progress(self):
        """Check current training progress."""
        self.print_header("Training Progress")
        
        if not os.path.exists(self.log_path):
            print("❌ Log file not found. Training may not have started.")
            return
        
        # Get last 5 lines from log
        try:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()[-10:]
            
            for line in lines:
                if "Training:" in line or "Epoch" in line or "Validation" in line:
                    print(line.strip())
        except Exception as e:
            print(f"❌ Error reading log file: {e}")
    
    def view_logs(self):
        """Display latest log entries."""
        self.print_header("Latest Log Entries (Last 30 lines)")
        
        if not os.path.exists(self.log_path):
            print("❌ Log file not found.")
            return
        
        try:
            with open(self.log_path, 'r') as f:
                lines = f.readlines()[-30:]
            
            for line in lines:
                print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading log: {e}")
    
    def check_loss_trend(self):
        """Check training loss trend from CSV."""
        self.print_header("Training History (Loss Trend)")
        
        if not os.path.exists(self.history_path):
            print("⏳ Training history not yet available (waiting for first epoch to complete)")
            return
        
        try:
            with open(self.history_path, 'r') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if not rows:
                print("⏳ No training epochs recorded yet")
                return
            
            print(f"Total epochs recorded: {len(rows)}\n")
            print("Epoch | Train Loss | Val Loss | MAE (BPM) | RMSE (BPM) | Pearson r | Within 3 BPM")
            print("-" * 85)
            
            for row in rows[-10:]:  # Show last 10
                epoch = row.get('epoch', 'N/A')
                train_loss = row.get('train_loss', 'N/A')
                val_loss = row.get('val_loss', 'N/A')
                mae = row.get('mae', 'N/A')
                rmse = row.get('rmse', 'N/A')
                pearson = row.get('pearson', 'N/A')
                within_3 = row.get('pct_within_3', 'N/A')
                
                print(f"{epoch:>5} | {train_loss:>10} | {val_loss:>8} | {mae:>9} | {rmse:>10} | {pearson:>9} | {within_3:>12}")
            
            # Show summary statistics
            if len(rows) > 1:
                print("\nTrend Analysis:")
                first_val_loss = float(rows[0]['val_loss'])
                last_val_loss = float(rows[-1]['val_loss'])
                improvement = ((first_val_loss - last_val_loss) / first_val_loss) * 100
                print(f"  Val Loss Improvement: {improvement:+.1f}%")
                print(f"  Current Val Loss: {last_val_loss:.6f}")
                
        except Exception as e:
            print(f"❌ Error reading training history: {e}")
    
    def verify_dataset(self):
        """Verify dataset accessibility."""
        self.print_header("Dataset Verification")
        
        dataset_path = "D:\\dataset"
        
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset not found at {dataset_path}")
            return
        
        print(f"✅ Dataset found at {dataset_path}")
        
        # Count subjects
        try:
            subjects = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]
            print(f"   Total subjects: {len(subjects)}")
            
            # Verify test split
            test_subjects = ['subject12', 'subject18', 'subject20', 'subject23', 'subject3', 'subject11', 'subject48']
            test_found = [s for s in test_subjects if s in subjects]
            print(f"   Test subjects available: {len(test_found)}/{len(test_subjects)}")
            
            if len(test_found) == len(test_subjects):
                print("   ✅ All test subjects accessible - ready for evaluation")
            
        except Exception as e:
            print(f"❌ Error scanning dataset: {e}")
    
    def check_training_complete(self):
        """Check if training has completed."""
        if not os.path.exists(self.log_path):
            return False
        
        try:
            with open(self.log_path, 'r') as f:
                content = f.read()
            
            if "Training completed successfully!" in content:
                return True
            
            # Also check for epoch 20 completion
            if "--- Epoch 20/" in content:
                return True
        except:
            pass
        
        return False
    
    def run_post_pipeline(self):
        """Run post-training pipeline."""
        self.print_header("Post-Training Pipeline")
        
        if not self.check_training_complete():
            print("❌ Training does not appear to be complete yet.")
            print("   Check the log file or come back later.")
            return
        
        confirm = input("Start post-training evaluation pipeline? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            return
        
        print("\nStarting post-training pipeline...\n")
        try:
            result = subprocess.run(
                ["python", "post_training_pipeline.py"],
                cwd=Path(__file__).parent
            )
            if result.returncode == 0:
                print("\n✅ Post-training pipeline completed successfully!")
                print("   Check outputs/reports/evaluation_summary.md for results")
            else:
                print(f"\n❌ Post-training pipeline failed with return code {result.returncode}")
        except Exception as e:
            print(f"❌ Error running pipeline: {e}")
    
    def interactive_menu(self):
        """Show interactive menu."""
        while True:
            print("\n" + "="*70)
            print("  Training Monitoring Console")
            print("="*70)
            print("\nOptions:")
            print("  [1] Check training progress")
            print("  [2] View latest log entries")
            print("  [3] Check training loss trend")
            print("  [4] Verify dataset accessibility")
            print("  [5] Run post-training pipeline")
            print("  [6] Exit")
            print()
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.check_progress()
            elif choice == '2':
                self.view_logs()
            elif choice == '3':
                self.check_loss_trend()
            elif choice == '4':
                self.verify_dataset()
            elif choice == '5':
                self.run_post_pipeline()
            elif choice == '6':
                print("\nGoodbye!")
                break
            else:
                print("❌ Invalid option. Try again.")
            
            input("\nPress Enter to continue...")

def main():
    os.chdir(Path(__file__).parent)
    monitor = TrainingMonitor()
    
    print(f"\n{'='*70}")
    print(f"  PhysNet Recovery Training Monitor")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    
    monitor.interactive_menu()

if __name__ == '__main__':
    main()
