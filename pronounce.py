#!/usr/bin/python
import os
from optparse import OptionParser

from api import Forvo

parser = OptionParser(usage="usage: %prog [options] word")
parser.add_option('-f', '--file',
    action='store', type='string', dest='file_name', default=None,
    help="Target path for the downloaded audio file, with an extension of 'mp3' or 'ogg'")
parser.add_option('-l', '--language',
    action='store', type='string', dest='language', default=None,
    help="Two digit language code (i.e. 'en', 'es', 'de', 'ja')")
parser.add_option('-k', '--key',
    action='store', type='string', dest='api_key', default=None,
    help="Your Forvo API key (overrides FORVO_API_KEY environmental variable)")

if __name__ == '__main__':
    options, args = parser.parse_args()
    if len(args) < 1:
        parser.error("word is required")
    
    # Get API key from option or environment
    api_key = options.api_key
    if not api_key:
        api_key = os.getenv('FORVO_API_KEY')
    if not api_key:
        parser.error("could not find API key (is FORVO_API_KEY set?)")
    
    f = Forvo(api_key)
    f.pronounce(word=args[0],
        language=options.language, file_name=options.file_name)
