from io import TextIOWrapper

import djclick as click
from django.db import transaction

from game.command_utils import show_command_time, read_stream_with_progress
from game.models import Word


@click.command(help='Hide language pairs with words from the passed file')
@click.argument('file', type=click.File())
@transaction.atomic
@show_command_time
def hidepairs(file: TextIOWrapper):
    removed_words = 0
    with read_stream_with_progress(
        file, progress_label='Processing words'
    ) as reader:
        for line in reader:
            removed_words += hide_single_word(line.strip())
    click.secho('ok', fg='green')
    if removed_words:
        click.secho(f'Hid {removed_words} words')
    else:
        click.secho(f'No words to hide')


def hide_single_word(word: str):
    try:
        word = Word.objects.get(text__iexact=word)
        if hasattr(word, 'english_pair'):
            if not word.english_pair.visible:
                return 0
            word.english_pair.visible = False
            word.english_pair.save()
        else:
            if not word.russian_pair.visible:
                return 0
            word.russian_pair.visible = False
            word.russian_pair.save()
        return 1
    except Word.DoesNotExist:
        return 0
