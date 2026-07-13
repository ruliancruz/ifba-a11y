from a11y.wcag import principle, level, ibm_criteria


def test_maps_each_wcag_criterion_to_its_pour_principle():
    criteria = ['1.1.1', '2.4.4', '3.1.1', '4.1.2']

    principles = [principle(c) for c in criteria]

    assert principles == ['Perceivable', 'Operable', 'Understandable', 'Robust']


def test_reports_the_conformance_level_of_each_wcag_criterion():
    levels = {c: level(c) for c in ['1.1.1', '1.4.3', '2.4.4', '2.5.8']}

    assert levels == {'1.1.1': 'A', '1.4.3': 'AA', '2.4.4': 'A', '2.5.8': 'AA'}


def test_maps_ibm_rule_ids_to_their_wcag_criteria():
    criteria = {r: ibm_criteria(r) for r in ['img_alt_valid', 'a_text_purpose', 'aria_content_in_landmark']}

    assert criteria == {
        'img_alt_valid': ['1.1.1'],
        'a_text_purpose': ['2.4.4', '4.1.2'],
        'aria_content_in_landmark': ['1.3.1'],
    }
