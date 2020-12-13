import subprocess

import djclick as click
from django.conf import settings


@click.command()
def handler():
    dbconfig = settings.DATABASES["default"]
    create_statement = (
        f"CREATE DATABASE {dbconfig['NAME']} "
        f"DEFAULT CHARSET = {dbconfig['OPTIONS']['charset']} "
        f"DEFAULT COLLATE = utf8mb4_unicode_ci;"
    )
    subprocess.run(
        [
            "mysql",
            "-u",
            dbconfig["USER"],
            f'-p{dbconfig["PASSWORD"]}',
            "--execute",
            create_statement,
        ]
    )
