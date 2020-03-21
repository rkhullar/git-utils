from .utils import git, PathOrStr, ProcessResult, url_to_name
from pathlib import Path


def clone(url: str, path: PathOrStr = None, branch: str = None, email: str = None, cwd: PathOrStr = None, raise_errors: bool = True):
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
    result: ProcessResult = git(*args, cwd=cwd)
    if result.code != 0 and raise_errors:
        raise ChildProcessError(dict(message='clone failed', command=args, result=result))

    if email:
        repo_dir: Path = (cwd or Path.cwd()) / path
        result: ProcessResult = git('config', 'user.email', email, cwd=repo_dir)
        if result.code != 0 and raise_errors:
            raise ChildProcessError(dict(message='config failed', command=args, result=result))
