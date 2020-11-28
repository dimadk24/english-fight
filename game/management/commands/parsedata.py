import csv
from io import TextIOWrapper

import djclick as click
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from game.command_utils import show_command_time, read_stream_with_progress
from game.models import LanguagePair, Word


@click.command(help='Parse input data file and fill database with it')
@click.argument('file', type=click.File())
@transaction.atomic
@show_command_time
def parsedata(file: TextIOWrapper):
    reader = csv.DictReader(file, delimiter=',')
    number_of_rows = sum(1 for _ in file) - 1
    # -1 because of the header line

    with read_stream_with_progress(
        file, reader=reader, progress_label='Processing words',
        length=number_of_rows
    ) as progress_reader:
        language_pairs = []
        words_inserted = 0
        rows_processed = 0
        for row in progress_reader:
            rows_processed += 1
            russian_word = row['bare']
            english_word = row['translations_en']
            if russian_word and english_word:
                any_word_already_present = Word.objects.filter(
                    Q(text=russian_word) | Q(text=english_word)).exists()
                if not any_word_already_present:
                    russian_word = Word.objects.create(text=russian_word)
                    english_word = Word.objects.create(text=english_word)
                    words_inserted += 2
                    language_pairs.append(
                        LanguagePair(russian_word=russian_word,
                                     english_word=english_word,
                                     created_at=timezone.now()))
    click.secho(f'Processed {rows_processed} rows')
    if words_inserted:
        click.secho('Creating language pairs')
        LanguagePair.objects.bulk_create(language_pairs)
        total_words = Word.objects.count()
        total_pairs = LanguagePair.objects.count()
        language_pairs_created = len(language_pairs)
        rows_skipped = rows_processed - language_pairs_created
        click.secho('ok', fg='green')
        click.secho(
            f'Created {words_inserted} words\n'
            f'Created {language_pairs_created} language pairs\n'
            f'Skipped {rows_skipped} input rows\n'
            f'Total words count: {total_words}\n'
            f'Total language pairs count: {total_pairs}')
    else:
        click.secho('No new words to create', fg='yellow')
