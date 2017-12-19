from __future__ import print_function
from collections import defaultdict
import wufoo_entry_loader

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

def join_tables(R, S, key):
    join = []
    for r in R:
        for s in S:
            if key(r, s):
                join.append((r, s))
    return join

def unique_tuples(join, key):
    unique = defaultdict(list)
    for (r, s) in join:
        if r not in unique[key(r)]:
            unique[key(r)].append(r)
        if s not in unique[key(r)]:
            unique[key(r)].append(s)
    return unique

def partial_match(app, reference):
    return app['first_name'] == reference['applicant_first_name'] or \
            app['last_name'] == reference['applicant_last_name']

def main():
    print(make_color('This script should output no issues (besides missing references) ' +\
            'before you continue running other scripts.', 'red'))
    print()

    # submission_time allows us to differentiate entries
    apps = wufoo_entry_loader.load_apps(fields=[
        'first_name', 'last_name', 'full_name', 'email', 'submission_time'])
    references = wufoo_entry_loader.load_references(fields=[
        'applicant_first_name', 'applicant_last_name', 'applicant_full_name',
        'reference_first_name', 'reference_last_name', 'reference_full_name',
        'submission_time'])

    ### DUPLICATE APPS ###

    duplicate_apps = unique_tuples(
        join_tables(apps, apps, lambda a1, a2: a1['full_name'] == a2['full_name'] and a1 != a2),
        key=lambda app: app['full_name'])

    for (name, matches) in duplicate_apps.items():
        print('Applicant {} submitted {} written applications.'.format(
            make_color(name, 'red'),
            len(matches)
        ))

    if len(duplicate_apps) > 0: print()

    ### DUPLICATE REFERENCES ###

    duplicate_references = unique_tuples(
        join_tables(references, references,
            lambda r1, r2: r1['applicant_full_name'] == r2['applicant_full_name'] and r1 != r2),
        key=lambda reference: reference['applicant_full_name'])

    for (name, duplicates) in duplicate_references.items():
        print('Applicant {} has multiple letters of reference from {} and {}.'.format(
            make_color(name, 'red'),
            make_color(', '.join(reference['reference_full_name'] for reference in duplicates[:-1]), 'red'),
            make_color(duplicates[-1]['reference_full_name'], 'red')
        ))

    if len(duplicate_references) > 0: print()

    # This removes all matched apps and references, so we don't have to deal with them below.
    have_references = join_tables(apps, references, lambda a, r: a['full_name'] == r['applicant_full_name'])
    for (a, r) in have_references:
        if a in apps:
            apps.remove(a)
        if r in references:
            references.remove(r)

    ### REFERENCES WITHOUT APPS ###

    found = False
    for reference in references:
        matching_apps = join_tables([reference], apps,
                lambda r, a: partial_match(a, r))  # we don't want to include partial matches since those printed below
        if len(matching_apps) == 0:
            found = True
            print('We have a letter of reference for {} (written by {}) but no matching application.'.format(
                make_color(reference['applicant_full_name'], 'blue'),
                reference['reference_full_name']))

    if found:
        print()
        found = False

    ### APPS WITHOUT REFERENCES ###

    for app in apps:
        matching_references = join_tables([app], references,
                lambda a, r: partial_match(a, r))
        if len(matching_references) == 0:
            found = True
            print('We have an application for {} ({}) but no letter of reference.'.format(
                make_color(app['full_name'], 'cyan'),
                app['email']
            ))

    if found:
        print()
        found = False
    
    ### PARTIAL REFERENCE MATCHES ###

    for app in apps:
        matches = join_tables([app], references,
                lambda a, r: partial_match(a, r))
        if len(matches) > 0:
            if not found:
                print(make_color('We can\'t find matching letters of reference for applicants below, but do have references for people\n' +\
                    'with partially matching names (first or last name matches).', 'bold'))
                found = True
            print('{} ({}): {}'.format(
                make_color(app['full_name'], 'green'),
                app['email'],
                ', '.join('{} (written by {})'.format(
                    make_color(match[1]['applicant_full_name'], 'green'), match[1]['reference_full_name']) for match in matches)
            ))

if __name__ == '__main__':
    main()

