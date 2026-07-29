def _rules(results, tool):
    return {v.rule_id for r in results if r.metadata.tool == tool for v in r.violations}


def target_rules(reference, live, tool):
    ref = _rules(reference, tool)
    liv = _rules(live, tool)
    return {
        'shared': sorted(ref & liv),
        'reference_only': sorted(ref - liv),
        'live_only': sorted(liv - ref),
    }


def _selectors(results, tool, device):
    by_rule = {}
    for result in results:
        if result.metadata.tool != tool or result.metadata.device != device:
            continue
        for violation in result.violations:
            by_rule.setdefault(violation.rule_id, set()).update(violation.targets)
    return by_rule


def target_selectors(reference, live, tool, device):
    ref = _selectors(reference, tool, device)
    liv = _selectors(live, tool, device)
    return {
        rule_id: {
            'shared': sorted(ref.get(rule_id, set()) & liv.get(rule_id, set())),
            'reference_only': sorted(ref.get(rule_id, set()) - liv.get(rule_id, set())),
            'live_only': sorted(liv.get(rule_id, set()) - ref.get(rule_id, set())),
        }
        for rule_id in sorted(set(ref) | set(liv))
    }
