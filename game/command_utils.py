from contextlib import contextmanager
from functools import wraps
from io import TextIOWrapper

import djclick as click
from django.utils import timezone


def show_command_time(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start_time = timezone.now()

        result = fn(*args, **kwargs)

        end_time = timezone.now()
        timedelta = end_time - start_time
        click.secho(f"Done in {timedelta.total_seconds()}s")
        return result

    return wrapper


@contextmanager
def read_stream_with_progress(
    stream: TextIOWrapper, progress_label: str, length: int = None, reader=None
):
    length = length or sum(1 for _ in stream)
    reader = reader or stream
    stream.seek(0)
    click.secho(f"Found {length} lines")
    with click.progressbar(
        reader, length=length, label=progress_label
    ) as progress_reader:
        yield progress_reader
