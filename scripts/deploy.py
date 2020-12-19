#!/usr/bin/env python

import subprocess
from pathlib import Path

import click
from environ import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
dotenv_file = BASE_DIR / ".env"
env.read_env(str(dotenv_file))


@click.command()
@click.argument("target_environment", type=click.STRING)
def handler(target_environment):
    # TODO: remove environment argument
    if target_environment not in ("dev", "prod"):
        raise Exception(f"wrong target env: {target_environment}")
    if target_environment == "dev":
        folder = env("DEPLOY_DEV_FOLDER")
        print("Deploying to dev")
    else:
        folder = env("DEPLOY_PROD_FOLDER")
        print("Deploying to prod")
    user = env("DEPLOY_USER")
    host = env("DEPLOY_HOST")
    if not env("CI", default=None):
        print(f"User: {user}")
        print(f"Host: {host}")
        print(f"Folder: {folder}")

    subprocess.run(
        [
            "rsync",
            "-a",
            "--exclude-from=.deployignore",
            ".",
            f'{user}@{host}:"{folder}"',
        ],
        cwd=BASE_DIR,
    )


if __name__ == "__main__":
    handler()
