from a11y.aggregate import by_criterion
from a11y.wcag import counterpart, ibm_criteria, level


def compare(results):
    axe = {row['criterion'] for row in by_criterion(results, 'axe-core')}
    ibm = {row['criterion'] for row in by_criterion(results, 'ibm-equal-access')}
    return {
        'shared': sorted(axe & ibm),
        'axe_only': sorted(axe - ibm),
        'ibm_only': sorted(ibm - axe),
    }


def _axe_criteria(results):
    criteria = {}
    for result in results:
        if result.metadata.tool != 'axe-core':
            continue
        for violation in result.violations:
            criteria.setdefault(violation.rule_id, list(violation.wcag))
    return criteria


def _ibm_rules(results):
    return {
        violation.rule_id
        for result in results if result.metadata.tool == 'ibm-equal-access'
        for violation in result.violations
    }


def _row(axe_rule, ibm_rule, criteria, detection):
    return {
        'axe_rule': axe_rule,
        'ibm_rule': ibm_rule,
        'criteria': sorted(criteria),
        'level': '/'.join(sorted({level(c) for c in criteria})),
        'detection': detection,
    }


def rule_pairs(results):
    axe = _axe_criteria(results)
    ibm = _ibm_rules(results)
    rows = []
    for rule_id, criteria in axe.items():
        mate = counterpart(rule_id)
        paired = mate if mate in ibm else None
        rows.append(_row(rule_id, paired, criteria, 'both' if paired else 'axe_only'))
    for rule_id in ibm:
        if counterpart(rule_id) in axe:
            continue
        rows.append(_row(None, rule_id, ibm_criteria(rule_id), 'ibm_only'))
    return sorted(rows, key=lambda row: (row['criteria'], row['axe_rule'] or row['ibm_rule']))
