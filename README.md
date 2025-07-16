# LLM Audit Report Evaluation Framework

## Overview

This project implements an evaluation framework for comparing the performance of multiple Large Language Models (LLMs) on audit report comprehension tasks. The system tests how accurately different models can extract information from audit reports by asking specific questions and comparing their responses against expected answers.

## Project Goal

The primary objective is to create an automated benchmarking system that:
- Evaluates multiple LLMs' ability to comprehend and extract information from audit reports
- Provides quantitative metrics for model comparison (accuracy, cost, token usage)
- Generates detailed reports for analysis and decision-making
- Helps organizations choose the most cost-effective LLM for audit-related tasks

## Technical Architecture

### Core Components

1. **`main.py`** - Orchestration layer
   - Loads input data (questions and audit reports)
   - Coordinates model responses across all LLMs
   - Generates comprehensive output reports (CSV and JSON)
   - Calculates performance metrics

2. **`models.py`** - Model integration layer
   - Implements API interfaces for three LLM providers:
     - OpenAI (GPT-4o-mini)
     - Google Gemini (Gemini-2.0-flash)
     - Llama (Llama3.2-3b)
   - Handles API authentication and request formatting
   - Standardizes responses across different model APIs

3. **`model_utils.py`** - Utilities and configuration
   - Defines standardized data structures (`ModelResponse`, `ModelType`)
   - Manages model-specific configurations and costs
   - Implements error handling patterns
   - Calculates token-based pricing

4. **`evaluation.py`** - Response evaluation engine
   - Implements text normalization for fair comparison
   - Handles various apostrophe encodings and special characters
   - Performs case-insensitive substring matching
   - Returns boolean correctness indicators

### Key Features

#### Multi-Model Support
- Seamless integration with three major LLM providers
- Extensible architecture for adding new models
- Standardized prompt formatting across all models

#### Comprehensive Metrics
- **Accuracy**: Percentage of correct answers per model
- **Cost Analysis**: Total and per-question costs based on token usage
- **Token Efficiency**: Average tokens consumed per question
- **Detailed Logging**: Full response tracking for qualitative analysis

#### Output Formats
- **CSV Summary**: High-level performance metrics for quick comparison
- **JSON Details**: Complete response data for deep analysis
- **Console Output**: Formatted tables for immediate review

## Technical Specifications

### Dependencies
- Python 3.8+
- `openai` - OpenAI API client
- `google-generativeai` - Google Gemini API client
- `python-dotenv` - Environment variable management
- Standard library: `json`, `csv`, `os`, `logging`

### Environment Variables
```
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LLAMA_API_KEY=your_llama_key
```

### Data Flow
1. **Input**: JSON file with questions/answers + Markdown audit report
2. **Processing**: Each question is sent to all three models with the audit context
3. **Evaluation**: Responses are normalized and compared against expected answers
4. **Output**: Performance metrics and detailed responses in multiple formats

### Cost Optimization
- Configurable cost-per-1K-tokens for each model
- Cost-effectiveness analysis in output reports

## Usage

```python
python main.py
```

The system will:
1. Load questions from the configured JSON file
2. Read the audit report from the Markdown file
3. Query each model for every question
4. Evaluate responses and calculate metrics
5. Generate output files and console summaries

## Output Files

- `model_comparison_responses.json` - Detailed responses and metrics
- `model_comparison_summary.csv` - Summary statistics for each model
- Console output with formatted comparison tables

## Evaluation Methodology

The evaluation uses a substring matching approach where:
- Correct answers are normalized (apostrophe variations, case)
- A response is marked correct if it contains the expected answer
- This allows for natural language variations while ensuring key information is present

## Performance Insights

The framework enables data-driven decisions by revealing:
- Which models provide the most accurate audit comprehension
- Cost-performance trade-offs between different LLMs
- Consistency of responses for critical audit queries

## Future Enhancements

Potential improvements include:
- Support for additional LLM providers
- Different evaluation metrics (LLM as a judge)
- Batch processing for large audit document sets
- Real-time comparison dashboard
- A/B testing capabilities for prompt optimization

---

This project demonstrates proficiency in API integration, data processing, evaluation methodologies, and creating production-ready Python applications for LLM benchmarking tasks.