# src/main.py

import json
import csv
import os
from logging_config import setup_logger
from models import (
    get_openai_model_response,
    get_gemini_model_response,
    get_llama_model_response
)
from evaluation import evaluate_response
from model_utils import ModelResponse

logger = setup_logger(__name__)

# Define model names as constants
OPENAI_MODEL = "gpt-4o-mini"
GEMINI_MODEL = "gemini-2.0-flash"
LLAMA_MODEL = "llama3.2-3b"
MODEL_LIST = [OPENAI_MODEL, GEMINI_MODEL, LLAMA_MODEL]

def load_input_files(json_path, markdown_path):
    """Load and return the question set and audit report."""
    logger.info("Loading question set from JSON...")
    with open(json_path, "r") as f:
        questions = json.load(f)

    logger.info("Loading audit report from Markdown...")
    with open(markdown_path, "r") as f:
        audit_report = f.read()
        
    return questions, audit_report

def process_model_responses(audit_report, qa_list):
    """Process questions through all models and return results."""
    report_records = []
    
    for qa in qa_list:
        q_id = qa["id"]
        q_text = qa["question"]
        expected_answer = qa["answer"]
        
        # Dict to store model responses
        model_responses = {
            OPENAI_MODEL: get_openai_model_response(audit_report, q_text),
            GEMINI_MODEL: get_gemini_model_response(audit_report, q_text),
            LLAMA_MODEL: get_llama_model_response(audit_report, q_text)
        }
        
        record = {
            "id": q_id,
            "question": q_text,
            "expected_answer": expected_answer
        }
        
        # Process each model's response
        for model_name, response in model_responses.items():
            model_prefix = model_name.replace("-", "_")
            is_correct = evaluate_response(expected_answer, response.text)
            
            record.update({
                f"{model_prefix}_response": response.text,
                f"{model_prefix}_is_correct": is_correct,
                f"{model_prefix}_cost": response.cost,
                f"{model_prefix}_tokens": response.total_tokens
            })
            
        report_records.append(record)
        
    return report_records

def write_csv_summary(results, output_csv):
    """Write summary results to CSV file with token information."""
    logger.info(f"Writing CSV to: {output_csv}")
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        for report_name, records in results.items():
            writer.writerow([f"REPORT: {report_name}"])
            if not records:
                writer.writerow(["No data."])
                continue
            
            question_ids = [r["id"] for r in records]
            
            # Updated headers to include token information
            header = ["Model"] + question_ids + ["%Correct", "TotalCost", "TotalTokens", "AvgTokens/Q"]
            writer.writerow(header)

            # Write each model's results
            for model_name in MODEL_LIST:
                row = [model_name]
                model_prefix = model_name.replace("-", "_")
                
                correct_count = 0
                total_cost = 0.0
                total_tokens = 0

                for rec in records:
                    is_correct = rec[f"{model_prefix}_is_correct"]
                    cost = rec[f"{model_prefix}_cost"]
                    tokens = rec[f"{model_prefix}_tokens"]
                    
                    correct_count += (1 if is_correct else 0)
                    total_cost += cost
                    total_tokens += tokens
                    row.append(str(is_correct))

                percent_correct = (correct_count / len(records)) * 100
                avg_tokens = total_tokens / len(records)
                
                row.extend([
                    f"{percent_correct:.1f}%",
                    f"${total_cost:.4f}",
                    str(total_tokens),
                    f"{avg_tokens:.1f}"
                ])
                
                writer.writerow(row)
            
            writer.writerow([])

def print_detailed_results(results):
    """Print detailed comparison of model responses with token information."""
    for report_name, records in results.items():
        print(f"\n=== RESULTS FOR REPORT: {report_name} ===")
        for rec in records:
            print("ID:", rec["id"])
            print("Question:", rec["question"])
            print("Correct Answer:", rec["expected_answer"])
            
            for model_name in MODEL_LIST:
                model_prefix = model_name.replace("-", "_")
                print(f"\n{model_name}:")
                print(f"Response: {rec[f'{model_prefix}_response']}")
                print(f"Is Correct: {rec[f'{model_prefix}_is_correct']}")
                print(f"Tokens Used: {rec[f'{model_prefix}_tokens']}")
                print(f"Cost: ${rec[f'{model_prefix}_cost']:.4f}")
            
            print("-"*50)
        
        print_summary_table(report_name, records)

def print_summary_table(report_name, records):
    """Print formatted summary table with token usage statistics."""
    print(f"\n=== SUMMARY TABLE FOR REPORT: {report_name} ===")
    
    question_ids = [rec["id"] for rec in records]
    
    # Updated header to include token information
    header = ["Model"] + question_ids + ["%Correct", "TotalCost", "TotalTokens", "AvgTokens/Q"]
    table_rows = []
    
    for model_name in MODEL_LIST:
        row = [model_name]
        model_prefix = model_name.replace("-", "_")
        
        correct_count = 0
        total_cost = 0.0
        total_tokens = 0
        
        for rec in records:
            is_correct = rec[f"{model_prefix}_is_correct"]
            cost = rec[f"{model_prefix}_cost"]
            tokens = rec[f"{model_prefix}_tokens"]
            
            correct_count += (1 if is_correct else 0)
            total_cost += cost
            total_tokens += tokens
            row.append(str(is_correct))
        
        percent_correct = (correct_count / len(records)) * 100
        avg_tokens = total_tokens / len(records)
        
        row.extend([
            f"{percent_correct:.1f}%",
            f"${total_cost:.4f}",
            str(total_tokens),
            f"{avg_tokens:.1f}"
        ])
        
        table_rows.append(row)

    # Calculate column widths for nice formatting
    col_widths = []
    for i in range(len(header)):
        width = len(str(header[i]))
        for row in table_rows:
            if i < len(row):
                width = max(width, len(str(row[i])))
        col_widths.append(width)

    # Print formatted table
    header_line = " | ".join(str(header[i]).ljust(col_widths[i]) for i in range(len(header)))
    print(header_line)
    print("-" * len(header_line))
    
    for row in table_rows:
        line = " | ".join(str(row[i]).ljust(col_widths[i]) for i in range(len(row)))
        print(line)

def write_json_results(results, output_path):
    """Write detailed results to JSON file including token information."""
    logger.info(f"Writing responses to {output_path}")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    logger.info(f"Done. Responses saved to: {output_path}")

def main():
    # Define file paths
    json_q_path = 'path/to/data'
    markdown_path = 'path/to/data'
    output_path = os.path.join(os.path.dirname(json_q_path), 'models', 'model_comparison_responses.json')
    output_csv = "path/to/data"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load input files
    questions, audit_report = load_input_files(json_q_path, markdown_path)
    
    # Process all questions and get results
    results = {}
    for report_name, qa_list in questions.items():
        logger.info(f"Processing report: {report_name}")
        results[report_name] = process_model_responses(audit_report, qa_list)

        # Write outputs
    write_csv_summary(results, output_csv)
    write_json_results(results, output_path)
    print_detailed_results(results)


if __name__ == "__main__":
    main()
