#!/usr/bin/env python3
import os
import json
import requests
from github import Github

# Configuration
SOURCE_REPO = "ScoopInstaller/Main"  # Repository to fetch from
TARGET_DIR = "bucket"  # Directory where JSON files are stored
OUTPUT_FILE = "aggregated.json"  # Output file name

def main():
    # Initialize GitHub API client
    token = os.environ.get("GITHUB_TOKEN")
    g = Github(token)
    
    # Get the source repository
    source_repo = g.get_repo(SOURCE_REPO)
    
    # Get contents of the bucket directory
    contents = source_repo.get_contents(TARGET_DIR)
    
    # Store all JSON data
    all_data = {}
    
    # Process each file in the bucket directory
    for content_file in contents:
        if content_file.name.endswith('.json'):
            try:
                # Get raw content
                raw_content = requests.get(content_file.download_url).text
                
                # Parse JSON
                json_data = json.loads(raw_content)
                
                # Add to aggregated data
                app_name = os.path.splitext(content_file.name)[0]
                all_data[app_name] = json_data
                
                print(f"Processed: {content_file.name}")
            except Exception as e:
                print(f"Error processing {content_file.name}: {str(e)}")
    
    # Save aggregated data to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Successfully aggregated {len(all_data)} JSON files to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()