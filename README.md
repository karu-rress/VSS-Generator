# Random VSS Generator

A simple, random [VSS](https://github.com/COVESA/vehicle_signal_specification) generator.

## Requirements
- python (>= 3.10)
- jsonpatch
- tqdm
- Tested with python=3.10 && jsonpatch 1.33 && tqdm 4.66

## Usage
```bash
python generate.py --n_cars=10 --n_files=20
```

### Arguments
- dataset (str): Path to VSS JSON dataset, default is ```'./vss_rel_4.2.json'```
- n_cars (int, required): Number of cars to generate
- n_files (int, required): Number of JSON files per car
- change_rate (float): Change rate for each car, default is 0.2
- size (float): Dataset size ratio 0.0-1.0, default is 1.0