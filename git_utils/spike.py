from pathlib import Path
from typing import Dict, List, Union
import json
import subprocess

PathOrStr = Union[Path, str]

here = Path(__file__).parent
manifest_path = here / 'single.json'
target_dir = manifest_path.parent
with manifest_path.open('r') as f:
    manifest = json.load(f)


def git(*args, cwd: PathOrStr = None) -> str:
    process = subprocess.run(['git', *args], cwd=str(cwd), stdout=subprocess.PIPE)
    output = process.stdout.decode('utf-8').strip()
    return output


def url_to_name(url: str) -> str:
    return url.split('/')[1].split('.git')[0]


def clone(url: str, path: PathOrStr = None, branch: str = None, email: str = None, cwd: PathOrStr = None):
    # determine local path
    path: Path = Path(path or url_to_name(url))

    # build arguments
    args = ["clone"]
    if branch:
        args.append('--branch')
        args.append(branch)
    args.append(url)
    args.append(str(path))

    # execute clone
    git(*args, cwd=cwd)

    if email:
        repo_dir: Path = (cwd or Path.cwd()) / path
        git('config', 'user.email', email, cwd=repo_dir)


for item in manifest:
    if isinstance(item, str):
        print(item)
        clone(url=item, cwd=target_dir)
    elif isinstance(item, Dict):
        clone(**item, cwd=target_dir)
