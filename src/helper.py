from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings
import re

def load_data(data):
    loader= DirectoryLoader(data,
                            glob="*.pdf",
                            loader_cls=PyPDFLoader)

    documents=loader.load()

    return documents

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=50
    )
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks



def get_ollama_embeddings():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text:v1.5",
    )
    return embeddings


keyword_to_sections = {
    # Robbery & related offenses
    "robbery": [392, 393, 394, 395, 397],
    "armed robbery": [394, 395, 397],
    "dacoity": [391, 395, 396, 397],
    
    # Theft & property crimes
    "theft": [378, 379, 380],
    "burglary": [378, 380, 457, 458],
    
    # Murder / attempt
    "murder": [302, 303, 304],
    "attempted murder": [307],
    "homicide": [302, 304],
    
    # Assault / harassment
    "assault": [351, 352, 354],
    "criminal intimidation": [503, 506],
    "kidnapping": [359, 360, 361, 362, 363],
    
    # Fraud / forgery
    "forgery": [463, 464, 465, 468, 471],
    "cheating": [415, 416, 420, 421, 423],
    
    # Sexual offenses
    "rape": [375, 376],
    "sexual assault": [354],
    
    # Property damage
    "arson": [435, 436],
    "criminal mischief": [427, 428],
    
    # Others
    "extortion": [383, 384, 385],
    "criminal breach of trust": [405, 406, 407],
}

# Synonyms mapping (optional for better matching)
synonyms = {
    "thief": "theft",
    "robbers": "robbery",
    "kidnap": "kidnapping",
    "kill": "murder",
    "fraud": "cheating",
    "fire": "arson",
    "assaulted": "assault",
}

def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)  # remove punctuation
    return text

def filter_response(query, response_text):
    query_norm = normalize_text(query)
    matched_sections = set()

    # Replace synonyms
    for syn, keyword in synonyms.items():
        query_norm = query_norm.replace(syn, keyword)

    # Search for keywords
    for keyword, sections in keyword_to_sections.items():
        if keyword in query_norm:
            matched_sections.update(sections)

    # If response already JSON, inject suggestions
    try:
        import json
        parsed = json.loads(response_text)
        if matched_sections:
            existing_numbers = {s["number"] for s in parsed.get("sections", [])}
            for sec in matched_sections:
                if sec not in existing_numbers:
                    parsed["sections"].append({"number": sec, "description": "Suggested"})
        return json.dumps(parsed, indent=2)
    except:
        # fallback to text
        if matched_sections:
            response_text += f"\nSuggested relevant sections: {sorted(list(matched_sections))}"
        return response_text
