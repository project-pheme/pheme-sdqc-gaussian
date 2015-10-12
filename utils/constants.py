'''
Created on 14 Jul 2014

@author: michal
'''

parent_types = [u'SIMPLE', u'COMPLEX', None]
parent_types_nonone = [u'SIMPLE', u'COMPLEX']
parent_types_of_values = [type(5), type(None)]

#JSON fields names
JSON_FIELD_TOKENS = "tokens"
JSON_FIELD_TEXT = "body"
JSON_FIELD_TEXTXML = "gatexml"
JSON_FIELD_PARENT_TYPE = "parent_type"
JSON_FIELD_TYPE = 'type'
JSON_FIELD_QAZVINIAN_TYPE = 'qtype'
PARENT_TYPE_SIMPLE = 1#"SIMPLE"
PARENT_TYPE_COMPLEX = 0#"COMPLEX"
PARENT_TYPE_NONEXISTENT = -1#"COMPLEX"

RIOT_RUMOUR_NAMES = ["army_bank", "hospital", "london_eye", "mcdonalds", "miss_selfridge", "police_beat_girl", "zoo"]
QAZVINIAN_RUMOUR_NAMES = ["palin", "airfrance", "michelle"]
QAZV_RIOT_RUMOUR_NAMES = RIOT_RUMOUR_NAMES+QAZVINIAN_RUMOUR_NAMES

SPECTRAL_CLUSTER_FIELD = 'spectral_components'

JSON_TEXT_FIELD='body'
#JSON_TEXT_FIELD='text'
JSON_TIME_FIELD='time'
#JSON_TIME_FIELD='timestamp'