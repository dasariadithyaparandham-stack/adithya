"""Optional semantic matching constrained to the seeded skill taxonomy."""

import re
from functools import lru_cache


def _tokens(value: str) -> set[str]:
    return set(re.findall(r'[a-z0-9]+', value.casefold()))


@lru_cache(maxsize=1)
def _embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer('all-MiniLM-L6-v2')
    except ImportError:
        return None


def similarity(left: str, right: str) -> float:
    model = _embedding_model()
    if model is not None:
        vectors = model.encode([left, right], normalize_embeddings=True)
        return max(0.0, float(vectors[0] @ vectors[1]))
    left_tokens = _tokens(left)
    right_tokens = _tokens(right)
    if not left_tokens or not right_tokens:
        return 0.0
    return len(left_tokens & right_tokens) / len(left_tokens | right_tokens)


def semantic_skill_matches(detected: list[str], required: list[str], threshold: float = 0.8):
    matches = []
    scores = []
    for required_skill in required:
        best = max((similarity(candidate, required_skill) for candidate in detected), default=0.0)
        scores.append(best)
        if best >= threshold:
            matches.append(required_skill)
    return matches, round(sum(scores) / len(scores) * 100, 2) if scores else 0.0