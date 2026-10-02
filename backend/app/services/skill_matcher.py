from app.services.recommender import build_learning_roadmap, build_recommendations
from app.services.semantic_matcher import semantic_skill_matches


def compute_match_score(matched_count, total_required):
    if total_required == 0:
        return 0.0
    return round((matched_count / total_required) * 100, 2)


def compute_weighted_score(matched_skills, required_skills):
    if not required_skills:
        return 0.0
    total_weight = sum(item['importance'] for item in required_skills)
    matched_weight = sum(item['importance'] for item in required_skills if item['name'] in matched_skills)
    if total_weight == 0:
        return 0.0
    return round((matched_weight / total_weight) * 100, 2)


def normalize_job_skills(job_skills):
    return [{'name': skill_name, 'importance': value} for skill_name, value in job_skills.items()]


def analyze_resume_against_job(resume_skills, job_id, job_data, experience_level='fresher', job_title=None):
    required_skill_map = job_data['skills']
    required_skill_names = list(required_skill_map.keys())
    detected = {name.strip().casefold() for name in resume_skills}
    matched = [name for name in required_skill_names if name.casefold() in detected]
    semantic_matches, semantic_score = semantic_skill_matches(list(resume_skills), required_skill_names)
    matched = list(dict.fromkeys(matched + [name for name in semantic_matches if name in required_skill_names]))
    missing = [name for name in required_skill_names if name.casefold() not in detected]

    score = compute_match_score(len(matched), len(required_skill_names))
    weighted_score = compute_weighted_score(matched, [{'name': name, 'importance': importance} for name, importance in required_skill_map.items()])

    missing_priority = {'High': [], 'Medium': [], 'Low': []}
    for skill in missing:
        importance = required_skill_map[skill]
        priority = 'High' if importance >= 8 else 'Medium' if importance >= 5 else 'Low'
        missing_priority[priority].append(skill)

    category_summary = {}
    for skill_name in matched:
        category = job_data.get('categories', {}).get(skill_name, 'General')
        category_summary.setdefault(category, {'matched': 0, 'required': 0})['matched'] += 1
    for skill_name in required_skill_names:
        category = job_data.get('categories', {}).get(skill_name, 'General')
        category_summary.setdefault(category, {'matched': 0, 'required': 0})['required'] += 1

    recommendations = build_recommendations(missing, experience_level, job_title=job_title)
    roadmap = build_learning_roadmap(missing)
    return {
        'score': max(score, weighted_score),
        'matched_skills': matched,
        'missing_skills': missing,
        'priority_summary': missing_priority,
        'recommendations': recommendations,
        'roadmap': roadmap,
        'detected_skills': sorted(set(resume_skills)),
        'weighted_score': weighted_score,
        'semantic_score': semantic_score,
        'matched_count': len(matched),
        'required_count': len(required_skill_names),
        'missing_count': len(missing),
        'category_summary': category_summary,
    }
