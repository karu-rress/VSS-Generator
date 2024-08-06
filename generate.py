import argparse
from vss import vss_json
import os
import shutil

OUTPUT_DIR = './output'

def main(args):
    # Remove output directory if it exists
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        
    vss = vss_json(file=args.dataset)
    for i in range(1, args.n_cars + 1):
        car = vss.generate(args.size)
        if not os.path.exists(f'{OUTPUT_DIR}/car_{i}'):
            os.makedirs(f'{OUTPUT_DIR}/car_{i}')
        car.save(f'{OUTPUT_DIR}/car_{i}/{i}_1.json')
        
        for j in range(2, args.n_files + 1):
            car = car.generate_next(args.change_rate)
            car.save(f'{OUTPUT_DIR}/car_{i}/{i}_{j}.json')
            
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='./vss_rel_4.2.json', help='Path to VSS JSON dataset')
    parser.add_argument('--n_cars', type=int, required=True, help='Number of cars to generate')
    parser.add_argument('--n_files', type=int, required=True, help='Number of JSON files per car')
    parser.add_argument('--change_rate', type=float, default=0.2, help='Change rate for each car')
    parser.add_argument('--size', type=float, default=1.0, help='Dataset size ratio 0.0-1.0')
    
    main(parser.parse_args())