from a11y.convergence import compare
from a11y.schema import Metadata, Result, Violation


def _violation(rule_id, count, tool='axe-core', wcag=None):
    return Violation(
        tool=tool,
        rule_id=rule_id,
        wcag=wcag or [],
        description='d',
        count=count,
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


def test_compare_partitions_wcag_criteria_into_shared_and_engine_specific():
    results = [
        _result('desktop', 'axe-core', [
            _violation('link-name', 7, wcag=['2.4.4', '4.1.2']),
            _violation('target-size', 25, wcag=['2.5.8']),
        ]),
        _result('mobile', 'axe-core', [
            _violation('link-name', 12, wcag=['2.4.4', '4.1.2']),
        ]),
        _result('desktop', 'ibm-equal-access', [
            _violation('a_text_purpose', 8, tool='ibm-equal-access'),
            _violation('aria_content_in_landmark', 6, tool='ibm-equal-access'),
        ]),
        _result('mobile', 'ibm-equal-access', [
            _violation('a_text_purpose', 12, tool='ibm-equal-access'),
        ]),
    ]

    partition = compare(results)

    assert partition == {
        'shared': ['2.4.4', '4.1.2'],
        'axe_only': ['2.5.8'],
        'ibm_only': ['1.3.1'],
    }
