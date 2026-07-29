from a11y.schema import Metadata, Result, Violation
from a11y.validation import target_rules, target_selectors


def _violation(rule_id, tool='axe-core', targets=()):
    return Violation(
        tool=tool,
        rule_id=rule_id,
        wcag=[],
        description='d',
        count=1,
        targets=list(targets),
    )


def _result(device, tool, violations):
    width = 1280 if device == 'desktop' else 375
    return Result(
        metadata=Metadata(
            timestamp='t',
            url='u',
            browser='chromium',
            browser_version='1',
            viewport={'width': width, 'height': 0},
            device=device,
            tool=tool,
            tool_version='1',
        ),
        violations=violations,
        raw={},
    )


def test_target_rules_partitions_axe_rules_shared_or_specific_across_both_viewports():
    reference = [
        _result('desktop', 'axe-core', [_violation('color-contrast'), _violation('link-name')]),
        _result('mobile', 'axe-core', [_violation('target-size'), _violation('image-alt')]),
        _result('desktop', 'ibm-equal-access', [_violation('a_text_purpose', tool='ibm-equal-access')]),
    ]
    live = [
        _result('desktop', 'axe-core', [_violation('color-contrast'), _violation('link-name')]),
        _result('mobile', 'axe-core', [_violation('target-size')]),
        _result('desktop', 'ibm-equal-access', [_violation('a_text_purpose', tool='ibm-equal-access')]),
    ]

    partition = target_rules(reference, live, 'axe-core')

    assert partition == {
        'shared': ['color-contrast', 'link-name', 'target-size'],
        'reference_only': ['image-alt'],
        'live_only': [],
    }


def test_target_rules_filters_by_tool_so_ibm_rules_partition_independently():
    reference = [
        _result('desktop', 'axe-core', [_violation('link-name')]),
        _result('desktop', 'ibm-equal-access', [
            _violation('a_text_purpose', tool='ibm-equal-access'),
            _violation('img_alt_valid', tool='ibm-equal-access'),
        ]),
    ]
    live = [
        _result('desktop', 'axe-core', [_violation('link-name')]),
        _result('desktop', 'ibm-equal-access', [_violation('a_text_purpose', tool='ibm-equal-access')]),
    ]

    partition = target_rules(reference, live, 'ibm-equal-access')

    assert partition == {
        'shared': ['a_text_purpose'],
        'reference_only': ['img_alt_valid'],
        'live_only': [],
    }


def test_target_selectors_partitions_selectors_per_rule_for_the_requested_device():
    reference = [
        _result('desktop', 'axe-core', [
            _violation('target-size', targets=('#banner1', '.doormatSection > a')),
            _violation('link-name', targets=('#logovlibras',)),
        ]),
        _result('mobile', 'axe-core', [_violation('target-size', targets=('#menu-icon',))]),
    ]
    live = [
        _result('desktop', 'axe-core', [
            _violation('target-size', targets=('#banner1', 'a[href$="instituto"]')),
            _violation('image-alt', targets=('#mediacarousel',)),
        ]),
        _result('mobile', 'axe-core', [_violation('target-size', targets=('#banner1',))]),
    ]

    partition = target_selectors(reference, live, 'axe-core', 'desktop')

    assert partition == {
        'image-alt': {
            'shared': [],
            'reference_only': [],
            'live_only': ['#mediacarousel'],
        },
        'link-name': {
            'shared': [],
            'reference_only': ['#logovlibras'],
            'live_only': [],
        },
        'target-size': {
            'shared': ['#banner1'],
            'reference_only': ['.doormatSection > a'],
            'live_only': ['a[href$="instituto"]'],
        },
    }


def test_target_selectors_filters_by_tool_so_each_engine_partitions_independently():
    reference = [
        _result('desktop', 'axe-core', [_violation('link-name', targets=('#logovlibras',))]),
        _result('desktop', 'ibm-equal-access', [
            _violation('a_text_purpose', tool='ibm-equal-access', targets=('#logovlibras', '#extra')),
        ]),
    ]
    live = [
        _result('desktop', 'axe-core', [_violation('link-name', targets=('#other',))]),
        _result('desktop', 'ibm-equal-access', [
            _violation('a_text_purpose', tool='ibm-equal-access', targets=('#logovlibras',)),
        ]),
    ]

    partition = target_selectors(reference, live, 'ibm-equal-access', 'desktop')

    assert partition == {
        'a_text_purpose': {
            'shared': ['#logovlibras'],
            'reference_only': ['#extra'],
            'live_only': [],
        },
    }
