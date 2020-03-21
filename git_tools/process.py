from .clone import clone
from .utils import read_suffix

from pathlib import Path
from typing import Dict, List, Union
import json


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
    config['raise_errors'] = False

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
