from bs4 import BeautifulSoup
import requests


class LetteredMusicNoteScraper:
    def __init__(self, note_duration=0.5):
        self.note_duration = note_duration
        self.base_notes = ['C', 'C#', 'D', 'D#', 'E', 'F',
                           'F#', 'G', 'G#', 'A', 'A#', 'B']

    def _is_note_line(self, s):
        note_letters = 'ABCDEFG^#*b-. '
        for c in s:
            if c not in note_letters:
                return False
        return True

    def _get_lettered_notes_from_content(self, content):
        lines = content.replace('\xa0', '') \
                      .replace('<div class="post content">', '') \
                      .replace('<p>', '<br>').replace('</p>', '') \
                      .replace('</br>', '<br>') \
                      .replace('<br/>', '<br>') \
                      .split('<br>')
        lines = [line.replace('<', '')
                     .replace('>', '')
                     .strip()
                     .replace('-', '- ')
                     .replace(' -', '-')
                     .strip()
                 for line in lines]
        lines = [line for line in lines if self._is_note_line(line)]
        letters = ' | '.join(lines) \
                       .replace('^', ' ^') \
                       .replace('\xa0', ' ') \
                       .strip() \
                       .split(' ')
        letters = [letter.strip() for letter in letters
                   if letter.strip()]
        if letters[0] == '|':
            letters = letters[1:]
        if letters[-1] == '|':
            letters = letters[:-1]
        note_letters = []
        last_letter = ''
        for letter in letters:
            if last_letter == letter and letter == '|':
                continue
            if letter == '-':
                note_letters[-1] = note_letters[-1] + '-'
                last_letter = note_letters[-1]
                continue
            last_letter = letter
            note_letters.append(letter)
        return note_letters

    def get_lettered_notes(self, url_id):
        res = requests.get('https://noobnotes.net/' + url_id + '/')
        if res.status_code == 404:
            return None
        soup = BeautifulSoup(res.text, features='html.parser')
        post_content = str(soup.find('div', {'class': 'post-content'}))

        lettered_notes = self._get_lettered_notes_from_content(post_content)

        with open('lettered_notes/' + url_id + '.txt', 'w') as f:
            f.write(','.join(lettered_notes))
            f.close()


if __name__ == '__main__':
    scraper = LetteredMusicNoteScraper()
    lettered_notes = scraper.get_lettered_notes(
                        'super-mario-bros-theme-nintendo'
                        )
    scraper = LetteredMusicNoteScraper()
    lettered_notes = scraper.get_lettered_notes(
                        'a-whole-new-world-aladdin'
                        )
    scraper = LetteredMusicNoteScraper()
    lettered_notes = scraper.get_lettered_notes(
                        'take-me-home-country-roads-john-denver'
                        )
    scraper = LetteredMusicNoteScraper()
    lettered_notes = scraper.get_lettered_notes(
                        'let-it-go-frozen-disney'
                        )
