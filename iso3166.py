countries = {
    'argentina': 'AR',
    'australia': 'AU',
    'austria': 'AT',
    'belgium': 'BE',
    'canada': 'CA',
    'chile': 'CL',
    'czech republic': 'CZ',
    'denmark': 'DK',
    'finland': 'FI',
    'france': 'FR',
    'germany': 'DE',
    'hungary': 'HU',
    'israel': 'IL',
    'italy': 'IT',
    'luxembourg': 'LU',
    'namibia': 'NA',
    'netherlands': 'NL',
    'new zealand': 'NZ',
    'poland': 'PL',
    'slovakia': 'SK',
    'slovenia': 'SI',
    'south-africa': 'ZA',
    'spain': 'ES',
    'sweden': 'SE',
    'switzerland': 'CH',
    'uk': 'GB',
    'united states': 'US'
}

def normalize_country(name):
    ''' Convert country name to ISO 3166-1 alpha-2 country code.'''

    return countries.get(name, 'ZZ')
