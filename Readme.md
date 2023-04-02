# Filename Randomizer
Simple command line program for randomizing filenames, the order of files or for picking random files.

Also supports reversal of the filename adjustments.

## Command

`python file_randomizer.py TARGET_DIR [-n -name] [-o -order] [-u undo] [-p -pick N] [-r -recurse] [-re regex EXPRESSION] [-v -verbose LEVEL] [-nc -nocheck]`

**TARGET_DIR** Target directory for the file search

**name** Randomize filenames

**order** Randomize order of files

**undo** Undo randomization

**pick** Pick **N** random files

**recurse** Apply action to all subfolders under **TARGET_DIR**

**regex** Filter all files via a regex pattern (filenames must match)

**verbose** Sets the verbosity **LEVEL** **1**=verbose **0**=basic

**nockeck** Skips the sanity check

## Disclaimer
This program is free software. It comes without any warranty.

Misuse, whether intention or accidental, can cause corruption of system files or loss of data.

By using this software you accept full responsibility for the outcome of its use.

## Example Usage

Randomize filenames.

`python file_randomizer.py .\stuff\cat-pics -name`

Randomize order of files.

`python file_randomizer.py .\music\workout-playlist -order`

Undo randomization.

`python file_randomizer.py .\music\workout-playlist -undo`

Pick 2 random png files.

`python file_randomizer.py .\pictures\mum -pick 2 -regex ".+\.png"`

Randomize filenames and order of .csv files recursively.

`python file_randomizer.py .\lotsofstuff -order -name -recurse -regex ".+\.csv"`

## Building an Executable (Windows)

*run-app.ps1* Can generate a single-file executable version of this program.

`./run-app.ps1 BuildExe`

The generated executable can be found in `/dist`

This requires **pyinstaller** `pip install pyinstaller`

## Tests and Linting

Run unit tests `./run-app.ps1 UnitTest`

Run functional tests `./run-app.ps1 FunctionalTest`

Run Pylint `./run-app.ps1 Lint`

Clean junk `./run-app.ps1 Clean`

## .rmanidest Files
When randomizing filenames the changes will be tracked in a *.rmanifest* file.

Do not modify or delete these files. They are necessary for `-undo`-ing any filename changes.

## Future Improvements
- Successive renamings via `-order` should remove the previous prefix so the filename does not grow indefinitely.
- Better sanity check
