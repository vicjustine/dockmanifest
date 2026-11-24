""" Raise the verison in pyproject.toml and in the package __init__.
Prints 'version=<new> so the workflow can read it form GITHUB_OUTPUT. 
"""

import re
import sys
from pathlib import Path 

PYPROJECT = Path("pyproject.toml")
INIT = Path("src/dockmanifest/__init__.py")

def bump(old, part): 
    major, minor, patch = (int(n) for n in old.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor": 
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1 }"
    raise SystemExit(f"unknown bump part: {part}")

def replace(path, pattern, new_line):
    text = path.read_text()
    path.write_text(re.sub(pattern, new_line, text, count=1, flags=re.M))

def main (): 
  part = sys.argv[1]
  old = re.search(r'^version = "(.+)"', PYPROJECT.read_text(), re.M).group (1)
  new = bump(old, part)

  replace(PYPROJECT, r'^version = ".+"', f'version = "{new}"')
  replace(INIT, r'^__version__ = ".+"', f'__version__ = "{new}"')

  print (f"version={new}")

if __name__ == "__main__":
    main()
