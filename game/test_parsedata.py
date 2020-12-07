from datetime import timedelta

from click.testing import CliRunner
from django.utils import timezone

from game.management.commands.parsedata import parsedata
from game.models import Word, LanguagePair


def call():
    runner = CliRunner()
    result = runner.invoke(parsedata,
                           ['test_input_files/parsedata_test_file.csv'])
    if result.exit_code:
        print(result.output)
    assert result.exit_code == 0
    return result.output


def test_command_output():
    output = call()

    assert 'Processed 444 rows' in output
    assert 'ok' in output
    assert 'Skipped 5 input rows' in output
    assert 'Created 878 words' in output
    assert 'Created 439 language pairs' in output
    assert 'Total words count: 878' in output
    assert 'Total language pairs count: 439' in output


def test_does_not_repeat_same_values():
    output = call()
    assert 'ok' in output
    assert 'Created 878 words' in output
    assert 'Total words count: 878' in output

    output = call()
    assert 'No new words to create' in output
    assert Word.objects.count() == 878
    assert LanguagePair.objects.count() == 439


def test_result_data():
    call()
    now = timezone.now()
    language_pairs = LanguagePair.objects.all()
    assert len(language_pairs) == 439
    for language_pair in language_pairs:
        assert now - language_pair.created_at < timedelta(minutes=1)
        assert language_pair.visible
