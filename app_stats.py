from __future__ import print_function
import wufoo_entry_loader

def make_color(val, color):
    colors = {
        'red': '\033[1;31m',
        'blue': '\033[1;34m',
        'cyan': '\033[1;36m',
        'green': '\033[0;32m',
        'bold': '\033[1m',
        'italic': '\033[3m',
        'reset': '\033[0;0m'
    }
    return colors[color] + val + colors['reset']

def count_year_by_gender(apps, year):
    male = []
    female = []
    nonbinary = []

    male_identifiers = ['male', 'mal', 'cis male',
            'cis mal', 'man', 'cis man', 'men', 'boy', 'm']
    female_identifiers = ['female', 'femal', 'cis female',
            'cis femal', 'woman', 'women', 'cis woman', 'girl', 'f']

    for app in apps:
        if app['school_year'] != year:
            continue

        if app['gender'] in male_identifiers:
            male.append(app)
        elif app['gender'] in female_identifiers:
            female.append(app)
        else:
            nonbinary.append(app)

    return (male, female, nonbinary)

def main():
    apps = wufoo_entry_loader.load_apps(fields=['full_name', 'school_year', 'gender'])
    for year in ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Co-Term']:
        male, female, nonbinary = count_year_by_gender(apps, year)
        total = len(male) + len(female) + len(nonbinary)
        print('{}: {}'.format(make_color(year, 'bold'), make_color('{} applicants'.format(total), 'italic')))
        print('  {} of those are male'.format(len(male)))
        print('  {} of those are female'.format(len(female)))
        print('  {} of those are nonbinary'.format(len(nonbinary)))
        print()

if __name__ == '__main__':
    main()
