from .types import PathOrStr
from typing import NamedTuple
import subprocess


class ProcessResult(NamedTuple):
    code: int
    stdout: str
    stderr: str


def run_cmd(*args, cwd: PathOrStr = None) -> ProcessResult:
    process = subprocess.run(args, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = process.stdout.decode('utf-8').strip()
    stderr = process.stderr.decode('utf-8').strip()
    return ProcessResult(code=process.returncode, stdout=stdout, stderr=stderr)


def git(*args, cwd: PathOrStr = None) -> ProcessResult:
    return run_cmd(*['git', *args], cwd=cwd)
