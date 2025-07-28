# Adobe India Hackathon - Round 1B: Persona-Driven Document Intelligence

## Overview
This solution analyzes multiple PDF documents to extract and prioritize relevant sections based on a specific persona and job-to-be-done. It produces a structured JSON output with ranked sections and detailed subsection analysis.


## Key Features

1. **Persona-Specific Analysis**: Custom weighting system based on the persona's role and task
2. **Context-Aware Processing**: Understands the job-to-be-done and prioritizes accordingly
3. **Efficient Processing**: Optimized for quick analysis of multiple documents
4. **Structured Output**: Generates output in the exact required JSON format
5. **Constraint Compliance**: Meets all size, runtime, and offline requirements

## Approach
1. **Persona Analysis**:
   - Uses NLP to understand the persona's needs and the specific task
   - Scores text sections based on relevance to the persona and job

2. **Document Processing**:
   - Processes each PDF document
   - Extracts potential sections and subsections
   - Filters and ranks them by relevance

3. **Output Generation**:
   - Creates a structured JSON output with metadata
   - Includes ranked sections and detailed subsection analysis

## Dependencies
- Python 3.9
- PyMuPDF (fitz) - for PDF text extraction
- spaCy - for NLP processing
- No internet access required during execution

## How to Build and Run

### Build the Docker Image
```bash
docker build --platform linux/amd64 -t persona-analyzer:latest .

