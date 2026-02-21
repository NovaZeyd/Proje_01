#!/usr/bin/env python3
"""
Context Compaction Helper
Summarizes conversation history and writes to memory files.
Usage: python3 compact.py [--memory-path PATH] [--project NAME]
"""
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

def create_checkpoint(project=None):
    """Generate checkpoint summary structure."""
    timestamp = datetime.now().isoformat()
    
    checkpoint = {
        "timestamp": timestamp,
        "type": "checkpoint",
        "project": project or "general",
        "summary_prompt": """
Summarize the conversation since the last checkpoint. Include:
1. Key decisions made
2. Code/files created or modified  
3. Problems identified and solutions
4. Next steps / open items

Format: Short bullet points, 200-500 words max.
"""
    }
    
    return checkpoint

def get_memory_path(project=None):
    """Determine memory file path."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    if project:
        project_dir = Path.home() / f".openclaw/workspace/projects/{project}"
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir / "memory.md"
    else:
        memory_dir = Path.home() / ".openclaw/workspace/memory"
        memory_dir.mkdir(exist_ok=True)
        return memory_dir / f"{today}.md"

def main():
    parser = argparse.ArgumentParser(description="Context compaction helper")
    parser.add_argument("--project", help="Project name (optional)")
    parser.add_argument("--print-only", action="store_true", help="Print template only")
    args = parser.parse_args()
    
    checkpoint = create_checkpoint(args.project)
    
    if args.print_only:
        print(json.dumps(checkpoint, indent=2))
        return
    
    # Write summary template to memory
    memory_path = get_memory_path(args.project)
    
    print(f"Memory path: {memory_path}")
    print(f"\nCheckpoint template ready.")
    print(json.dumps(checkpoint, indent=2))

if __name__ == "__main__":
    main()
