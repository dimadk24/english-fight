from click.testing import CliRunner

from game.management.commands.hidepairs import hidepairs, hide_single_word
from game.models import Word, LanguagePair


def call():
    runner = CliRunner()
    result = runner.invoke(hidepairs,
                           ['test_input_files/hidepairs_test_file.txt'])
    if result.exit_code:
        print(result.output)
    assert result.exit_code == 0
    return result.output


bad_english = 'word'
bad_russian = 'слово'
good_english = 'cat'
good_russian = 'кот'


def create_language_pairs():
    en = Word.objects.create(text=bad_english)
    ru = Word.objects.create(text=bad_russian)
    LanguagePair.objects.create(english_word=en, russian_word=ru)
    valid_en = Word.objects.create(text=good_english)
    valid_ru = Word.objects.create(text=good_russian)
    LanguagePair.objects.create(english_word=valid_en, russian_word=valid_ru)


class TestCli:
    def test_works(self):
        create_language_pairs()
        assert LanguagePair.objects.get(english_word__text=bad_english).visible

        output = call()

        assert 'ok' in output
        assert 'Hid 1 words' in output
        assert not LanguagePair.objects.get(
            english_word__text=bad_english).visible


class TestHideSingleWord:
    def test_returns_zero_when_nothing_matched(self):
        create_language_pairs()
        result = hide_single_word('Phone')

        assert result == 0
        assert LanguagePair.objects.get(english_word__text=bad_english).visible

    def test_returns_zero_when_english_pair_is_already_hidden(self):
        create_language_pairs()
        LanguagePair.objects.update(visible=False)

        result = hide_single_word(bad_english)

        assert result == 0
        assert not LanguagePair.objects.get(
            english_word__text=bad_english).visible

    def test_returns_zero_when_russian_pair_is_already_hidden(self):
        create_language_pairs()
        LanguagePair.objects.update(visible=False)

        result = hide_single_word(bad_russian)

        assert result == 0
        assert not LanguagePair.objects.get(
            russian_word__text=bad_russian).visible

    def test_hides_english_word(self):
        create_language_pairs()
        assert LanguagePair.objects.get(english_word__text=bad_english).visible

        result = hide_single_word(bad_english)

        assert result == 1
        assert not LanguagePair.objects.get(
            english_word__text=bad_english).visible

    def test_hides_russian_word(self):
        create_language_pairs()
        assert LanguagePair.objects.get(russian_word__text=bad_russian).visible

        result = hide_single_word(bad_russian)

        assert result == 1
        assert not LanguagePair.objects.get(
            russian_word__text=bad_russian).visible

    def test_works_case_insensitively_for_english(self):
        create_language_pairs()
        assert LanguagePair.objects.get(english_word__text=bad_english).visible

        result = hide_single_word(bad_english.capitalize())

        assert result == 1
        assert not LanguagePair.objects.get(
            english_word__text=bad_english).visible

    def test_works_case_insensitively_for_russian(self):
        create_language_pairs()
        assert LanguagePair.objects.get(russian_word__text=bad_russian).visible

        result = hide_single_word(bad_russian.capitalize())

        assert result == 1
        assert not LanguagePair.objects.get(
            russian_word__text=bad_russian).visible

    def test_does_not_change_visibility_of_good_words(self):
        create_language_pairs()
        assert LanguagePair.objects.get(
            russian_word__text=good_russian).visible

        result = hide_single_word(bad_russian.capitalize())

        assert result == 1
        assert LanguagePair.objects.get(
            russian_word__text=good_russian).visible
