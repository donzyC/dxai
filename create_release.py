import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

def create_release():
    # Load environment variables from .env file
    load_dotenv()
    
    # GitHub API endpoint
    api_url = "https://api.github.com/repos/donzyC/dxai/releases"
    
    # Get GitHub token from environment variable
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Please set GITHUB_TOKEN environment variable")
        print("Run: python setup_token.py")
        return
    
    # Headers for authentication
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Create release
    release_data = {
        'tag_name': 'v1.0.0',
        'name': 'Initial Release',
        'body': 'Initial release with model and data files for Vercel deployment',
        'draft': False,
        'prerelease': False
    }
    
    print("Creating release...")
    # Create the release
    response = requests.post(api_url, headers=headers, json=release_data)
    if response.status_code != 201:
        print(f"Failed to create release: {response.text}")
        return
    
    release = response.json()
    upload_url = release['upload_url'].split('{')[0]
    
    print("\nUploading files...")
    # Upload files
    release_files = Path('release_files')
    for file_path in release_files.glob('*'):
        if file_path.is_file():
            print(f"Uploading {file_path.name}...")
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Upload file
            upload_response = requests.post(
                f"{upload_url}?name={file_path.name}",
                headers={
                    **headers,
                    'Content-Type': 'application/octet-stream'
                },
                data=file_data
            )
            
            if upload_response.status_code == 201:
                print(f"✓ Uploaded {file_path.name}")
            else:
                print(f"✗ Failed to upload {file_path.name}: {upload_response.text}")
    
    print("\nRelease created successfully!")
    print(f"Release URL: {release['html_url']}")

if __name__ == '__main__':
    create_release() 