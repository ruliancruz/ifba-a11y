_PRINCIPLES = {
    '1': 'Perceivable',
    '2': 'Operable',
    '3': 'Understandable',
    '4': 'Robust',
}


_LEVELS = {
    '1.1.1': 'A',
    '1.3.1': 'A',
    '1.4.3': 'AA',
    '2.4.4': 'A',
    '2.5.8': 'AA',
    '4.1.2': 'A',
}


_IBM_CRITERIA = {
    'img_alt_valid': ['1.1.1'],
    'img_alt_redundant': ['1.1.1'],
    'a_text_purpose': ['2.4.4', '4.1.2'],
    'aria_content_in_landmark': ['1.3.1'],
    'text_contrast_sufficient': ['1.4.3'],
}


def principle(criterion):
    return _PRINCIPLES[criterion.split('.')[0]]


def level(criterion):
    return _LEVELS[criterion]


def ibm_criteria(rule_id):
    return _IBM_CRITERIA[rule_id]
