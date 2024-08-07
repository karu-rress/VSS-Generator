#
# generate.py
#
# Generates a JSON / JSON patch dataset of cars
# using the VSS dataset.
#

import os
import shutil
import argparse
from tqdm import tqdm
from pathlib import Path
from vss import vss_json

OUTPUT_DIR = Path('./output')

def main(args):
    print('Running with arguments:')
    print('--dataset:', args.dataset)
    print('--n_cars:', args.n_cars)
    print('--n_files:', args.n_files)
    print('--change_rate:', args.change_rate)
    print('--size:', args.size, end='\n\n')
    
    # Remove output directory if it exists
    print('Checking for existing output directory...', end='', flush=True)
    if OUTPUT_DIR.exists() and OUTPUT_DIR.is_dir():
        print('\nDirectory found. Removing...', end='', flush=True)
        shutil.rmtree(OUTPUT_DIR)
        print('removed successfully.\n')
    else:
        print('not found.\n')
    
    # Generate dataset
    print(f'Generating {args.n_cars} cars with {args.n_files} files each...')
    vss = vss_json(file=args.dataset)
    
    with tqdm(total=args.n_cars*args.n_files, desc='Progress') as pbar:
        for i in range(1, args.n_cars + 1):
            # Create directories
            car_dir = OUTPUT_DIR / f'car_{i}'
            patch_dir = OUTPUT_DIR / f'car_{i}/patches'

            if not car_dir.exists():
                car_dir.mkdir(parents=True)
            if not patch_dir.exists():
                patch_dir.mkdir(parents=True)
                
            # Generate first (randomized) data and patch
            data, patch = vss.generate(args.size)
            data.save(car_dir / f'{i}_1.json')
            patch.save(patch_dir / f'{i}_1.json')
            pbar.update(1)

            # Generate the rest of the files
            for j in range(2, args.n_files + 1):
                data, patch = data.generate_next(args.change_rate)
                data.save(car_dir / f'{i}_{j}.json')
                patch.save(patch_dir / f'{i}_{j}.json')
                pbar.update(1)

    print(f'Saved to {OUTPUT_DIR.absolute()}! Exiting...')
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='./vss_rel_4.2.json', help='Path to VSS JSON dataset')
    parser.add_argument('--n_cars', type=int, required=True, help='Number of cars to generate')
    parser.add_argument('--n_files', type=int, required=True, help='Number of JSON files per car')
    parser.add_argument('--change_rate', type=float, default=0.2, help='Change rate for each car')
    parser.add_argument('--size', type=float, default=1.0, help='Dataset size ratio 0.0-1.0')
    
    main(parser.parse_args())