from .utils import git, PathOrStr, url_to_name
from pathlib import Path


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
