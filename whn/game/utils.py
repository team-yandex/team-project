import json
import re

import django.conf


def normilize_string(string):
    ambiguous_path = django.conf.settings.BASE_DIR / 'game' / 'ambiguous.json'
    with ambiguous_path.open(mode='r') as fp:
        ambiguous = json.load(fp)
        ambiguous = dict((int(k), v) for k, v in ambiguous.items())
    # remove puctuaction
    normilized = re.sub(r'[^\w\s]', '', string)
    # remove spacing
    normilized = ''.join(normilized.split())
    # replace ambiguous symbols to ascii
    normilized = normilized.upper()
    normilized = normilized.translate(ambiguous)
    normilized = normilized.lower()
    normilized = normilized.translate(ambiguous)
    return normilized
