import json
from pathlib import Path

from a11y.parse import parse_result

VIEWPORTS = ['desktop', 'mobile']
TOOLS = ['axe', 'ibm']


def load_results(results_dir):
    directory = Path(results_dir)
    results = []
    for viewport in VIEWPORTS:
        for tool in TOOLS:
            path = directory / viewport / f'{tool}.json'
            results.append(parse_result(json.loads(path.read_text())))
    return results
