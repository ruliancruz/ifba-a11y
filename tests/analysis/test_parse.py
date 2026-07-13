from a11y.parse import parse_result
from a11y.schema import Metadata, Result, Violation


def test_parses_a_result_file_into_typed_dataclasses():
    data = {
        'metadata': {
            'timestamp': '2026-05-14T12:00:00.000Z',
            'url': 'https://portal.ifba.edu.br/',
            'browser': 'chromium',
            'browserVersion': '145.0.7632.6',
            'viewport': {'width': 1280, 'height': 720},
            'device': 'desktop',
            'tool': 'axe-core',
            'toolVersion': '4.12.1',
            'wcagTags': ['wcag2a', 'wcag22aa'],
        },
        'violations': [
            {
                'tool': 'axe-core',
                'ruleId': 'link-name',
                'wcag': ['2.4.4', '4.1.2'],
                'description': 'Ensure links have discernible text',
                'count': 7,
                'targets': ['#logovlibras', 'a.tile'],
                'impact': 'serious',
                'helpUrl': 'https://example.test/rules/link-name',
            },
        ],
        'raw': {'testEngine': {'name': 'axe-core', 'version': '4.12.1'}},
    }

    result = parse_result(data)

    assert result == Result(
        metadata=Metadata(
            timestamp='2026-05-14T12:00:00.000Z',
            url='https://portal.ifba.edu.br/',
            browser='chromium',
            browser_version='145.0.7632.6',
            viewport={'width': 1280, 'height': 720},
            device='desktop',
            tool='axe-core',
            tool_version='4.12.1',
            wcag_tags=['wcag2a', 'wcag22aa'],
        ),
        violations=[
            Violation(
                tool='axe-core',
                rule_id='link-name',
                wcag=['2.4.4', '4.1.2'],
                description='Ensure links have discernible text',
                count=7,
                targets=['#logovlibras', 'a.tile'],
                impact='serious',
                help_url='https://example.test/rules/link-name',
            ),
        ],
        raw={'testEngine': {'name': 'axe-core', 'version': '4.12.1'}},
    )


def test_defaults_absent_optional_fields_to_none():
    data = {
        'metadata': {
            'timestamp': '2026-05-14T12:00:00.000Z',
            'url': 'https://portal.ifba.edu.br/',
            'browser': 'chromium',
            'browserVersion': '145.0.7632.6',
            'viewport': {'width': 375, 'height': 667},
            'device': 'mobile',
            'tool': 'ibm-equal-access',
            'toolVersion': '4.0.26',
        },
        'violations': [
            {
                'tool': 'ibm-equal-access',
                'ruleId': 'a_text_purpose',
                'wcag': [],
                'description': 'Hyperlink has no link text',
                'count': 12,
                'targets': ['/html[1]/body[1]/a[1]'],
                'helpUrl': 'https://example.test/rules/a_text_purpose',
            },
        ],
        'raw': {'summary': {'counts': {'violation': 40}}},
    }

    result = parse_result(data)

    assert result == Result(
        metadata=Metadata(
            timestamp='2026-05-14T12:00:00.000Z',
            url='https://portal.ifba.edu.br/',
            browser='chromium',
            browser_version='145.0.7632.6',
            viewport={'width': 375, 'height': 667},
            device='mobile',
            tool='ibm-equal-access',
            tool_version='4.0.26',
            wcag_tags=None,
        ),
        violations=[
            Violation(
                tool='ibm-equal-access',
                rule_id='a_text_purpose',
                wcag=[],
                description='Hyperlink has no link text',
                count=12,
                targets=['/html[1]/body[1]/a[1]'],
                impact=None,
                help_url='https://example.test/rules/a_text_purpose',
            ),
        ],
        raw={'summary': {'counts': {'violation': 40}}},
    )
