import re

_FOOTER_LINKS = (
    'instituto',
    'memorial',
    'organograma/',
    'quem-e-quem/',
    'dados.ifba.edu.br/',
    'doc',
    'seja-nosso-aluno',
    'tipos-de-cursos',
    'nossos-cursos',
    'ead',
    'sisproc.ifba.edu.br/',
)

_FOOTER_HREFS = '|'.join(re.escape(href) for href in _FOOTER_LINKS)

_COMPONENTS = (
    ('banner_rotator', re.compile(r'#banner\d+\b')),
    ('grid_footer', re.compile(rf'doormat|href\$="(?:{_FOOTER_HREFS})"')),
    ('news_tile', re.compile(r'nitf-basic-tile')),
)

_ORDER = [label for label, _ in _COMPONENTS] + ['other']


def component(selector):
    for label, pattern in _COMPONENTS:
        if pattern.search(selector):
            return label
    return 'other'


def component_counts(results, rule_id, device):
    totals = {}
    for result in results:
        if result.metadata.device != device:
            continue
        for violation in result.violations:
            if violation.rule_id != rule_id:
                continue
            for target in violation.targets:
                label = component(target)
                totals[label] = totals.get(label, 0) + 1
    return [{'component': c, 'occurrences': totals[c]} for c in _ORDER if c in totals]
