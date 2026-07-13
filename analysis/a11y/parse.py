from a11y.schema import Metadata, Result, Violation


def _violation(v):
    return Violation(
        tool=v['tool'],
        rule_id=v['ruleId'],
        wcag=v['wcag'],
        description=v['description'],
        count=v['count'],
        targets=v['targets'],
        impact=v.get('impact'),
        help_url=v.get('helpUrl'),
    )


def _metadata(m):
    return Metadata(
        timestamp=m['timestamp'],
        url=m['url'],
        browser=m['browser'],
        browser_version=m['browserVersion'],
        viewport=m['viewport'],
        device=m['device'],
        tool=m['tool'],
        tool_version=m['toolVersion'],
        wcag_tags=m.get('wcagTags'),
    )


def parse_result(data):
    return Result(
        metadata=_metadata(data['metadata']),
        violations=[_violation(v) for v in data['violations']],
        raw=data['raw'],
    )
