from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.utils import split_into_sentences, clean_text
from app.core_dsa import kmp_search, rabin_karp_search

app = FastAPI(
    title="Core DSA Plagiarism Detection System API",
    description="Engine evaluating substring patterns via KMP and Rabin-Karp techniques."
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlagiarismRequest(BaseModel):
    source_doc: str
    student_doc: str
    algorithm: str = "kmp"  # Allowed options: 'kmp' or 'rabin_karp'

@app.post("/api/analyze")
async def analyze_documents(payload: PlagiarismRequest):
    src_text = payload.source_doc
    stud_text = payload.student_doc
    algo = payload.algorithm.lower()
    
    if not src_text.strip() or not stud_text.strip():
        raise HTTPException(status_code=400, detail="Documents cannot be empty strings.")

    # Step 1: Preprocess and clean the text
    cleaned_src = clean_text(src_text)
    student_sentences = split_into_sentences(stud_text)
    
    if not student_sentences:
        return {
            "plagiarism_percentage": 0.0,
            "matched_sentences": [],
            "total_sentences_checked": 0
        }

    matched_sentences_list = []
    copied_character_count = 0
    unique_matched_characters = set() # Tracks overlapping indices to handle repetitive text accurately

    # Step 2: Run the selected string matching algorithm sentence by sentence
    for sentence in student_sentences:
        if algo == "rabin_karp":
            match_indices = rabin_karp_search(cleaned_src, sentence)
        else:
            match_indices = kmp_search(cleaned_src, sentence)

        if match_indices:
            matched_sentences_list.append({
                "text": sentence,
                "algorithm_used": algo,
                "match_found": True
            })
            # Reconstruct original student indices or estimate match weight using character spans
            copied_character_count += len(sentence)
        else:
            matched_sentences_list.append({
                "text": sentence,
                "algorithm_used": algo,
                "match_found": False
            })

    # Step 3: Compute final plagiarism metrics
    cleaned_student_total = clean_text(stud_text)
    total_len = len(cleaned_student_total)
    
    # Calculate percentage based on total characters identified as copied
    plagiarism_percentage = (min(copied_character_count, total_len) / total_len * 100) if total_len > 0 else 0.0

    return {
        "plagiarism_percentage": round(plagiarism_percentage, 2),
        "matched_sentences": matched_sentences_list,
        "total_sentences_checked": len(student_sentences)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)