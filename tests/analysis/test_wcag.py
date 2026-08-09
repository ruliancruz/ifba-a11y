from a11y.wcag import principle, level, ibm_criteria, affected_groups


def test_maps_each_wcag_criterion_to_its_pour_principle():
    criteria = ['1.1.1', '2.4.4', '3.1.1', '4.1.2']

    principles = [principle(c) for c in criteria]

    assert principles == ['Perceivable', 'Operable', 'Understandable', 'Robust']


def test_reports_the_conformance_level_of_each_wcag_criterion():
    criteria = ['1.1.1', '1.3.1', '1.4.1', '1.4.3', '2.4.4', '2.5.8', '3.1.1', '4.1.2']

    levels = {c: level(c) for c in criteria}

    assert levels == {
        '1.1.1': 'A',
        '1.3.1': 'A',
        '1.4.1': 'A',
        '1.4.3': 'AA',
        '2.4.4': 'A',
        '2.5.8': 'AA',
        '3.1.1': 'A',
        '4.1.2': 'A',
    }


def test_maps_ibm_rule_ids_to_their_wcag_criteria():
    rules = [
        'img_alt_valid',
        'a_text_purpose',
        'aria_content_in_landmark',
        'frame_title_exists',
        'html_lang_exists',
        'table_headers_exists',
    ]

    criteria = {r: ibm_criteria(r) for r in rules}

    assert criteria == {
        'img_alt_valid': ['1.1.1'],
        'a_text_purpose': ['2.4.4', '4.1.2'],
        'aria_content_in_landmark': ['1.3.1'],
        'frame_title_exists': ['4.1.2'],
        'html_lang_exists': ['3.1.1'],
        'table_headers_exists': ['1.3.1'],
    }


def test_maps_each_wcag_criterion_to_its_affected_user_groups():
    criteria = ['1.1.1', '1.3.1', '1.4.1', '1.4.3', '2.4.4', '2.5.8', '3.1.1', '4.1.2']

    groups = {c: affected_groups(c) for c in criteria}

    assert groups == {
        '1.1.1': ['screen_reader', 'cognitive'],
        '1.3.1': ['screen_reader'],
        '1.4.1': ['low_vision', 'color_vision_deficiency', 'older_users'],
        '1.4.3': ['low_vision', 'color_vision_deficiency'],
        '2.4.4': ['screen_reader', 'cognitive', 'motor'],
        '2.5.8': ['motor', 'touch_mobile'],
        '3.1.1': ['screen_reader', 'cognitive'],
        '4.1.2': ['screen_reader', 'low_vision', 'motor'],
    }
