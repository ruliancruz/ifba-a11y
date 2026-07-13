from a11y.aggregate import by_criterion


def compare(results):
    axe = {row['criterion'] for row in by_criterion(results, 'axe-core')}
    ibm = {row['criterion'] for row in by_criterion(results, 'ibm-equal-access')}
    return {
        'shared': sorted(axe & ibm),
        'axe_only': sorted(axe - ibm),
        'ibm_only': sorted(ibm - axe),
    }
