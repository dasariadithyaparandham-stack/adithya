import re

from app.data.skill_catalog import SKILL_CATALOG


def normalize_skill_text(value: str) -> str:
    value = value.lower().strip()
    value = value.replace('-', ' ')
    value = re.sub(r'[^a-z0-9\s]', ' ', value)
    value = re.sub(r'\s+', ' ', value)
    return value


def alias_matches(text: str, alias: str) -> bool:
    alias_norm = normalize_skill_text(alias)
    if not alias_norm:
        return False

    text_norm = normalize_skill_text(text)
    alias_pattern = re.escape(alias_norm).replace(r'\ ', r'\s+')
    pattern = rf'(?<![a-z0-9]){alias_pattern}(?![a-z0-9])'
    return re.search(pattern, text_norm) is not None


def find_matching_skill(candidate_text: str):
    normalized = normalize_skill_text(candidate_text)
    for canonical_name, metadata in SKILL_CATALOG.items():
        aliases = [normalize_skill_text(alias) for alias in metadata.get('aliases', [])]
        if normalized in aliases or normalized == normalize_skill_text(canonical_name):
            return canonical_name
    return None


def extract_skills_from_text(text: str):
    if not text:
        return []
    found = []
    for canonical_name, metadata in SKILL_CATALOG.items():
        aliases = metadata.get('aliases', []) + [canonical_name]
        if any(alias_matches(text, alias) for alias in aliases):
            found.append(canonical_name)
    return sorted(found)


def extract_resume_skills(text: str):
    skill_names = extract_skills_from_text(text)
    result = []
    for name in skill_names:
        result.append({
            'name': name,
            'category': SKILL_CATALOG[name]['category'],
            'canonical_name': name,
            'confidence': 0.95 if alias_matches(text, name) else 0.8
        })
    return result
