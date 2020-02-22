from typing import Dict, Iterator, NamedTuple, Optional
from pathlib import Path
import csv
import requests


class RepoInfo(NamedTuple):
    owner: str
    name: str
    private: bool
    main_branch: Optional[str] = None
    project_name: Optional[str] = None
    project_key: Optional[str] = None

    @staticmethod
    def from_api(item: Dict) -> 'RepoInfo':
        return RepoInfo(owner=item['owner'].get('username') or item['full_name'].split('/')[0],
                        name=item['name'],
                        private=item['is_private'],
                        main_branch=(item['mainbranch'] or {}).get('name'),
                        project_key=item.get('project', {}).get('key'),
                        project_name=item.get('project', {}).get('name'))

    @property
    def clone_url(self) -> str:
        return f'git@bitbucket.org:{self.owner}/{self.name}.git'


class Bitbucket:
    api = 'https://api.bitbucket.org/2.0'

    def __init__(self, username: str, password: str):
        self.auth = (username, password)

    def iter_repos(self, role: str = None) -> Iterator[RepoInfo]:
        url = f'{self.api}/repositories'
        params = dict()
        if role:
            params['role'] = role

        request_kwargs = dict(url=url, auth=self.auth, params=params)

        while True:
            response = requests.get(**request_kwargs)
            response_data = response.json()

            for item in response_data['values']:
                yield RepoInfo.from_api(item)

            if 'next' in response_data:
                request_kwargs['url'] = response_data['next']
                if 'params' in request_kwargs:
                    request_kwargs.pop('params')
            else:
                break


def build_main_callback(output: str = None):
    def print_clone_url(repo_info):
        print(repo_info.clone_url)

    def append_csv(repo_info):
        with Path(output).open('a') as f:
            csv_writer = csv.DictWriter(f, list(RepoInfo._fields))
            csv_writer.writerow(repo_info._asdict())

    return append_csv if output else print_clone_url


def prepare_csv(output: str):
    output_path = Path(output)
    if output_path.exists():
        output_path.unlink()
    with output_path.open('w') as f:
        csv_writer = csv.DictWriter(f, list(RepoInfo._fields))
        csv_writer.writeheader()


def main(username: str, password: str, platform: str, role: str, output: str = None):
    fn = build_main_callback(output)
    if output:
        prepare_csv(output)
    if platform == 'bitbucket':
        api = Bitbucket(username=username, password=password)
        for repo_info in api.iter_repos(role=role):
            fn(repo_info)
