from .process import process
from argparse import ArgumentParser, Namespace
from pathlib import Path


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    clone_parser = subparsers.add_parser('clone')
    clone_parser.add_argument('-m', '--manifest')

    scan_parser = subparsers.add_parser('scan')
    scan_parser.add_argument('-p', '--platform')

    return parser


def main():
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    action: str = args.action
    if action == 'clone':
        process(manifest_path=Path(args.manifest))
    elif action == 'scan':
        print('coming soon')
