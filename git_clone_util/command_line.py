from .process import process as handle_clone
from .scan import main as handle_scan
from argparse import ArgumentParser, Namespace
from getpass import getpass
from pathlib import Path


def build_parser() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='action')
    subparsers.required = True

    clone_parser = subparsers.add_parser('clone')
    clone_parser.add_argument('-m', '--manifest')

    scan_parser = subparsers.add_parser('scan')
    scan_parser.add_argument('-d', '--platform', required=True, choices=['bitbucket'])
    scan_parser.add_argument('-u', '--username', required=True)
    scan_parser.add_argument('-p', '--password', required=False)
    scan_parser.add_argument('-r', '--role', required=True, choices=['admin', 'contributor', 'member', 'owner'])
    scan_parser.add_argument('-o', '--output', required=False)

    return parser


def main():
    parser: ArgumentParser = build_parser()
    args: Namespace = parser.parse_args()
    action: str = args.action
    if action == 'clone':
        handle_clone(manifest_path=Path(args.manifest))
    elif action == 'scan':
        password = args.password or getpass()
        handle_scan(username=args.username, password=password, platform=args.platform, role=args.role, output=args.output)
