import json
from datetime import datetime, timedelta

#function to parse date strings (MM/DD/YYYY) with error handling
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%m/%d/%Y")
    except ValueError:
        return None

#loading JSON data from the file
def load_training_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading file: {e}")
        return []

#Generating the completed training summary
def generate_completed_training_summary(data):
    training_summary = {}

    for person in data:
        for record in person['completions']:
            training_name = record['name']
            completion_date = parse_date(record['timestamp'])
            person_name = person['name']

            # Initialize training record if not already present
            if training_name not in training_summary:
                training_summary[training_name] = {}

            # Track the latest completion only
            if person_name not in training_summary[training_name] or \
               (completion_date and completion_date > training_summary[training_name][person_name]):
                training_summary[training_name][person_name] = completion_date

    # Convert to counts of unique participants
    return {training: len(participants) for training, participants in training_summary.items()}

#Generating the fiscal year report for specific trainings
def generate_fiscal_year_training_report(data, fiscal_year, training_list):
    fiscal_year_start = datetime(fiscal_year - 1, 7, 1)
    fiscal_year_end = datetime(fiscal_year, 6, 30)

    report = {training: set() for training in training_list}

    for person in data:
        for record in person['completions']:
            training_name = record['name']
            completion_date = parse_date(record['timestamp'])

            if training_name in training_list and completion_date:
                if fiscal_year_start <= completion_date <= fiscal_year_end:
                    report[training_name].add(person['name'])

    # Convert sets to lists for JSON serialization
    return {training: list(participants) for training, participants in report.items()}

#Generating a report for expired or expiring soon trainings
def generate_expiring_training_report(data, reference_date_str):
    reference_date = parse_date(reference_date_str)
    if not reference_date:
        print("Invalid reference date provided.")
        return {}

    soon_threshold = reference_date + timedelta(days=30)
    report = {}

    for person in data:
        expiring_trainings = []
        for record in person['completions']:
            expiration_date_str = record.get('expires')
            expiration_date = parse_date(expiration_date_str)

            if expiration_date:
                if expiration_date < reference_date:
                    expiring_trainings.append({"training": record['name'], "status": "Expired"})
                elif expiration_date <= soon_threshold:
                    expiring_trainings.append({"training": record['name'], "status": "Expiring Soon"})

        if expiring_trainings:
            report[person['name']] = expiring_trainings

    return report

#save the output to a JSON file
def save_to_json(output_data, output_file_name):
    try:
        with open(output_file_name, 'w') as file:
            json.dump(output_data, file, indent=4)
    except IOError as e:
        print(f"Error saving file: {e}")

# Main logic to run the program
if __name__ == "__main__":
    # Load the training data
    data = load_training_data('training.txt')
    
    # 1. Generate the completed training summary
    completed_training_summary = generate_completed_training_summary(data)
    save_to_json(completed_training_summary, 'completed_training_summary.json')
    
    # 2. Generate the report for the fiscal year 2024
    training_list = ["Electrical Safety for Labs", "X-Ray Safety", "Laboratory Safety Training"]
    fiscal_year_training_report = generate_fiscal_year_training_report(data, 2024, training_list)
    save_to_json(fiscal_year_training_report, 'fiscal_year_training_report.json')
    
    # 3. Generate the report for trainings expiring by Oct 1, 2023
    expiring_training_report = generate_expiring_training_report(data, '10/01/2023')
    save_to_json(expiring_training_report, 'expiring_training_report.json')
