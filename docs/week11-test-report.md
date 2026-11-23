# Week 11 testing report

Project: Campus Status
Tester(s): Leah Comerford (A00041045)
Date: 23 November 2026
Python version: 3.14.8
Git commit or branch: week11-testing

## Scope and environment

Testing local Python file operations with pytest in a temporary test directory.
No production files or cloud resources are changed.

## Test plan - Configuration backup

Requirements: B1-B4 in the Week 11 tutorial.
Approach: representative valid and invalid files; expected error for missing source.

| ID | Test data and starting state | Expected result | Actual result | Status |
| --- | --- | --- | --- | --- |
| B-T1 | `monitoring.json` with `{"port": 443}`; no destination | Copy contents unchanged; return its destination path | Passed. The contents and the returned path were correct | Pass |
<img width="966" height="243" alt="image" src="https://github.com/user-attachments/assets/824912ed-5e2d-41a1-82c1-da938a099475" />

| B-T2 | `service.json` and `notes.txt`; no destination | Copy only `service.json`; return only that path | Passed. Only `service.json` was copied | Pass |
<img width="958" height="205" alt="image" src="https://github.com/user-attachments/assets/1c82678e-08ef-42ff-80aa-c12e990c3b81" />


| B-T3 | Source path does not exist | Raise `FileNotFoundError`; do not create destination | Passed. `FileNotFoundError` was raised and no destination was made | Pass |
<img width="962" height="236" alt="image" src="https://github.com/user-attachments/assets/a28295f0-8773-4d15-a53c-0592b1cc04b5" />



## Execution and evidence - Backup

Manual backup observation: I ran `python scripts/run_backup.py sample-data/week11-backup-input output/week11-backup`. It copied `monitoring.json` and `service.json`. `notes.txt` was not copied.
Command used: `python -m pytest tests/test_backup.py -v`
Summary: 3 passed in 0.11s
<img width="969" height="252" alt="image" src="https://github.com/user-attachments/assets/b0ae6dde-177f-4fc6-a883-f88856917bcc" />

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
<img width="959" height="235" alt="image" src="https://github.com/user-attachments/assets/bda1f46f-643b-4f27-9c76-14716e20912f" />


| D-T2 | Source contains `service.json` and `notes.txt` | Only `service.json` is in the destination; the returned list has only that path | First run FAILED because the destination had `['notes.txt', 'service.json']`. After the fix it PASSED | Pass (after fix) |
<img width="982" height="306" alt="image" src="https://github.com/user-attachments/assets/2f14b2ae-0df6-496b-8b02-dc8cc178344b" />

| D-T3 | Source exists but is empty | Destination is created and empty; returns `[]` | Passed. The destination was created, it was empty and `[]` was returned | Pass |
<img width="959" height="298" alt="image" src="https://github.com/user-attachments/assets/c9d20051-0a0c-4031-ac21-472ec3d5db6b" />


| D-T4 | Source directory does not exist | `FileNotFoundError` is raised; destination is not created | Passed. The error was raised and no destination was made | Pass |
<img width="974" height="281" alt="image" src="https://github.com/user-attachments/assets/e0ce6aa7-acfe-4ed0-badd-a98db4cc91b6" />


### Defect investigation

Requirement checked: D1 and D3. Only `.json` files directly inside the source folder should be copied.

Observed failure and evidence: On the original `deploy_config.py`, `test_deploy_excludes_other_files` failed with `AssertionError: assert ['notes.txt', 'service.json'] == ['service.json']`. This shows that `notes.txt` was copied when it should not have been. I kept a screenshot of this.

Cause found in the code: The condition in the loop was `if path.is_file():`. It only checked that the entry was a file. It did not check the file extension, so every file was copied.

Correction made: I changed the line to `if path.is_file() and path.suffix == ".json":`.

Result after correction: `test_deploy_excludes_other_files` passed. All 4 deployment tests passed.
<img width="953" height="274" alt="image" src="https://github.com/user-attachments/assets/70ef97ca-96a5-45f8-aa95-820e15c6a034" />


### Final verification

Command and result for deployment tests: `python -m pytest tests/test_deploy_config.py -v` -> 4 passed in 0.08s
<img width="952" height="358" alt="image" src="https://github.com/user-attachments/assets/8d7958ab-6351-4082-b518-01967f218fba" />



Command and result for the full test suite: `python -m pytest -q` -> 24 passed in 0.09s
<img width="869" height="67" alt="image" src="https://github.com/user-attachments/assets/a917ceac-0351-47cb-8899-8d39307ff98f" />


Anything not tested: I did not test a real server or cloud deployment, a large number of files or  uppercase `.JSON` files.



