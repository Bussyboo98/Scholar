from transformers import DebertaForSequenceClassification, DebertaV2Tokenizer
import language_tool_python
import torch
from torch.nn.functional import sigmoid
from nltk.corpus import stopwords
from collections import Counter
import nltk

# NLTK setup
nltk.download('stopwords')

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load tokenizer and model
tokenizer = DebertaV2Tokenizer.from_pretrained("microsoft/deberta-v3-large")
model = DebertaForSequenceClassification.from_pretrained(
    "microsoft/deberta-v3-large", num_labels=1, ignore_mismatched_sizes=True
).to(device)

# Load grammar checking tool
tool = language_tool_python.LanguageTool("en-US")

def evaluate_essay(essay_text):
    if not essay_text.strip():
        return {"error": "The essay text cannot be empty."}

    # Split the essay into chunks
    chunks = chunk_essay(essay_text)
    
    # Score each chunk and calculate the average predicted score
    predicted_scores = []
    for chunk in chunks:
        encoding = tokenizer(
            chunk,
            max_length=512,
            truncation=True,
            padding="max_length",
            return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            outputs = model(**encoding)
            predicted_scores.append(sigmoid(outputs.logits).squeeze().item() * 10)

    predicted_score = sum(predicted_scores) / len(predicted_scores)  # Average score

    # Word count-based score
    word_count = len(essay_text.split())
    word_count_score = min(10, max(0, (word_count / 300) * 10))

    # Lexical diversity
    words = [word.lower() for word in essay_text.split() if word.isalpha()]
    unique_words = len(set(words))
    lexical_diversity = unique_words / word_count if word_count > 0 else 0
    lexical_score = min(10, lexical_diversity * 20)

    # Idea richness
    keywords = [word for word in words if word not in stopwords.words("english")]
    key_points = len(Counter(keywords).most_common(50))
    idea_richness_score = min(10, key_points / 5)

    # Combined content score
    content_score = (
        0.5 * word_count_score +
        0.3 * lexical_score +
        0.2 * idea_richness_score
    )

    # Grammar score
    matches = tool.check(essay_text)
    grammar_issues = len(matches)
    grammar_score = max(0, 10 - grammar_issues)

    # Structure score
    paragraphs = essay_text.split("\n")
    structure_score = min(10, len(paragraphs))

    # Final score
    final_score = round((predicted_score + content_score + grammar_score + structure_score) / 4, 2)

    # Progress widths
    predicted_score_width = predicted_score * 10
    content_score_width = content_score * 10
    grammar_score_width = grammar_score * 10
    structure_score_width = structure_score * 10

    # Feedback
    feedback = generate_feedback(content_score, grammar_score, structure_score, grammar_issues)

    return {
        "predicted_score": round(predicted_score, 2),
        "content_score": round(content_score, 2),
        "grammar_score": round(grammar_score, 2),
        "grammar_progress_width": grammar_score_width,
        "content_progress_width": content_score_width,
        "predicted_progress_width": predicted_score_width,
        "structure_progress_width": structure_score_width,
        "structure_score": round(structure_score, 2),
        "final_score": final_score,
        "grammar_issues": grammar_issues,
        "feedback": feedback,
    }


def chunk_essay(essay_text, chunk_size=256):
    words = essay_text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


def generate_feedback(content_score, grammar_score, structure_score, grammar_issues):
    feedback = ""
    if content_score > 6.5:
        feedback += "Excellent content with strong ideas and clarity.\n"
    elif content_score > 4.0:
        feedback += "Good content but could benefit from deeper analysis or more examples.\n"
    else:
        feedback += "Content is weak. Consider adding more evidence or elaboration.\n"

    feedback += f"Grammar issues detected: {grammar_issues}. "
    if grammar_score > 8:
        feedback += "Grammar is strong.\n"
    elif grammar_score > 5:
        feedback += "Consider revising minor grammar mistakes.\n"
    else:
        feedback += "Significant grammar issues affect readability. Proofreading is recommended.\n"

    if structure_score == 10:
        feedback += "Excellent structure with well-organized paragraphs.\n"
    elif structure_score >= 7:
        feedback += "Structure is good, but paragraphs are either too long or too short.\n"
    else:
        feedback += "Poor structure. Ensure each paragraph has a clear topic and is not too short or too long.\n"

    return feedback
