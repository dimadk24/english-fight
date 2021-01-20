#!/usr/bin/env python

import subprocess  # nosec
from pathlib import Path

import click
from environ import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
dotenv_file = BASE_DIR / ".env"
env.read_env(str(dotenv_file))


@click.command()
def handler():
    folder = env("DEPLOY_FOLDER")
    user = env("DEPLOY_USER")
    host = env("DEPLOY_HOST")
    if not env("CI", default=None):
        print(f"User: {user}")
        print(f"Host: {host}")
        print(f"Folder: {folder}")

    subprocess.check_output(  # nosec
        [
            "/usr/bin/rsync",
            "-a",
            "--exclude-from=.deployignore",
            "--delete",
            ".",
            f'{user}@{host}:"{folder}"',
        ],
        cwd=BASE_DIR,
    )
    print("Done")


if __name__ == "__main__":
    handler()
