from collections import defaultdict
import wufoo_entry_loader

# Match types for applicants with Letters of Reference
NO_MATCH = 0
PARTIAL_MATCH = 1
FULL_MATCH = 3

def find_matching_references(app, references):
    """Find unmatched reference for given app, returning reference match and the type (if partial, full, or none)."""
    full_matches = []
    matches = []
    for reference in references:
        if reference['matched']: continue
        if app['full_name'] == reference['full_name']:
            full_matches.append(reference)
        elif app['first_name'] == reference['first_name'] or app['last_name'] == reference['last_name']:
            matches.append(reference)

    return (full_matches, FULL_MATCH) if full_matches else (matches, PARTIAL_MATCH) if matches else ([], NO_MATCH)

def mark_full_matches(apps, references):
    """Mark apps and references as matched when first and last name fully match."""
    # First, mark full matches.
    multiple_full_matches = []
    for app in apps:
        matched_references, match_type = find_matching_references(app, references)
        if match_type == FULL_MATCH:
            if len(matched_references) > 1:
                multiple_full_matches.append((app, matched_references))
            app['matched'] = True
            for matched_reference in matched_references:
                matched_reference['matched'] = True
    return multiple_full_matches

def find_uncertain_matches(apps, references):
    """Check for partial or no match for unmatched apps."""
    # Find partial matches for each unmatched applicant and reference.
    matches = defaultdict(list)
    for app in apps:
        if app['matched']: continue
        matching_references, match_type = find_matching_references(app, references)
        matches[match_type].append((app, matching_references))
    return matches

def report_uncertain_matches(app_reference_matches, reference_app_matches): 
    """Report partial and no matches in passed list.

    List holds tuples of (app, reference).
    """

    colors = {
        'red': '\033[1;31m',
        'blue': '\033[1;34m',
        'cyan': '\033[1;36m',
        'green': '\033[0;32m',
        'bold': '\033[1m',
        'reset': '\033[0;0m'
    }

    def make_color(val, color):
        return colors[color] + val + colors['reset']

    for match in app_reference_matches[FULL_MATCH]:
        print('Applicant {} ({}) has multiple letters of reference from {} and {}.'.format(
            make_color(match[0]['full_name'], 'red'),
            match[0]['email'],
            make_color(', '.join(reference['reference_full_name'] for reference in match[1][1:]), 'red'),
            make_color(match[1][0]['reference_full_name'], 'red')
        ))

    print()

    for match in app_reference_matches[NO_MATCH]:
        print('Applicant {} ({}) has no letter of reference.'.format(
            make_color(match[0]['full_name'], 'cyan'),
            match[0]['email']
        ))

    print()
    
    for match in reference_app_matches[NO_MATCH]:
        print('We have a letter of reference for {} (written by {}) but no matching application.'.format(
            make_color(match[0]['full_name'], 'blue'),
            match[0]['reference_full_name']
        ))

    print()

    print(make_color('We can\'t find matching letters of reference for applicants below, but do have references for people\n' +\
            'with partially matching names (first or last name matches).', 'bold'))
    for match in app_reference_matches[PARTIAL_MATCH]:
        print('{} ({}): {}'.format(
            make_color(match[0]['full_name'], 'green'),
            match[0]['email'],
            ', '.join('{} (written by {})'.format(make_color(reference['full_name'], 'green'), reference['reference_full_name']) for reference in match[1]), 'green'
        ))

def main():
    apps = wufoo_entry_loader.load_apps(fields=[
        'first_name', 'last_name', 'full_name', 'email'],
        metadata={
            'matched': False
        })

    references = wufoo_entry_loader.load_references(
        fields=[
            'applicant_first_name', 'applicant_last_name', 'applicant_full_name',
            'reference_first_name', 'reference_last_name', 'reference_full_name'
        ],
        rename={
            'applicant_first_name': 'first_name',
            'applicant_last_name': 'last_name',
            'applicant_full_name': 'full_name'
        },
        metadata={
            'matched': False
        }
    )

    # These full matches are only those that have *more than one*
    # fully matching letter of reference.
    app_reference_matches_full = mark_full_matches(apps, references)
    app_reference_matches = find_uncertain_matches(apps, references)
    assert len(app_reference_matches[FULL_MATCH]) == 0, 'Found full matches. Something seems wrong...'
    app_reference_matches[FULL_MATCH] = app_reference_matches_full

    # This finds references without matching applications.
    reference_app_matches = find_uncertain_matches(references, apps)

    report_uncertain_matches(app_reference_matches, reference_app_matches)

if __name__ == '__main__':
    main()

