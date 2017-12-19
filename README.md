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
`kesem-selection` directory and call them `apps.csv` and `references.csv` (you can do
this in Finder if you have a Mac).

## Instructions

Run the following commands from your terminal in the `kesem-selection` directory.

1. `python3 cross_reference.py`
    1. This script cross references each applicant with each letter of reference and vice
    versa. It will list any problems (e.g., applicants that don't seem to have a letter of reference).
    2. You will have to fix these problems before running any other scripts (the one exception: applicants
    with letters that are *truly* missing).
    3. To have the scripts "ignore" an application or reference, change the "Completion Status" column to a 0.
    *Do this carefully, as you are effectively removing an application or reference from our application pool.*
    4. Each time you make a change to `apps.csv` or `references.csv`, run `python3 cross_reference.py` again.
    Make sure you see the expected result.
    3. **NOTE:** *You should NOT continue past this step until all issues listed by `cross_reference.py`
    are manually resolved (i.e., by removing extra letters of reference and fixing names such that
    each application corresponds with exactly one letter of reference). Keep running `python3 cross_reference.py`
    until nothing is listed!*
2. `python3 assign_applicant_ids.py`
    1. This script assigns IDs to each application. This is for the purpose of anonymizing applications
    and for use in the final deliberation room (if your Rainbow decides to anonymize deliberations, too).
    2. **IMPORTANT:** Once you start reading apps (see below), you *cannot* lose this file. Otherwise, you won't
    know which application was written by which applicant. In other words, you're screwed. (To be clear, you
    probably could get out of this sticky situation by looking at the letters of reference which often reference
    applicant's first or last names...but it wouldn't be fun to do.)
    
From here, choose one of the options below (you'll probably do both eventually) ...

### Scored Application Reading

Follow these instructions for setting up the process of having readers score each application.

3. `python3 make_conflicts_of_interest_spreadsheet.csv`
    1. This script creates a spreadsheet for marking applicants that each reader knows. This will prevent that
    reader from being assigned that applicant.
    2. You will have to know who is reading applications to run this script (you will have to enter their names).
    3. Once you've run this, upload `conflicts_of_interest.csv` to Google Drive and open it in Google Sheets. Have
    readers mark people they know with an "x".
    4. Once every reader has completed this, download the file as a CSV and put it back into the `kesem/` directory.
4. `python3 make_reader_folders.py`
    1. This script will assign applicants to each reader and create a folder with a scoresheet and application packet for
    them. Make sure to quickly inspect `app_read_assignments.csv` before letting the script continue (run the script to find     out what I mean here – it won't do anything dangerous, so don't worry).
    2. Upload the `Application Reading/` folder to Google Drive. Tell readers to double click on their CSV score sheets and     click "Open in Google Sheets".
    3. Wahoo! Readers are ready to read applications.
    
At this point, you might want to also upload `applicant_ids.csv` to the `Application Reading/` folder on Google Drive to make sure you don't accidentally delete that file (see above for why!).

### Pre-Interview Application Reading

Follow these instructions for making PDFs of apps and references for ULs/Rainbow members to read before interviews
to learn about the applicant their interviewing.

3. `python3 make_individual_pdfs.py`
    1. This script makes PDFs for both applications (which go in the directory `apps/`) and letters of
    reference (which go in the directory `references/`).
    2. Upload the `apps/` and `references/` directories to Google Drive (or only `apps/` if that's all
    you want interviewers to read).
    3. Note that these applications are *not* anonymized so that interviewers know the names of the applicant
    they are interviewing.
