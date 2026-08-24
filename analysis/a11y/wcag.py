_PRINCIPLES = {
    '1': 'Perceivable',
    '2': 'Operable',
    '3': 'Understandable',
    '4': 'Robust',
}


_LEVELS = {
    '1.1.1': 'A',
    '1.3.1': 'A',
    '1.4.1': 'A',
    '1.4.3': 'AA',
    '2.4.4': 'A',
    '2.5.8': 'AA',
    '3.1.1': 'A',
    '4.1.2': 'A',
}


_IBM_CRITERIA = {
    'img_alt_valid': ['1.1.1'],
    'img_alt_redundant': ['1.1.1'],
    'a_text_purpose': ['2.4.4', '4.1.2'],
    'aria_content_in_landmark': ['1.3.1'],
    'text_contrast_sufficient': ['1.4.3'],
    'frame_title_exists': ['4.1.2'],
    'html_lang_exists': ['3.1.1'],
    'table_headers_exists': ['1.3.1'],
}


_ENGINE_PAIRS = {
    'image-alt': 'img_alt_valid',
    'link-name': 'a_text_purpose',
    'color-contrast': 'text_contrast_sufficient',
    'frame-title': 'frame_title_exists',
}


_COUNTERPARTS = {**_ENGINE_PAIRS, **{ibm: axe for axe, ibm in _ENGINE_PAIRS.items()}}


_AFFECTED_GROUPS = {
    '1.1.1': ['screen_reader', 'cognitive'],
    '1.3.1': ['screen_reader'],
    '1.4.1': ['low_vision', 'color_vision_deficiency', 'older_users'],
    '1.4.3': ['low_vision', 'color_vision_deficiency'],
    '2.4.4': ['screen_reader', 'cognitive', 'motor'],
    '2.5.8': ['motor', 'touch_mobile'],
    '3.1.1': ['screen_reader', 'cognitive'],
    '4.1.2': ['screen_reader', 'low_vision', 'motor'],
}


def principle(criterion):
    return _PRINCIPLES[criterion.split('.')[0]]


def level(criterion):
    return _LEVELS[criterion]


def ibm_criteria(rule_id):
    return _IBM_CRITERIA[rule_id]


def affected_groups(criterion):
    return _AFFECTED_GROUPS[criterion]


def counterpart(rule_id):
    return _COUNTERPARTS.get(rule_id)
