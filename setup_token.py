import os
import getpass
from pathlib import Path

def setup_token():
    print("Please enter your GitHub token (it won't be displayed):")
    token = getpass.getpass()
    
    # Create .env file
    env_file = Path('.env')
    env_file.write_text(f'GITHUB_TOKEN={token}\n')
    
    # Set environment variable for current session
    os.environ['GITHUB_TOKEN'] = token
    
    print("\nToken has been saved to .env file and set for current session.")
    print("You can now run: python create_release.py")

if __name__ == '__main__':
    setup_token() 