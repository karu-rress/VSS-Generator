import os
import shutil
import argparse
from tqdm import tqdm
from vss import vss_json

OUTPUT_DIR = './output'

def main(args):
    print('Running with arguments:')
    print('--dataset:', args.dataset)
    print('--n_cars:', args.n_cars)
    print('--n_files:', args.n_files)
    print('--change_rate:', args.change_rate)
    print('--size:', args.size, end='\n\n')
    
    # Remove output directory if it exists
    if os.path.exists(OUTPUT_DIR) and os.path.isdir(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
        print(f'Removed existing output directory.\n')
        
    print(f'Generating {args.n_cars} cars with {args.n_files} files each...')
    vss = vss_json(file=args.dataset)
    
    total_iterations = args.n_cars * (args.n_files - 1)
    with tqdm(total=total_iterations, desc='Progress') as pbar:
        for i in range(1, args.n_cars + 1):
            # Create directories
            if not os.path.exists(f'{OUTPUT_DIR}/car_{i}'):
                os.makedirs(f'{OUTPUT_DIR}/car_{i}')
            if not os.path.exists(f'{OUTPUT_DIR}/car_{i}/patches'):
                os.makedirs(f'{OUTPUT_DIR}/car_{i}/patches')
                
            # Generate first data and patch
            data, patch = vss.generate(args.size)
            data.save(f'{OUTPUT_DIR}/car_{i}/{i}_1.json')
            patch.save(f'{OUTPUT_DIR}/car_{i}/patches/{i}_1.json')
            
            # Generate the rest of the files
            for j in range(2, args.n_files + 1):
                data, patch = data.generate_next(args.change_rate)
                data.save(f'{OUTPUT_DIR}/car_{i}/{i}_{j}.json')
                patch.save(f'{OUTPUT_DIR}/car_{i}/patches/{i}_{j}.json')
                pbar.update(1)
            pbar.update(1)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, default='./vss_rel_4.2.json', help='Path to VSS JSON dataset')
    parser.add_argument('--n_cars', type=int, required=True, help='Number of cars to generate')
    parser.add_argument('--n_files', type=int, required=True, help='Number of JSON files per car')
    parser.add_argument('--change_rate', type=float, default=0.2, help='Change rate for each car')
    parser.add_argument('--size', type=float, default=1.0, help='Dataset size ratio 0.0-1.0')
    
    main(parser.parse_args())