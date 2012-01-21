# rrrt2
# - MQS
import os
import platform
import json
import urllib, urllib2

FORVO_API_URL = 'http://apifree.forvo.com/'

FORMATS = ('mp3', 'ogg',)
MP3, OGG = FORMATS

ACTIONS = ('word-pronunciations', 'standard-pronunciation',)
WORD_PRONUNCIATIONS, STANDARD_PRONUNCIATION = ACTIONS

class Forvo(object):
    def __init__(self, key):
        self.key = key
        self._last_response = None
    
    def pronunciations(self, word, language=None, standard=False):
        action = STANDARD_PRONUNCIATION if standard else WORD_PRONUNCIATIONS
        args = [
            ('key', self.key),
            ('format', 'json'),
            ('action', action),
            ('word', urllib.quote(word)),
            ('language', language),
        ]
        url = FORVO_API_URL + '/'.join(['%s/%s' % a for a in args if a[1]])
        
        pronunciations = []
        try:
            self._last_resonse = urllib2.urlopen(url).read()
            results = json.loads(self._last_resonse)
            
            # Some requests will return an empty list or None
            if not results:
                return []
            
            for item in results.get('items', []):
                kwargs = dict([(str(key), value) for key, value in item.items()])
                pronunciations.append(Pronunciation(**kwargs))
        except:
            raise
        
        return pronunciations
    
    def pronounce(self, word, language=None, file_name=None):
        pronunciations = self.pronunciations(word, language, standard=True)
        if pronunciations:
            pronunciations[0].play()


class Pronunciation(object):
    default_format = MP3
    
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.pathmp3 = kwargs['pathmp3']
        self.pathogg = kwargs['pathogg']
        
        self._local_file_name = None
        self._local_format = None
        self._get_cached_download()
    
    def download(self, file_name=None, format=None):
        if not file_name:
            file_name = self._create_file_name(format)
        name, extension = os.path.splitext(file_name)
        format = extension.lstrip('.').lower()
        
        assert format in FORMATS
        
        with open(file_name, 'wb') as f:
            f.write(urllib2.urlopen(self.pathmp3).read())
        
        self._local_file_name = file_name
        self._local_format = format
    
    def play(self):
        if not self._is_downloaded():
            self.download()
        if platform.system == 'Linux':
            os.system('mpg123 -q %s' % self._local_file_name)
        else:
            os.system('afplay %s' % self._local_file_name)
    
    def _create_file_name(self, format=None):
        if not format:
            format = self.default_format
        temp_file_template = '/tmp/forvo_pronunciation_%s.%s'
        return temp_file_template % (self.id, format)
    
    def _get_cached_download(self):
        file_name = self._create_file_name()
        if os.path.exists(file_name):
            self._local_path = file_name
            self._local_format = self.default_format
    
    def _is_downloaded(self):
        return self._local_file_name and self._local_format
