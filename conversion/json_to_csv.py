import csv
import json

def convert_json_to_csv(json_data, output_file):
    # Extract the data from the JSON
    questions_data = json_data["21-025"]
    
    # Prepare the CSV headers
    headers = [
        'Question Number', 
        'Question', 
        'GPT-4 Mini Response',
        'GPT-4 Mini Is Correct',
        'GPT-4 Mini Cost', 
        'Gemini 2.0 Response',
        'Gemini 2.0 Is Correct',
        'Gemini 2.0 Cost', 
        'Llama 3.2 Response',
        'Llama 3.2 Is Correct',
        'Llama 3.2 Cost'
    ]
    
    # Open the output file and write the CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Write each row of data
        for item in questions_data:
            row = [
                item['id'],
                item['question'],
                item['gpt_4o_mini_response'],
                item['gpt_4o_mini_is_correct'],
                item['gpt_4o_mini_cost'],
                item['gemini_2.0_flash_response'],
                item['gemini_2.0_flash_is_correct'],
                item['gemini_2.0_flash_cost'],
                item['llama3.2_3b_response'],
                item['llama3.2_3b_is_correct'],
                item['llama3.2_3b_cost']
            ]
            writer.writerow(row)

# Read the JSON data
file_path = '/Users/scottlabbe/Projects/Evaluate/extraction/data/models/model_comparison_responses.json'
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = json.load(file)

# Convert to CSV
convert_json_to_csv(json_data, 'model_comparison.csv')