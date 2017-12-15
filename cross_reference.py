from collections import defaultdict
import wufoo_entry_loader

# Match types for applicants with Letters of Reference
NO_MATCH = 0
PARTIAL_MATCH = 1
FULL_MATCH = 3

WELCOME_MESSAGE = """Welcome! This script is here to help you cross reference applications with letters of
reference. It detects...

    • Applicants who have more than one letter of reference. If this occurs,
      the applicant's name will show up twice under "Referee".

    • Applicants who have no matching letter of reference. If this occurs,
      the applicant's Reference and Referee columns will be missing.

    • Letters of reference with no matching applicant. This is shown as a row in the  
      table below whose Applicant and Email columns are missing. 

    • Applicants who have partial matches to one or more letters of reference.
      This means the applicant's first or last name (but not both) matches those
      on the listed letters of reference. Usually, this means the reference
      spelled the applicant's name wrong, but sometimes can mean that the applicant
      doesn't have a letter of reference. You will have to decide this for yourself.
      If partial matches occur, the applicant's Referee column will partially match
      the applicant's name.

Questions? Email Finchley at kravitzj@stanford.edu.
"""

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
        'green': '\033[0;32m'
    }

    def print_app_reference_match(match, color):
        print('{}{: <30}{: <30}{: <40}{: <40}\033[0;0m'.format(
            colors[color],
            match[0]['full_name'],
            match[0]['email'],
            ', '.join(reference['reference_full_name'] for reference in match[1]),
            ', '.join(reference['full_name'] for reference in match[1])))

    def print_reference_app_match(match, color):
        print('{}{: <30}{: <30}{: <40}{: <40}'.format(
            colors[color],
            '', '',
            match[0]['reference_full_name'],
            match[0]['full_name']))

    print('{: <30}{: <30}{: <40}{: <40}'.format('Applicant', 'Stanford Email', 'Reference', 'Referee'))
    print('{: <30}{: <30}{: <40}{: <40}'.format('-' * 25, '-' * 25, '-' * 25, '-' * 25))

    for match in app_reference_matches[FULL_MATCH]:
        print_app_reference_match(match, 'red')
    for match in app_reference_matches[NO_MATCH]:
        print_app_reference_match(match, 'cyan')
    for match in reference_app_matches[NO_MATCH]:
        print_reference_app_match(match, 'blue')
    for match in app_reference_matches[PARTIAL_MATCH]:
        print_app_reference_match(match, 'green')

def main():
    print(WELCOME_MESSAGE)
    print('Press enter to continue.')
    input()

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

