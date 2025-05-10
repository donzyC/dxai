import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv
import base64

def upload_to_gist():
    # Load environment variables
    load_dotenv()
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        return

    # Headers for authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Create a new gist
    gist_data = {
        'description': 'DXAI Model and Data Files',
        'public': True,
        'files': {}
    }

    # Add files to gist
    release_files = Path('release_files')
    for file_path in release_files.glob('*'):
        if file_path.is_file():
            with open(file_path, 'rb') as f:
                content = f.read()
                if file_path.suffix == '.pkl':
                    # Convert binary file to base64
                    content = base64.b64encode(content).decode('utf-8')
                else:
                    # Convert text file to string
                    content = content.decode('utf-8')
                
                gist_data['files'][file_path.name] = {
                    'content': content
                }

    # Create the gist
    response = requests.post(
        'https://api.github.com/gists',
        headers=headers,
        json=gist_data
    )

    if response.status_code == 201:
        gist = response.json()
        print(f"\nGist created successfully!")
        print(f"Gist URL: {gist['html_url']}")
        print(f"Raw URL: {gist['files'][list(gist['files'].keys())[0]]['raw_url'].rsplit('/', 1)[0]}")
        
        # Update main.py with the new Gist URL
        with open('main.py', 'r') as f:
            content = f.read()
        
        gist_url = gist['files'][list(gist['files'].keys())[0]]['raw_url'].rsplit('/', 1)[0]
        content = content.replace('your-gist-id', gist_url.split('/')[-2])
        
        with open('main.py', 'w') as f:
            f.write(content)
        
        print("\nUpdated main.py with the new Gist URL")
    else:
        print(f"Failed to create gist: {response.text}")

if __name__ == '__main__':
    upload_to_gist() 