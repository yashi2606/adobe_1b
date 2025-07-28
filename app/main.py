import json
import os
import fitz  # PyMuPDF
from datetime import datetime
from persona_analyzer import PersonaAnalyzer
from utils import is_valid_section, clean_text

def process_documents(input_json_path, output_dir):
    # Load input configuration
    with open(input_json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    persona = config['persona']['role']
    job = config['job_to_be_done']['task']
    documents = config['documents']
    
    # Initialize analyzer with persona and job context
    analyzer = PersonaAnalyzer(persona, job)
    
    extracted_sections = []
    subsection_analysis = []
    
    # Process each document
    for doc_info in documents:
        filename = doc_info['filename']
        doc_path = os.path.join('/app/input', filename)
        
        if not os.path.exists(doc_path):
            print(f"Warning: Document {filename} not found in input directory")
            continue
        
        doc = fitz.open(doc_path)
        sections = extract_sections(doc, analyzer)
        
        # Add document title to sections
        for section in sections:
            section['document'] = filename
            extracted_sections.append(section)
        
        # Extract detailed subsections for top sections
        top_sections = [s for s in sections if s['importance_rank'] <= 3]
        for section in top_sections:
            subsections = extract_subsections(doc, section['page_number'], analyzer)
            for sub in subsections:
                sub['document'] = filename
                subsection_analysis.append(sub)
    
    # Sort sections by importance rank
    extracted_sections.sort(key=lambda x: x['importance_rank'])
    
    # Prepare output
    output = {
        "metadata": {
            "input_documents": [d['filename'] for d in documents],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections[:10],  # Limit to top 10
        "subsection_analysis": subsection_analysis[:5]  # Limit to top 5
    }
    
    # Save output
    output_filename = os.path.join(output_dir, 'output.json')
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    
    print(f"Processing complete. Output saved to {output_filename}")

def extract_sections(doc, analyzer):
    sections = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if "lines" not in b:
                continue
                
            # Extract text from block
            text = " ".join([s["text"].strip() for l in b["lines"] for s in l["spans"]])
            text = clean_text(text)
            
            if not is_valid_section(text):
                continue
                
            # Analyze relevance to persona and job
            relevance_score = analyzer.analyze(text)
            
            if relevance_score > 0.3:  # Threshold for inclusion
                sections.append({
                    "section_title": text[:200],  # Limit title length
                    "importance_rank": int((1 - relevance_score) * 10),  # Convert to 1-10 rank
                    "page_number": page_num + 1  # 1-based page numbers
                })
    
    return sections

def extract_subsections(doc, page_num, analyzer):
    subsections = []
    page = doc[page_num - 1]  # Convert to 0-based index
    blocks = page.get_text("dict")["blocks"]
    
    for b in blocks:
        if "lines" not in b:
            continue
            
        text = " ".join([s["text"].strip() for l in b["lines"] for s in l["spans"]])
        text = clean_text(text)
        
        if not text or len(text.split()) < 10:
            continue
            
        relevance_score = analyzer.analyze(text)
        
        if relevance_score > 0.4:  # Higher threshold for subsections
            subsections.append({
                "refined_text": text[:1000],  # Limit length
                "page_number": page_num
            })
    
    return subsections

if __name__ == "__main__":
    input_dir = '/app/input'
    output_dir = '/app/output'
    
    # Find input JSON file
    input_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    if not input_files:
        print("Error: No input JSON file found in input directory")
        exit(1)
        
    input_json_path = os.path.join(input_dir, input_files[0])
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    process_documents(input_json_path, output_dir)
