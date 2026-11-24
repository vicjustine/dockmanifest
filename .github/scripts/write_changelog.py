"""Write a CHANGELOG section and release notes for a new version. 

Collects commit subject since the last tag. """

import subprocess
import sys
from datetime import date
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
NOTES = Path(".github/release-notes.md")

def run(args):
    done = subprocess.run(args, capture_output=True, text=True)
    return done.stdout.strip() if done.returncode == 0 else ""

def subjects(): 
    tag = run(["git", "describe", "--tags", "--abbrev=0"])
    span = f"{tag}..HEAD" if tag else "HEAD" 
    log = run(["git", "log", "--no-merges", "--pretty=format:%s", span])
    lines = [s for s in log.splitlines() if s]
    return [s for s in lines if not s.startswith("Release v")]

def main(): 
    version = sys.argv[1]
    entries = subjects() or ["Maintenance release."]
    body = "\n".join(f"- {line}" for line in entries)

    heading = f"## [{version}] - {date.today().isoformat()}"
    section = f"{heading}\n\n### Changed\n\n{body}\n"

    old = CHANGELOG.read_text()
    marker = "file.\n"
    head, _, tail = old.partition(marker)
    CHANGELOG.write_text(f"{head}{marker}\n{section}\n{tail.strip()}\n")

    NOTES.write_text(f"## What changed\n\n{body}\n")
    print(f"changelog updated for {version}")

if __name__ == "__main__": 
    main()

                      
    
    
