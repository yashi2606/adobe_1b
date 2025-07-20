import fitz  # PyMuPDF
import os
import json

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def extract_headings(pdf_path):
    doc = fitz.open(pdf_path)
    headings = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = ""
                sizes = []
                for span in line["spans"]:
                    text += span["text"]
                    sizes.append(span["size"])
                text = text.strip()
                if not text:
                    continue

                avg_font_size = sum(sizes) / len(sizes)

                # Classify heading level based on font size
                if avg_font_size > 15:
                    level = "H1"
                elif avg_font_size > 13:
                    level = "H2"
                elif avg_font_size > 11:
                    level = "H3"
                elif avg_font_size > 10:
                    level = "H4"
                else:
                    continue  # Skip non-headings

                headings.append({
                    "level": level,
                    "text": text,
                    "page": page_num + 1
                })

    return headings

def process_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".pdf")]

    for file in files:
        pdf_path = os.path.join(INPUT_DIR, file)
        headings = extract_headings(pdf_path)
        output = {
            "title": os.path.splitext(file)[0],
            "outline": headings
        }

        json_path = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=4, ensure_ascii=False)
        print(f"✅ Processed: {file}")

if __name__ == "__main__":
    process_pdfs()
