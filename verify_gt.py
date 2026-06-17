import os
import glob
import numpy as np

def verify_ground_truth(base_dir="D:\\dataset"):
    print(f"Verifying ground truth files in {base_dir}")
    subject_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for sub in subject_dirs[:3]:  # Check first 3 subjects
        sub_path = os.path.join(base_dir, sub)
        gt_paths = glob.glob(os.path.join(sub_path, "ground_truth*.txt")) + glob.glob(os.path.join(sub_path, "gnd_txt*.txt"))
        if not gt_paths:
            print(f"  [!] Missing ground truth in {sub}")
            continue
            
        gt_path = gt_paths[0]
        try:
            with open(gt_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if not lines:
                print(f"  [!] Empty ground truth in {sub}")
                continue
                
            first_line_parts = lines[0].split()
            if len(first_line_parts) > 10:
                print(f"  [OK] {sub}: Row style detected. Rows: {len(lines)}, Cols per row: {len(first_line_parts)}")
                trace = np.array([float(val) for val in lines[0].split()], dtype=np.float32)
                hr = np.array([float(val) for val in lines[1].split()], dtype=np.float32) if len(lines) > 1 else None
                time = np.array([float(val) for val in lines[2].split()], dtype=np.float32) if len(lines) > 2 else None
            else:
                print(f"  [OK] {sub}: Column style detected. Rows: {len(lines)}, Cols per row: {len(first_line_parts)}")
                trace = np.array([float(line.split()[0]) for line in lines], dtype=np.float32)
                hr = np.array([float(line.split()[1]) for line in lines if len(line.split()) > 1], dtype=np.float32)
                time = np.array([float(line.split()[2]) for line in lines if len(line.split()) > 2], dtype=np.float32)
                
            print(f"       Trace length: {len(trace)}, HR length: {len(hr) if hr is not None else 0}, Time length: {len(time) if time is not None else 0}")
            print(f"       Sample Trace[0:3]: {trace[:3]}")
            if hr is not None and len(hr) > 0: print(f"       Sample HR[0:3]: {hr[:3]}")
            if time is not None and len(time) > 0: print(f"       Sample Time[0:3]: {time[:3]}")
        except Exception as e:
            print(f"  [!] Error parsing {sub}: {e}")

if __name__ == "__main__":
    verify_ground_truth()
