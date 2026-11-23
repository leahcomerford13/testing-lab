# Week 11 testing report

Project: Campus Status
Tester(s): Leah Comerford
Date: 23 November 2026
Python version: 3.14.8
Git commit or branch: 

## Scope and environment

Testing local Python file operations with pytest in a temporary test directory.
No production files or cloud resources are changed.

## Test plan - Configuration backup

Requirements: B1-B4 in the Week 11 tutorial.
Approach: representative valid and invalid files; expected error for missing source.

| ID | Test data and starting state | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| B-T1 | `monitoring.json` with `{"port": 443}`; no destination | Copy contents unchanged; return its destination path | Passed. The contents and the returned path were correct | Pass |
| B-T2 | `service.json` and `notes.txt`; no destination | Copy only `service.json`; return only that path | Passed. Only `service.json` was copied | Pass |
| B-T3 | Source path does not exist | Raise `FileNotFoundError`; do not create destination | Passed. `FileNotFoundError` was raised and no destination was made | Pass |

## Execution and evidence - Backup

Manual backup observation: I ran `python scripts/run_backup.py sample-data/week11-backup-input output/week11-backup`. It copied `monitoring.json` and `service.json`. `notes.txt` was not copied.
Command used: `python -m pytest tests/test_backup.py -v`
Summary: 3 passed in 0.11s
Relevant failure messages: None
Elapsed time observation: The tests took between 0.08s and 0.11s. I only noted this and did not treat it as a target.
Missing source check: I ran the script with a source that does not exist. It showed the error "Source directory not found", which was expected.

## Deployment tests

Requirements: D1-D6 in the Week 11 lab.
Method: equivalence partitions for file types and source states;
check actual files, contents, returned paths and errors.

| ID | Test data and starting state | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| D-T1 | Source contains `service.json`; destination absent | `service.json` is copied with contents unchanged; the returned list is exactly that one path | Passed. The file was copied and the path was correct | Pass |
| D-T2 | Source contains `service.json` and `notes.txt` | Only `service.json` is in the destination; the returned list has only that path | First run FAILED because the destination had `['notes.txt', 'service.json']`. After the fix it PASSED | Pass (after fix) |
| D-T3 | Source exists but is empty | Destination is created and empty; returns `[]` | Passed. The destination was created, it was empty and `[]` was returned | Pass |
| D-T4 | Source directory does not exist | `FileNotFoundError` is raised; destination is not created | Passed. The error was raised and no destination was made | Pass |

### Defect investigation

Requirement checked: D1 and D3. Only `.json` files directly inside the source folder should be copied.

Observed failure and evidence: On the original `deploy_config.py`, `test_deploy_excludes_other_files` failed with `AssertionError: assert ['notes.txt', 'service.json'] == ['service.json']`. This shows that `notes.txt` was copied when it should not have been. I kept a screenshot of this.

Cause found in the code: The condition in the loop was `if path.is_file():`. It only checked that the entry was a file. It did not check the file extension, so every file was copied.

Correction made: I changed the line to `if path.is_file() and path.suffix == ".json":`.

Result after correction: `test_deploy_excludes_other_files` passed. All 4 deployment tests passed.

### Final verification

Command and result for deployment tests: `python -m pytest tests/test_deploy_config.py -v` -> 4 passed in 0.08s

Command and result for the full test suite: `python -m pytest -q` -> 24 passed in 0.09s

Anything not tested: I did not test a real server or cloud deployment, a large number of files or  uppercase `.JSON` files.
