from .utils import run_cmd, PathOrStr
from pathlib import Path
from typing import Dict, List, Union
import json


def git(*args, cwd: PathOrStr = None) -> str:
    return run_cmd(['git', *args], cwd=cwd)


def url_to_name(url: str) -> str:
    return url.split(':')[1].split('.git')[0].split('/')[1]


def read_suffix(name: str) -> str:
    return Path(name).suffix.strip('.')


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


def process(manifest_path: Path, target_dir: Path = None, parent_config: Dict = None):
    parent_config: Dict = parent_config or dict()
    target_dir: Path = target_dir or manifest_path.parent
    with manifest_path.open('r') as f:
        manifest: Union[List, Dict] = json.load(f)

    if isinstance(manifest, List):
        items: List = manifest
        config: Dict = parent_config.copy()

    elif isinstance(manifest, Dict):
        items: List = manifest['targets']
        config: Dict = {**parent_config, **manifest['config']}

    else:
        raise ValueError

    config['cwd'] = target_dir

    for item in items:
        if isinstance(item, str):
            suffix: str = read_suffix(item)
            if suffix == 'git':
                params = {**config, **dict(url=item)}
                clone(**params)

            elif suffix == 'json':
                child_path: Path = target_dir / item
                child_work_dir = target_dir / child_path.stem
                child_work_dir.mkdir(exist_ok=True, parents=True)
                process(manifest_path=child_path, target_dir=child_work_dir, parent_config=config.copy())

        elif isinstance(item, Dict):
            if 'url' in item:
                params = {**config, **item}
                clone(**params)

            elif 'manifest' in item:
                child_path: Path = target_dir / item['manifest']
                child_work_dir = target_dir / item.get('path', child_path.stem)
                child_work_dir.mkdir(exist_ok=True, parents=True)
                process(manifest_path=child_path, target_dir=child_work_dir, parent_config=config.copy())
