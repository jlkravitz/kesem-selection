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
4. Install fpdf, a python library for building pdfs: `pip install fpdf`
5. Separately, install [Table Tool](https://itunes.apple.com/us/app/table-tool/id1122008420) for Mac.
This will make it easier to view and edit CSV files, which you'll have to do later.
6. Separately (again), export the applications and references from Wufoo into CSV format.

Move them to the `kesem-selection` directory and call them `apps.csv` and `references.csv` (you can do
this in Finder if you have a Mac).

**NOTE:** Only export once you know you have *all* applications and references.
These scripts don't play nicely with "new" apps and references. This means that
you can't start reading apps until *all* apps are in, so don't give long
deadline extensions!

Nice! Your computer is ready to rumble...

(For computer nerds: This code is python2-compatible and *almost* python3 compatible.
I originally wrote this for python3 since it's easier to deal with unicode, but decided
to change to python2 to avoid forcing non-computer-nerds to install python3, which isn't
installed on computers by default.)

## Instructions

Run the following commands from your terminal in the `kesem-selection` directory.

1. `python cross_reference.py`
    1. This script cross references each applicant with each letter of reference and vice
    versa. It will list any problems (e.g., applicants that don't seem to have a letter of reference).
    2. You will have to fix these problems before running any other scripts (the one exception: applicants
    with letters that are *truly* missing).
    3. To have the scripts "ignore" an application or reference, change the "Completion Status" column to a 0.
    *Do this carefully, as you are effectively removing an application or reference from our application pool.*
    4. Each time you make a change to `apps.csv` or `references.csv`, run `python cross_reference.py` again.
    Make sure you see the expected result.
    4. **LISTEN UP!:** You should *NOT* continue past this step until all issues listed by `cross_reference.py`
    are manually resolved (i.e., by removing extra letters of reference and fixing names such that
    each application corresponds with exactly one letter of reference). Keep running `python cross_reference.py`
    until nothing (except for references that truly don't have a matching applicant) is listed!
    5. **LISTEN UP!:** Once you have completed this step, *immediately* upload `apps.csv` and `references.csv`
    to Google Drive. You do not want to lose these files!
2. Optional: `python app_stats.py`
    1. This will list the applicant breakdown in each year and the gender breakdown within each year.
    2. You can run this whenever you want – it only analyzes the data and changes nothing!
3. `python assign_applicant_ids.py`
    1. This script assigns IDs to each application. This is for the purpose of anonymizing applications
    and for use in the final deliberation room (if your Rainbow decides to anonymize deliberations, too).
    2. **LISTEN UP!:** Once you have completed this step, **immediately upload `applicants_ids.csv` to Google
    Drive. You do not want to lose this file! (If you do, you won't know which ID corresponds with which
    applicant, which is very sad :()
    
From here, choose one of the options below (you'll probably do both eventually) ...

### Scored Application Reading

Follow these instructions for setting up the process of having readers score each application.

4. `python make_conflicts_of_interest_spreadsheet.csv`
    1. This script creates a spreadsheet which allows readers to mark applicants they know. Any marked applicants
    won't be assigned to that reader.
    2. You'll have to know the names of every reader to run this script.
    3. Once you've run this, upload `conflicts_of_interest.csv` to Google Drive and open it in Google Sheets. Have
    readers mark people they know with an "x" (any non-empty cell will count).
    4. Once completed by each reader, download the file as a CSV and put it back into the `kesem/` directory.
5. `python make_reader_folders.py`
    1. For each reader, this script assigns applicants (keeping in mind the conflicts spreadsheet above),
    creates a reader-specific score sheet, and creates a reader-specific application packet with applications
    and letters of reference for each applicant.
    2. Make sure to quickly inspect `app_read_assignments.csv` before letting the script continue
    (run the script to find out what I mean here – it won't do anything dangerous, so don't worry).
    2. Once the script finishes running (be patient! this can take a few minutes), upload the
    `Application Reading/` folder to Google Drive. Tell readers to double click on their CSV score
    sheets and click "Open in Google Sheets".
    3. Wahoo! Readers can now read apps. 
6. At this point, you should upload `applicant_ids.csv` to the `Application Reading/` folder on
Google Drive to make sure you don't accidentally delete that file (see above for why!). Rename
it to `Applicant IDs (SENSITIVE: DO NOT OPEN).csv` so that people get the message. Anonymity goes
out the window if readers or Rainbow members look at this file.

### Pre-Interview Application Reading

Follow these instructions for making PDFs of apps and references for ULs/Rainbow members to read before interviews
to learn about the applicant their interviewing.

4. `python make_individual_pdfs.py`
    1. This script makes PDFs for both applications (which go in the directory `apps/`) and letters of
    reference (which go in the directory `references/`).
    2. Upload the `apps/` and `references/` directories to Google Drive (or only `apps/` if that's all
    you want interviewers to read).
    3. Note that these applications are *not* anonymized so that interviewers know the names of the applicant
    they are interviewing.
