import os
import argparse
from mp3_player import Player
from spelling import Speller
from ivona_api import Ivona, Region


def main() -> None:
    parser = argparse.ArgumentParser('IVONA TTS reader')
    parser.add_argument('-l', '--language', type=str,
                        help='Voice language (e.g. pl-PL, en-US)')
    parser.add_argument('-n', '--name', type=str, help='Voice name')
    parser.add_argument('-g', '--gender', type=str,
                        help='Voice gender (Male or Female)')
    parser.add_argument('--spelling', dest='spelling', action='store_true',
                        help="Enable spelling (default)")
    parser.add_argument('--no-spelling', dest='spelling',
                        action='store_false', help="Disable spelling")
    parser.set_defaults(spelling=True)
    args = parser.parse_args()

    ivona = Ivona(
        os.environ.get('IVONA_ACCESS_KEY'),
        os.environ.get('IVONA_SECRET_KEY'),
        Region(os.environ.get('IVONA_REGION', 'eu-west-1')))

    voices = ivona.list_voices(name=args.name,
                               language=args.language,
                               gender=args.gender)

    if len(voices) == 0:
        print("No voices with specified criteria.")
        return

    voice = voices[0]

    if len(voices) > 1:
        for i, voice in enumerate(voices):
            print(i, voice)
        voice = voices[int(input("voice number> "))]

    print("Selected voice:", voice)

    player = Player()
    if args.spelling:
        speller = Speller(language=voice.language.split('-')[0])
    while True:
        text = input("").strip()
        if text == '':
            continue
        elif text in {'.q', '.quit'}:
            break

        if args.spelling:
            if text.startswith('!'):
                text = text[1:]
            else:
                fixed_text = speller.fix(text)
                if text != fixed_text:
                    text = fixed_text
                    print('fixed:', text)

        speech_file = ivona.create_speech(text, voice)
        player.play(speech_file)


if __name__ == "__main__":
    main()
