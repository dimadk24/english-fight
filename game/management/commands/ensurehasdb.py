import subprocess  # nosec

import djclick as click
from django.conf import settings


@click.command()
def handler():
    dbconfig = settings.DATABASES["default"]
    create_statement = (
        f"CREATE DATABASE IF NOT EXISTS {dbconfig['NAME']} "
        f"DEFAULT CHARSET = {dbconfig['OPTIONS']['charset']} "
        f"DEFAULT COLLATE = utf8mb4_0900_ai_ci;"
    )
    subprocess.check_output(  # nosec
        [
            "/usr/bin/mysql",
            "-u",
            dbconfig["USER"],
            f'-p{dbconfig["PASSWORD"]}',
            "--port",
            str(dbconfig["PORT"]),
            "--host",
            dbconfig["HOST"],
            "--execute",
            create_statement,
        ]
    )
