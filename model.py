from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface import HuggingFacePipeline
import pdfplumber
from docx import Document

# Load lightweight model
model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Improved generation settings
pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    do_sample=True,           # Fixes temperature warning
    temperature=0.3,
    top_k=50,
    top_p=0.95,
    num_return_sequences=1
)

llm = HuggingFacePipeline(pipeline=pipe)

# Store uploaded document content globally
document_content = ""

def extract_text_from_file(file_path):
    """
    Extracts text from a file and stores it in global variable.
    Supports PDF, DOCX, and TXT files.
    """
    global document_content

    print(f"📄 Reading file: {file_path}")  # Debug log

    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    print(f"📖 Page {page_num + 1} text length: {len(page_text)}")  # Debug
                    text += page_text + "\n"
            document_content = text.strip()
            print("📄 PDF extraction complete.")  # Debug
            return document_content

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        document_content = text.strip()
        print("📄 DOCX extraction complete.")
        return document_content

    elif file_path.endswith(".txt"):
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        document_content = text.strip()
        print("📄 TXT extraction complete.")
        return document_content

    else:
        raise ValueError("Unsupported file type")
