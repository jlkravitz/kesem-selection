# TODO: Find all partial matches for each applicant.
import csv
from collections import defaultdict
import textwrap

COMPLETION_STATUS_COL = -1

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

def preprocess_name(name):
    return ' '.join(name.strip().lower().split())

def make_name(obj, key_prefix=''):
    return '{} {}'.format(obj['{}first_name'.format(key_prefix)], obj['{}last_name'.format(key_prefix)])

def load_apps():
    """Load apps CSV from exported Wufoo entries."""
    with open('apps.csv', encoding='ISO-8859-1') as f:
        return [
            {
                'first_name': preprocess_name(app[1]),
                'last_name': preprocess_name(app[2]),
                'email': app[9],
                'matched': False
            }
            for app in csv.reader(f)
            if app[COMPLETION_STATUS_COL] == '1'
        ]

def load_lors():
    """Load applicant names in letters of reference from exported Wufoo entries."""
    with open('lors.csv', encoding='ISO-8859-1') as f:
        return [
            {
                'first_name': preprocess_name(lor[5]),
                'last_name': preprocess_name(lor[6]),
                'reference_first_name': preprocess_name(lor[1]),
                'reference_last_name': preprocess_name(lor[2]),
                'matched': False
            }
            for lor in csv.reader(f)
            if lor[COMPLETION_STATUS_COL] == '1'
        ]

def find_matching_lors(app, lors):
    """Find unmatched lor for given app, returning lor match and the type (if partial, full, or none)."""
    full_matches = []
    matches = []
    for lor in lors:
        if lor['matched']: continue
        if make_name(app) == make_name(lor): #app['first_name'] == lor['first_name'] and app['last_name'] == lor['last_name']:
            full_matches.append(lor)
        elif app['first_name'] == lor['first_name'] or app['last_name'] == lor['last_name']:
            matches.append(lor)

    return (full_matches, FULL_MATCH) if full_matches else (matches, PARTIAL_MATCH) if matches else ([], NO_MATCH)

def mark_full_matches(apps, lors):
    """Mark apps and lors as matched when first and last name fully match."""
    # First, mark full matches.
    multiple_full_matches = []
    for app in apps:
        matched_lors, match_type = find_matching_lors(app, lors)
        if match_type == FULL_MATCH:
            if len(matched_lors) > 1:
                multiple_full_matches.append((app, matched_lors))
            app['matched'] = True
            for matched_lor in matched_lors:
                matched_lor['matched'] = True
    return multiple_full_matches

def find_uncertain_matches(apps, lors):
    """Check for partial or no match for unmatched apps."""
    # Find partial matches for each unmatched applicant and lor.
    matches = defaultdict(list)
    for app in apps:
        if app['matched']: continue
        matching_lors, match_type = find_matching_lors(app, lors)
        matches[match_type].append((app, matching_lors))
    return matches

def report_uncertain_matches(app_lor_matches, lor_app_matches): 
    """Report partial and no matches in passed list.

    List holds tuples of (app, lor).
    """

    colors = {
        'red': '\033[1;31m',
        'blue': '\033[1;34m',
        'cyan': '\033[1;36m',
        'green': '\033[0;32m'
    }
    def print_app_lor_match(match, color):
        print('{}{: <30}{: <30}{: <40}{: <40}\033[0;0m'.format(
            colors[color],
            make_name(match[0]),
            match[0]['email'],
            ', '.join(make_name(lor, key_prefix='reference_') for lor in match[1]),
            ', '.join(make_name(lor) for lor in match[1])))
    def print_lor_app_match(match, color):
        print('{}{: <30}{: <30}{: <40}{: <40}'.format(
            colors[color],
            '', '',
            make_name(match[0], key_prefix='reference_'),
            make_name(match[0])))

    print('{: <30}{: <30}{: <40}{: <40}'.format('Applicant', 'Stanford Email', 'Reference', 'Referee'))
    print('{: <30}{: <30}{: <40}{: <40}'.format('-' * 25, '-' * 25, '-' * 25, '-' * 25))

    for match in app_lor_matches[FULL_MATCH]:
        print_app_lor_match(match, 'red')
    for match in app_lor_matches[NO_MATCH]:
        print_app_lor_match(match, 'cyan')
    for match in lor_app_matches[NO_MATCH]:
        print_lor_app_match(match, 'blue')
    for match in app_lor_matches[PARTIAL_MATCH]:
        print_app_lor_match(match, 'green')

def main():
    print(WELCOME_MESSAGE)
    print('Press enter to continue.')
    input()

    apps = load_apps()
    lors = load_lors()

    # These full matches are only those that have *more than one*
    # fully matching letter of reference.
    app_lor_matches_full = mark_full_matches(apps, lors)
    app_lor_matches = find_uncertain_matches(apps, lors)
    assert len(app_lor_matches[FULL_MATCH]) == 0, 'Found full matches. Something seems wrong...'
    app_lor_matches[FULL_MATCH] = app_lor_matches_full

    # This finds lors without matching applications.
    lor_app_matches = find_uncertain_matches(lors, apps)

    report_uncertain_matches(app_lor_matches, lor_app_matches)

if __name__ == '__main__':
    main()

