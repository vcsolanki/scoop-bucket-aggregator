#!/usr/bin/env python3
import os
import json
import requests
from github import Github

# Configuration
# List of repositories to fetch from, each with their target directory
SOURCE_REPOS = [
    {"repo": "ScoopInstaller/Main", "dir": "bucket"},
    {"repo": "ScoopInstaller/Extras", "dir": "bucket"},
    {"repo": "ScoopInstaller/Java", "dir": "bucket"}
    # Add more repositories as needed:
    # {"repo": "owner/repo", "dir": "bucket_folder"},
    # {"repo": "another_owner/another_repo", "dir": "json_folder"},
]
OUTPUT_FILE = "aggregated.json"  # Output file name

def main():
    # Initialize GitHub API client
    token = os.environ.get("GITHUB_TOKEN")
    g = Github(token)
    
    # Store all JSON data
    all_data = {}
    
    # Process each repository
    for source in SOURCE_REPOS:
        repo_name = source["repo"]
        target_dir = source["dir"]
        
        print(f"Processing repository: {repo_name}, directory: {target_dir}")
        
        # Get the source repository
        source_repo = g.get_repo(repo_name)
        
        try:
            # Get contents of the target directory
            contents = source_repo.get_contents(target_dir)
            
            # Process each file in the directory
            for content_file in contents:
                if content_file.name.endswith('.json'):
                    try:
                        # Get raw content
                        raw_content = requests.get(content_file.download_url).text
                        
                        # Parse JSON
                        json_data = json.loads(raw_content)
                        
                        # Add to aggregated data with repo as namespace
                        repo_short_name = repo_name.split('/')[1]
                        app_name = os.path.splitext(content_file.name)[0]
                        key = f"{repo_short_name}/{app_name}"
                        all_data[key] = json_data
                        
                        print(f"Processed: {key}")
                    except Exception as e:
                        print(f"Error processing {content_file.name} from {repo_name}: {str(e)}")
        
        except Exception as e:
            print(f"Error accessing directory {target_dir} in {repo_name}: {str(e)}")
    
    # Save aggregated data to file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Successfully aggregated {len(all_data)} JSON files to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
