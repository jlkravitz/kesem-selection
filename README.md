# Kesem Presents: Computer Science

Welcome to the GitHub repository full of fun, fancy scripts meant to
run on Camp Kesem applications and letters of reference from Wufoo.

## History

Before the electronic application, Camp Kesem used PDF applications sent
to the CoCo email account. Well, never more! Kesem and Computer Science
have finally joined hands.

Wufoo allows users to export entries (submissions of a form) into a CSV
or Excel format. We use CSV, which is easier to manipulate programatically.

CSV stands for comma-separated values, which is basically an Excel document
represented in text format (see
[Wikipedia](https://en.wikipedia.org/wiki/Comma-separated_values#Example)
for an example).

But since applications and references are in CSV format, they're almost impossible
to read! So these scripts are here to help with that (among other things).

## Computer Setup

To get these scripts running, run the following commands in your terminal.

1. Navigate to your "Documents" directory: `cd ~/Documents`
2. Clone this github repository: `git clone git@github.com:jlkravitz/kesem-selection.git`
3. Navigate to the new directory: `cd kesem-selection`
4. Install Homebrew (This is safe and fast! I swear!): `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
5. Install python3: `brew install python3`
6. Install fpdf, a python library for building pdfs: `pip3 install fpdf`

Once you have the exported applications and references in CSV format, move them to the
`kesem-selection` directory and call them `apps.csv` and `references.csv`.

## Instructions

Run the following commands from your terminal in the `kesem-selection` directory.

1. `python3 cross_reference.py`
    1. This script cross references each applicant with each letter of reference and vice
    versa. The script gives you some more information, but from the output, you can infer
    which applicants have > 1 reference, which have none, and which references have no matching
    application. For those applicants that have no matching reference, you'll see potential
    matches listed in the output (e.g., Joshua Kravitz's reference might have written a reference
    for "Josh Kravitz" -- the script won't know these are the same, but it will guess that these
    are a match).
    2. **NOTE:** *You should NOT continue past this step until all issues listed by `cross_reference.py`
    are manually resolved (i.e., by removing extra letters of reference and fixing names such that
    each application corresponds with exactly one letter of reference). Keep running `python3 cross_reference.py`
    until nothing is listed!*
2. `python3 assign_applicant_ids.py`
    1. This script assigns IDs to each application. This is for the purpose of anonymizing applications
    and for use in the final deliberation room (if your Rainbow decides to anonymize deliberations, too).
3. `python3 make_pdfs.py`
    1. This script makes PDFs for both applications (which go in the directory `apps/`) and letters of
    reference (which go in the directory `references/`).
