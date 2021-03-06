from typing import List
from typing.io import BinaryIO
from enum import Enum
import requests
from requests_aws4auth import AWS4Auth


# http://developer.ivona.com/en/speechcloud/introduction.html#SpeechCloudEndpoints
class Region(Enum):
    EuWest1 = 'eu-west-1'  # EU, Dublin
    UsEast1 = 'us-east-1'  # US East, N. Virginia
    UsWest2 = 'us-west-2'  # US West, Oregon

    def endpoint(self) -> str:
        return 'tts.{}.ivonacloud.com'.format(self.value)


class Voice(object):
    @staticmethod
    def from_dict(d: dict):
        return Voice(d['Name'], d['Language'], d['Gender'])

    def __init__(self, name: str=None, language: str=None,
                 gender: str=None) -> None:
        self.name = name
        self.language = language
        self.gender = gender

    def __repr__(self) -> str:
        return "Voice(name='{}', language='{}', gender='{}')".format(
                self.name, self.language, self.gender)

    def to_dict(self) -> dict:
        d = {}
        for key, val in [('Name', self.name),
                         ('Language', self.language),
                         ('Gender', self.gender)]:
            if val is not None:
                d[key] = val
        return d


class IvonaAPIException(Exception):
    def __init__(self, res: requests.Response) -> None:
        self.status_code = res.status_code
        self.error_type = res.headers['x-amzn-ErrorType'].split(':')
        self.details = res.json()

    def __str__(self) -> str:
        return '{} {}: {}'.format(
                self.status_code, self.error_type[0], self.details['Message'])


class Ivona(object):
    def __init__(self, access_key: str, secret_key: str,
                 region: Region) -> None:
        self._region = region
        self._session = requests.Session()
        self._session.auth = AWS4Auth(
                access_key, secret_key, region.value, 'tts')

    def _do_request(self, action: str, data: dict,
                    stream: bool= False) -> requests.Response:
        endpoint = 'https://{}/{}'.format(self._region.endpoint(), action)
        res = self._session.post(endpoint, json=data, stream=stream, timeout=3)

        if res.status_code != 200:
            raise IvonaAPIException(res)

        return res

    def list_voices(self, name: str=None, language: str=None,
                    gender: str=None) -> List[Voice]:
        voice_selector = Voice(name, language, gender)

        res = self._do_request('ListVoices', {
                'Voice': voice_selector.to_dict()
            })

        voices = []
        for voice in res.json()['Voices']:
            voices.append(Voice.from_dict(voice))

        return voices

    def create_speech(self, text: str, voice: Voice) -> BinaryIO:
        data = {
            'Input': {
                'Data': text,
                'Type': 'text/plain'
            },
            'Voice': voice.to_dict()
        }

        res = self._do_request('CreateSpeech', data, True)

        return res.raw
