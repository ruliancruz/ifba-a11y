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
