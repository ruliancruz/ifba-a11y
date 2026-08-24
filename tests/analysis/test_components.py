from a11y.components import component, component_counts
from a11y.schema import Metadata, Result, Violation


def _violation(rule_id, targets):
    return Violation(
        tool='axe-core',
        rule_id=rule_id,
        wcag=[],
        description='d',
        count=len(targets),
        targets=list(targets),
    )


def _result(device, violations):
    width = 1280 if device == 'desktop' else 375
    return Result(
        metadata=Metadata(
            timestamp='t',
            url='u',
            browser='chromium',
            browser_version='1',
            viewport={'width': width, 'height': 0},
            device=device,
            tool='axe-core',
            tool_version='1',
        ),
        violations=violations,
        raw={},
    )


def test_component_classifies_selectors_by_portal_component():
    selectors = [
        '#banner2 > .button-nav',
        '.column-0 > .doormatSection > .doormatSectionBody:nth-child(2) > .external-link',
        'a[href$="organograma/"]',
        '#abc > .nitf-basic-tile.tile-content > h2 > a',
        '.pagination > a',
    ]

    assert [component(s) for s in selectors] == [
        'banner_rotator',
        'grid_footer',
        'grid_footer',
        'news_tile',
        'other',
    ]


def test_component_counts_partitions_one_rule_on_one_viewport():
    results = [
        _result('desktop', [_violation('target-size', [
            '#banner1 > .button-nav',
            '#banner2 > .button-nav',
            '.column-2 > .doormatSection > .doormatSectionBody:nth-child(3) > .external-link',
            'a[href$="nossos-cursos"]',
            '.pagination > a',
        ])]),
        _result('mobile', [_violation('target-size', ['#banner1 > .button-nav'])]),
    ]

    counts = component_counts(results, 'target-size', 'desktop')

    assert counts == [
        {'component': 'banner_rotator', 'occurrences': 2},
        {'component': 'grid_footer', 'occurrences': 2},
        {'component': 'other', 'occurrences': 1},
    ]


def test_component_counts_is_empty_when_the_rule_is_absent_from_the_viewport():
    results = [_result('desktop', [_violation('link-name', ['#logovlibras'])])]

    assert component_counts(results, 'target-size', 'desktop') == []
