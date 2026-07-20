from a11y.aggregate import (
    axe_rules,
    by_criterion,
    by_impact,
    by_level,
    by_principle,
    ibm_buckets,
    ibm_rules,
    overview,
    priorities,
    viewport_criteria,
)
from a11y.schema import Metadata, Result, Violation


def _violation(rule_id, count, tool='axe-core', wcag=None, impact=None):
    return Violation(
        tool=tool,
        rule_id=rule_id,
        wcag=wcag or [],
        description='d',
        count=count,
        targets=[],
        impact=impact,
    )


def _result(device, tool, violations, raw=None):
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
        raw=raw or {},
    )


def test_overview_counts_axe_rules_occurrences_and_ibm_violations_per_viewport():
    results = [
        _result('desktop', 'axe-core', [_violation('link-name', 7), _violation('target-size', 25)]),
        _result('desktop', 'ibm-equal-access', [_violation('a_text_purpose', 8, tool='ibm-equal-access')]),
        _result('mobile', 'axe-core', [_violation('link-name', 12), _violation('target-size', 4)]),
        _result('mobile', 'ibm-equal-access', [_violation('a_text_purpose', 12, tool='ibm-equal-access')]),
    ]

    rows = overview(results)

    assert rows == [
        {'device': 'desktop', 'axe_rules': 2, 'axe_occurrences': 32, 'ibm_violations': 8},
        {'device': 'mobile', 'axe_rules': 2, 'axe_occurrences': 16, 'ibm_violations': 12},
    ]


def test_axe_rules_lists_each_rule_with_wcag_level_impact_and_per_viewport_counts():
    results = [
        _result('desktop', 'axe-core', [
            _violation('target-size', 25, wcag=['2.5.8'], impact='serious'),
            _violation('link-name', 7, wcag=['2.4.4', '4.1.2'], impact='serious'),
        ]),
        _result('mobile', 'axe-core', [
            _violation('target-size', 4, wcag=['2.5.8'], impact='serious'),
            _violation('link-name', 12, wcag=['2.4.4', '4.1.2'], impact='serious'),
        ]),
    ]

    rows = axe_rules(results)

    assert rows == [
        {'rule_id': 'target-size', 'wcag': ['2.5.8'], 'level': 'AA', 'impact': 'serious', 'desktop': 25, 'mobile': 4},
        {'rule_id': 'link-name', 'wcag': ['2.4.4', '4.1.2'], 'level': 'A', 'impact': 'serious', 'desktop': 7, 'mobile': 12},
    ]


def test_ibm_rules_lists_each_rule_with_looked_up_wcag_level_and_per_viewport_counts():
    results = [
        _result('desktop', 'ibm-equal-access', [
            _violation('a_text_purpose', 8, tool='ibm-equal-access'),
            _violation('aria_content_in_landmark', 6, tool='ibm-equal-access'),
        ]),
        _result('mobile', 'ibm-equal-access', [
            _violation('a_text_purpose', 12, tool='ibm-equal-access'),
            _violation('aria_content_in_landmark', 3, tool='ibm-equal-access'),
        ]),
    ]

    rows = ibm_rules(results)

    assert rows == [
        {'rule_id': 'a_text_purpose', 'wcag': ['2.4.4', '4.1.2'], 'level': 'A', 'desktop': 8, 'mobile': 12},
        {'rule_id': 'aria_content_in_landmark', 'wcag': ['1.3.1'], 'level': 'A', 'desktop': 6, 'mobile': 3},
    ]


def test_ibm_buckets_reads_each_summary_count_category_per_viewport():
    desktop = {'violation': 14, 'potentialviolation': 38, 'recommendation': 1,
               'potentialrecommendation': 69, 'manual': 16, 'pass': 4983}
    mobile = {'violation': 40, 'potentialviolation': 47, 'recommendation': 1,
              'potentialrecommendation': 53, 'manual': 35, 'pass': 4940}
    results = [
        _result('desktop', 'ibm-equal-access', [], raw={'summary': {'counts': desktop}}),
        _result('mobile', 'ibm-equal-access', [], raw={'summary': {'counts': mobile}}),
    ]

    rows = ibm_buckets(results)

    assert rows == [
        {'category': 'violation', 'desktop': 14, 'mobile': 40},
        {'category': 'potentialviolation', 'desktop': 38, 'mobile': 47},
        {'category': 'recommendation', 'desktop': 1, 'mobile': 1},
        {'category': 'potentialrecommendation', 'desktop': 69, 'mobile': 53},
        {'category': 'manual', 'desktop': 16, 'mobile': 35},
    ]


def test_by_impact_totals_axe_occurrences_per_impact_across_viewports():
    results = [
        _result('desktop', 'axe-core', [
            _violation('image-alt', 20, impact='critical'),
            _violation('target-size', 25, impact='serious'),
        ]),
        _result('mobile', 'axe-core', [
            _violation('image-alt', 20, impact='critical'),
            _violation('target-size', 4, impact='serious'),
        ]),
    ]

    rows = by_impact(results)

    assert rows == [
        {'impact': 'critical', 'occurrences': 40},
        {'impact': 'serious', 'occurrences': 29},
    ]


