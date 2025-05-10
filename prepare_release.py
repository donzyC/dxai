import pandas as pd
import os
from pathlib import Path

def convert_to_json():
    """Convert all CSV files to JSON format."""
    release_dir = Path("release_files")
    release_dir.mkdir(exist_ok=True)
    
    # Convert CSV files to JSON
    csv_files = [
        'symptoms_df.csv',
        'precautions_df.csv',
        'workout_df.csv',
        'description.csv',
        'medications.csv',
        'diets.csv'
    ]
    
    for csv_file in csv_files:
        if os.path.exists(f'datasets/{csv_file}'):
            df = pd.read_csv(f'datasets/{csv_file}')
            json_file = csv_file.replace('.csv', '.json')
            df.to_json(release_dir / json_file, orient='records')
    
    # Copy model file
    if os.path.exists('models/svc.pkl'):
        with open('models/svc.pkl', 'rb') as src, open(release_dir / 'svc.pkl', 'wb') as dst:
            dst.write(src.read())

if __name__ == '__main__':
    convert_to_json()
    print("Release files prepared in 'release_files' directory") 