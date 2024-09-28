Solution by Mohammed Anas Hussaini

Run the script using the command:

python main.py
This will generate three JSON output files: completed_training_summary.json, 
fiscal_year_training_report.json, and expiring_training_report.json.

Time Complexity:
Training Summary Generation: O(n), where n is the number of completion records.
Fiscal Year Report Generation: O(n), where n is the number of relevant training records in the specified year.
Expired/Expiring Trainings Report: O(n), where n is the total number of training records checked for expiration.
