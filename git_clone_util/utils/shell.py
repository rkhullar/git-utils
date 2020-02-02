from .types import PathOrStr
import subprocess


def run_cmd(*args, cwd: PathOrStr = None) -> str:
    process = subprocess.run(args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = process.stdout.decode('utf-8').strip()
    return output


def git(*args, cwd: PathOrStr = None) -> str:
    return run_cmd(['git', *args], cwd=cwd)
