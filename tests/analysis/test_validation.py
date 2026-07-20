from a11y.schema import Metadata, Result, Violation
from a11y.validation import target_rules


def _violation(rule_id, tool='axe-core'):
    return Violation(
        tool=tool,
        rule_id=rule_id,
        wcag=[],
        description='d',
        count=1,
        targets=[],
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
