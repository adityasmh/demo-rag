import os

HERE = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE = os.path.join(HERE, "knowledge")


def load_paragraphs(company):
    """Read every .md file of a company and split it at the '## ' headings."""
    paragraphs = []
    folder = os.path.join(KNOWLEDGE, company)
    for file_name in sorted(os.listdir(folder)):
        if not file_name.endswith(".md"):
            continue
        heading = file_name
        lines = []
        with open(os.path.join(folder, file_name), encoding="utf-8") as f:
            for line in f.read().splitlines():
                if line.startswith("## "):
                    if lines:
                        paragraphs.append({"heading": heading, "text": " ".join(lines)})
                    heading = line[3:].strip()
                    lines = []
                elif line.strip() and not line.startswith("# "):
                    lines.append(line.strip())
        if lines:
            paragraphs.append({"heading": heading, "text": " ".join(lines)})
    return paragraphs


SKIP_WORDS = {"a", "an", "the", "is", "are", "to", "of", "and", "or", "in", "on", "for",
              "it", "my", "i", "me", "do", "does", "how", "what", "much", "can", "will",
              "at", "be", "with", "if", "by", "this", "that", "you", "your"}


def clean_words(text):
    words = []
    for word in text.lower().replace(",", " ").replace(".", " ").replace("?", " ").split():
        if word in SKIP_WORDS:
            continue
        if word.endswith("s") and len(word) > 3:
            word = word[:-1]
        words.append(word)
    return words


def search(paragraphs, question, top_k=2):
    question_words = set(clean_words(question))
    results = []
    for p in paragraphs:
        paragraph_words = set(clean_words(p["heading"] + " " + p["text"]))
        score = len(question_words & paragraph_words)
        if score > 0:
            results.append((score, p))
    results.sort(key=lambda pair: pair[0], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    for score, p in search(load_paragraphs("groww"), "what is the brokerage for stocks"):
        print(score, p["heading"])