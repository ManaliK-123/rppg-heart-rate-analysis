import yaml

with open('data/splits/train.txt') as f: train = [l.strip() for l in f if l.strip()]
with open('data/splits/val.txt') as f: val = [l.strip() for l in f if l.strip()]
with open('data/splits/test.txt') as f: test = [l.strip() for l in f if l.strip()]

with open('configs/ubfc.yaml', 'r') as f: 
    c = yaml.safe_load(f)

c['raw_dir'] = 'D:\\dataset'
c['splits']['train'] = train
c['splits']['val'] = val
c['splits']['test'] = test

with open('configs/ubfc.yaml', 'w') as f: 
    yaml.dump(c, f, sort_keys=False)
print("Updated ubfc.yaml with new splits and raw_dir")
