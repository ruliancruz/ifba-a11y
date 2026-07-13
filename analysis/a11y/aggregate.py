from a11y.wcag import ibm_criteria, level, principle

_IMPACT_ORDER = ['critical', 'serious', 'moderate', 'minor']

_IBM_BUCKETS = [
    'violation',
    'potentialviolation',
    'recommendation',
    'potentialrecommendation',
    'manual',
    'pass',
]


def _by_device_tool(results):
    return {(r.metadata.device, r.metadata.tool): r for r in results}


def _devices(results):
    width = {}
    for r in results:
        width[r.metadata.device] = r.metadata.viewport['width'] if r.metadata.viewport else 0
    return sorted(width, key=width.get, reverse=True)


def _per_device_counts(results, tool):
    index = _by_device_tool(results)
    devices = _devices(results)
    counts = {}
    sample = {}
    for device in devices:
        for v in index[(device, tool)].violations:
            counts.setdefault(v.rule_id, {})[device] = v.count
            sample.setdefault(v.rule_id, v)
    return devices, counts, sample


def _levels(criteria):
    return '/'.join(sorted({level(c) for c in criteria}))


def _by_frequency(rows, devices):
    return sorted(rows, key=lambda r: (-sum(r[d] for d in devices), r['rule_id']))


def overview(results):
    index = _by_device_tool(results)
    rows = []
    for device in _devices(results):
        axe = index[(device, 'axe-core')]
        ibm = index[(device, 'ibm-equal-access')]
        rows.append({
            'device': device,
            'axe_rules': len(axe.violations),
            'axe_occurrences': sum(v.count for v in axe.violations),
            'ibm_violations': sum(v.count for v in ibm.violations),
        })
    return rows


def by_impact(results):
    index = _by_device_tool(results)
    totals = {}
    for device in _devices(results):
        for v in index[(device, 'axe-core')].violations:
            totals[v.impact] = totals.get(v.impact, 0) + v.count
    return [{'impact': i, 'occurrences': totals[i]} for i in _IMPACT_ORDER if i in totals]


def by_criterion(results, tool):
    index = _by_device_tool(results)
    totals = {}
    for device in _devices(results):
        for v in index[(device, tool)].violations:
            criteria = v.wcag if tool == 'axe-core' else ibm_criteria(v.rule_id)
            for c in criteria:
                totals[c] = totals.get(c, 0) + v.count
    return [
        {'criterion': c, 'principle': principle(c), 'level': level(c), 'occurrences': totals[c]}
        for c in sorted(totals)
    ]


def axe_rules(results):
    devices, counts, sample = _per_device_counts(results, 'axe-core')
    rows = []
    for rule_id, v in sample.items():
        row = {'rule_id': rule_id, 'wcag': v.wcag, 'level': _levels(v.wcag), 'impact': v.impact}
        for device in devices:
            row[device] = counts[rule_id].get(device, 0)
        rows.append(row)
    return _by_frequency(rows, devices)


def ibm_buckets(results):
    index = _by_device_tool(results)
    devices = _devices(results)
    rows = []
    for category in _IBM_BUCKETS:
        row = {'category': category}
        for device in devices:
            row[device] = index[(device, 'ibm-equal-access')].raw['summary']['counts'][category]
        rows.append(row)
    return rows


def ibm_rules(results):
    devices, counts, sample = _per_device_counts(results, 'ibm-equal-access')
    rows = []
    for rule_id in sample:
        criteria = ibm_criteria(rule_id)
        row = {'rule_id': rule_id, 'wcag': criteria, 'level': _levels(criteria)}
        for device in devices:
            row[device] = counts[rule_id].get(device, 0)
        rows.append(row)
    return _by_frequency(rows, devices)
