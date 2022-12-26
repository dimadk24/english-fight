#!/usr/bin/env python
import subprocess  # nosec
from datetime import datetime
from pathlib import Path

import click


@click.command()
@click.option("--user", "-u", help="Database user, passed directly to mysql")
@click.argument("database", default="enfight")
def handler(user, database):
    output_folder = Path("/var/backups/enfight")
    if not output_folder.exists():
        raise Exception(f"{output_folder} does not exists, please create")

    today = datetime.today()
    file_name = f"{today.strftime('%b-%d').lower()}.sql"
    output_path = output_folder / file_name

    user_string = f"using user {user}" if user else "using current user"

    click.secho(
        f"Dumping database {database} to {str(output_path)} {user_string}\n"
        "You will be asked for database password"
    )

    stdout = open(output_path, "w")
    user_arguments = ["-u", user] if user else []

    subprocess.run(  # nosec
        [
            "mysqldump",
            "-p",
            "--add-drop-database",
            *user_arguments,
            database,
        ],
        stdout=stdout,
    )
    print("Done")


if __name__ == "__main__":
    handler()