def test_by_criterion_totals_axe_occurrences_per_wcag_criterion():
    results = [
        _result('desktop', 'axe-core', [_violation('link-name', 7, wcag=['2.4.4', '4.1.2'])]),
        _result('mobile', 'axe-core', [_violation('link-name', 12, wcag=['2.4.4', '4.1.2'])]),
    ]

    rows = by_criterion(results, 'axe-core')

    assert rows == [
        {'criterion': '2.4.4', 'principle': 'Operable', 'level': 'A', 'occurrences': 19},
        {'criterion': '4.1.2', 'principle': 'Robust', 'level': 'A', 'occurrences': 19},
    ]


def test_by_criterion_uses_the_ibm_lookup_for_occurrences_per_criterion():
    results = [
        _result('desktop', 'ibm-equal-access', [_violation('a_text_purpose', 8, tool='ibm-equal-access')]),
        _result('mobile', 'ibm-equal-access', [_violation('a_text_purpose', 12, tool='ibm-equal-access')]),
    ]

    rows = by_criterion(results, 'ibm-equal-access')

    assert rows == [
        {'criterion': '2.4.4', 'principle': 'Operable', 'level': 'A', 'occurrences': 20},
        {'criterion': '4.1.2', 'principle': 'Robust', 'level': 'A', 'occurrences': 20},
    ]


def test_by_principle_rolls_occurrences_up_to_pour_principles_in_canonical_order():
    results = [
        _result('desktop', 'axe-core', [
            _violation('image-alt', 10, wcag=['1.1.1']),
            _violation('link-name', 7, wcag=['2.4.4', '4.1.2']),
        ]),
        _result('mobile', 'axe-core', [
            _violation('image-alt', 10, wcag=['1.1.1']),
            _violation('link-name', 12, wcag=['2.4.4', '4.1.2']),
        ]),
    ]

    rows = by_principle(results, 'axe-core')

    assert rows == [
        {'principle': 'Perceivable', 'occurrences': 20},
        {'principle': 'Operable', 'occurrences': 19},
        {'principle': 'Robust', 'occurrences': 19},
    ]


def test_by_level_rolls_occurrences_up_to_conformance_levels_a_before_aa():
    results = [
        _result('desktop', 'axe-core', [
            _violation('target-size', 25, wcag=['2.5.8']),
            _violation('link-name', 7, wcag=['2.4.4', '4.1.2']),
        ]),
        _result('mobile', 'axe-core', [
            _violation('target-size', 4, wcag=['2.5.8']),
            _violation('link-name', 12, wcag=['2.4.4', '4.1.2']),
        ]),
    ]

    rows = by_level(results, 'axe-core')

    assert rows == [
        {'level': 'A', 'occurrences': 38},
        {'level': 'AA', 'occurrences': 29},
    ]


def test_viewport_criteria_partitions_wcag_criteria_shared_or_specific_to_each_viewport():
    results = [
        _result('desktop', 'axe-core', [
            _violation('link-name', 7, wcag=['2.4.4', '4.1.2']),
            _violation('target-size', 25, wcag=['2.5.8']),
        ]),
        _result('desktop', 'ibm-equal-access', [
            _violation('aria_content_in_landmark', 6, tool='ibm-equal-access'),
        ]),
        _result('mobile', 'axe-core', [
            _violation('link-name', 12, wcag=['2.4.4', '4.1.2']),
        ]),
        _result('mobile', 'ibm-equal-access', [
            _violation('img_alt_redundant', 3, tool='ibm-equal-access'),
        ]),
    ]

    partition = viewport_criteria(results)

    assert partition == {
        'shared': ['2.4.4', '4.1.2'],
        'desktop_only': ['1.3.1', '2.5.8'],
        'mobile_only': ['1.1.1'],
    }


def test_priorities_ranks_axe_rules_by_impact_then_level_a_over_aa_then_frequency():
    results = [
        _result('desktop', 'axe-core', [
            _violation('image-alt', 5, wcag=['1.1.1'], impact='critical'),
            _violation('target-size', 20, wcag=['2.5.8'], impact='serious'),
            _violation('link-name', 10, wcag=['2.4.4', '4.1.2'], impact='serious'),
            _violation('color-contrast', 2, wcag=['1.4.3'], impact='serious'),
        ]),
        _result('mobile', 'axe-core', [
            _violation('image-alt', 5, wcag=['1.1.1'], impact='critical'),
            _violation('target-size', 9, wcag=['2.5.8'], impact='serious'),
            _violation('link-name', 9, wcag=['2.4.4', '4.1.2'], impact='serious'),
            _violation('color-contrast', 2, wcag=['1.4.3'], impact='serious'),
        ]),
    ]

    rows = priorities(results)

    assert rows == [
        {'rule_id': 'image-alt', 'wcag': ['1.1.1'], 'level': 'A', 'impact': 'critical', 'occurrences': 10},
        {'rule_id': 'link-name', 'wcag': ['2.4.4', '4.1.2'], 'level': 'A', 'impact': 'serious', 'occurrences': 19},
        {'rule_id': 'target-size', 'wcag': ['2.5.8'], 'level': 'AA', 'impact': 'serious', 'occurrences': 29},
        {'rule_id': 'color-contrast', 'wcag': ['1.4.3'], 'level': 'AA', 'impact': 'serious', 'occurrences': 4},
    ]
