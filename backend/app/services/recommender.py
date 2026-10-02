from app.data.skill_catalog import JOB_ROLE_SEED
from urllib.parse import quote_plus


RECOMMENDATION_LIBRARY = {
    'Machine Learning': {
        'reason': 'Machine learning is central to predictive systems and model building in data-driven roles.',
        'topics': ['Supervised learning', 'Model evaluation', 'Feature engineering', 'Cross-validation'],
        'practice': 'Train a classification model on a public dataset and compare performance metrics.',
        'time_to_learn': '6-10 hours',
    },
    'Deep Learning': {
        'reason': 'Deep learning powers neural networks for complex tasks such as image, text and sequence processing.',
        'topics': ['Neural networks', 'Backpropagation', 'CNNs', 'Transformers'],
        'practice': 'Build a small image classifier or text model using a public dataset.',
        'time_to_learn': '8-12 hours',
    },
    'Statistics': {
        'reason': 'Statistics supports interpretation, uncertainty measurement and reliable decision-making.',
        'topics': ['Probability', 'Hypothesis testing', 'Descriptive statistics', 'Sampling'],
        'practice': 'Analyze a dataset and write a short report using hypothesis tests and summary statistics.',
        'time_to_learn': '4-8 hours',
    },
    'Data Visualization': {
        'reason': 'Visualization converts analytical results into clear business-ready insights.',
        'topics': ['Charts', 'Dashboard design', 'Storytelling with data', 'Exploratory analysis'],
        'practice': 'Create a dashboard with key metrics and annotations from a sample dataset.',
        'time_to_learn': '4-6 hours',
    },
    'SQL': {
        'reason': 'SQL is essential for querying and transforming structured data in analytics and product workflows.',
        'topics': ['Joins', 'Aggregations', 'Window functions', 'Data modeling'],
        'practice': 'Write SQL queries that join multiple tables and answer business questions.',
        'time_to_learn': '3-5 hours',
    },
    'Python': {
        'reason': 'Python is the foundation for data analysis, automation and model development.',
        'topics': ['Functions', 'Lists and dictionaries', 'NumPy', 'Pandas'],
        'practice': 'Build a small script that cleans data and outputs summary insights.',
        'time_to_learn': '5-8 hours',
    },
    'Pandas': {
        'reason': 'Pandas enables efficient data cleaning, transformation and exploration.',
        'topics': ['DataFrames', 'Filtering', 'Grouping', 'Merging'],
        'practice': 'Load a CSV, clean missing values and compute descriptive summaries.',
        'time_to_learn': '4-6 hours',
    },
    'Power BI': {
        'reason': 'Power BI turns data into accessible reports and dashboards for stakeholders.',
        'topics': ['Relationships', 'DAX', 'Dashboards', 'Publishing reports'],
        'practice': 'Create a dashboard with KPIs, filters and trend charts.',
        'time_to_learn': '5-7 hours',
    },
    'NLP': {
        'reason': 'NLP enables the processing and understanding of human language in intelligent applications.',
        'topics': ['Tokenization', 'Embeddings', 'Text classification', 'Sentiment analysis'],
        'practice': 'Build a text classifier for reviews or support tickets.',
        'time_to_learn': '6-9 hours',
    },
    'AWS': {
        'reason': 'Cloud skills help deploy, scale and operate services reliably in production environments.',
        'topics': ['EC2', 'S3', 'IAM', 'Deployments'],
        'practice': 'Deploy a sample web app or pipeline to a cloud environment.',
        'time_to_learn': '7-10 hours',
    },
    'Docker': {
        'reason': 'Containerization makes application environments consistent and reproducible.',
        'topics': ['Images', 'Containers', 'Dockerfiles', 'Compose'],
        'practice': 'Containerize a Python or Node.js app and run it locally.',
        'time_to_learn': '3-5 hours',
    }
}


LEARNING_RESOURCES = {
    'Python': [{'title': 'Official Python Tutorial', 'url': 'https://docs.python.org/3/tutorial/', 'platform': 'Python Docs'}],
    'SQL': [{'title': 'SQLBolt interactive lessons', 'url': 'https://sqlbolt.com/', 'platform': 'SQLBolt'}],
    'Pandas': [{'title': 'Pandas getting started guide', 'url': 'https://pandas.pydata.org/docs/getting_started/index.html', 'platform': 'Pandas Docs'}],
    'Power BI': [{'title': 'Microsoft Learn: Power BI', 'url': 'https://learn.microsoft.com/training/powerplatform/power-bi', 'platform': 'Microsoft Learn'}],
    'AWS': [{'title': 'AWS Skill Builder', 'url': 'https://skillbuilder.aws/', 'platform': 'AWS'}],
    'Docker': [{'title': 'Docker Get Started', 'url': 'https://docs.docker.com/get-started/', 'platform': 'Docker Docs'}],
    'Machine Learning': [{'title': 'Google Machine Learning Crash Course', 'url': 'https://developers.google.com/machine-learning/crash-course', 'platform': 'Google'}],
    'Deep Learning': [{'title': 'PyTorch Tutorials', 'url': 'https://pytorch.org/tutorials/', 'platform': 'PyTorch'}],
}

ROLE_COURSE_LIBRARY = {
    'Data Analyst': {
        'SQL': [{'title': 'Mode SQL Tutorial', 'url': 'https://mode.com/sql-tutorial/', 'platform': 'Mode'}],
        'Python': [{'title': 'Python for Everybody', 'url': 'https://www.py4e.com/', 'platform': 'Coursera / University of Michigan'}],
        'Power BI': [{'title': 'Power BI Desktop training', 'url': 'https://learn.microsoft.com/training/paths/get-started-power-bi/', 'platform': 'Microsoft Learn'}],
    },
    'Data Scientist': {
        'Python': [{'title': 'Python for Data Science', 'url': 'https://www.coursera.org/specializations/python-for-applied-data-science-ai', 'platform': 'Coursera'}],
        'Machine Learning': [{'title': 'Machine Learning Crash Course', 'url': 'https://developers.google.com/machine-learning/crash-course', 'platform': 'Google'}],
        'Statistics': [{'title': 'Statistics Specialization', 'url': 'https://www.coursera.org/specializations/statistics', 'platform': 'Coursera'}],
    },
    'Machine Learning Engineer': {
        'Machine Learning': [{'title': 'Hands-On Machine Learning', 'url': 'https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/', 'platform': 'O’Reilly'}],
        'Deep Learning': [{'title': 'Deep Learning Specialization', 'url': 'https://www.coursera.org/specializations/deep-learning', 'platform': 'Coursera'}],
        'Python': [{'title': 'Python for AI/ML', 'url': 'https://www.coursera.org/learn/python-for-applied-data-science-ai', 'platform': 'Coursera'}],
    },
    'Backend Developer': {
        'Python': [{'title': 'FastAPI Tutorial', 'url': 'https://fastapi.tiangolo.com/tutorial/', 'platform': 'FastAPI'}],
        'SQL': [{'title': 'SQLBolt', 'url': 'https://sqlbolt.com/', 'platform': 'SQLBolt'}],
        'REST API': [{'title': 'REST API Design', 'url': 'https://restfulapi.net/', 'platform': 'REST API Tutorial'}],
    },
    'Frontend Developer': {
        'HTML': [{'title': 'MDN HTML Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTML', 'platform': 'MDN'}],
        'CSS': [{'title': 'MDN CSS Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS', 'platform': 'MDN'}],
        'JavaScript': [{'title': 'JavaScript MDN Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'platform': 'MDN'}],
    },
    'Cloud Engineer': {
        'AWS': [{'title': 'AWS Skill Builder', 'url': 'https://skillbuilder.aws/', 'platform': 'AWS'}],
        'Docker': [{'title': 'Docker Get Started', 'url': 'https://docs.docker.com/get-started/', 'platform': 'Docker Docs'}],
        'Kubernetes': [{'title': 'Kubernetes Basics', 'url': 'https://kubernetes.io/docs/tutorials/kubernetes-basics/', 'platform': 'Kubernetes'}],
    }
}

LEVEL_PATHS = {
    'beginner': ['Start with the fundamentals', 'Practice with a guided exercise', 'Build a small project'],
    'intermediate': ['Review the core concepts', 'Apply in a realistic workflow', 'Solve a mini project with debugging'],
    'advanced': ['Study architecture and trade-offs', 'Build production-style solutions', 'Optimize and review with metrics'],
}


def build_study_schedule(skill, experience_level='fresher'):
    level = 'beginner' if experience_level in {'fresher'} else 'intermediate' if experience_level in {'intermediate'} else 'advanced'
    base_steps = LEVEL_PATHS[level]
    steps = [
        {'day': 'Day 1', 'focus': f'Learn the core concepts of {skill}', 'goal': base_steps[0]},
        {'day': 'Day 2', 'focus': f'Practice key examples in {skill}', 'goal': base_steps[1]},
        {'day': 'Day 3', 'focus': f'Build a small project using {skill}', 'goal': base_steps[2]},
    ]
    if skill in {'Machine Learning', 'Deep Learning', 'AWS'}:
        steps.append({'day': 'Day 4', 'focus': f'Review metrics and deployment for {skill}', 'goal': 'Measure execution quality and final output'})
    return steps


def build_learning_path(skill, experience_level='fresher'):
    level_key = 'beginner' if experience_level in {'fresher'} else 'intermediate' if experience_level in {'intermediate'} else 'advanced'
    return {
        'level': level_key,
        'path': LEVEL_PATHS[level_key],
    }


def build_role_resources(skill, job_title=None):
    if not job_title:
        return []
    role_map = ROLE_COURSE_LIBRARY.get(job_title, {})
    return role_map.get(skill, [])


EXPERIENCE_GUIDANCE = {
    'fresher': 'Start with the fundamentals and guided exercises, then complete one small portfolio project.',
    'intermediate': 'Apply this skill in an end-to-end project and practice realistic workflows and debugging.',
    'experienced': 'Focus on architecture, trade-offs, scalability, and reviewing or mentoring others in this skill.',
}



def build_recommendations(missing_skills, experience_level='fresher', job_title=None):
    recs = []
    for index, skill in enumerate(missing_skills, start=1):
        meta = RECOMMENDATION_LIBRARY.get(skill, {
            'reason': f'{skill} is relevant for the target role and should be developed further.',
            'topics': ['Core concepts', 'Application practice', 'Project integration'],
            'practice': 'Apply the skill through a mini project connected to your career goal.',
            'time_to_learn': '4-6 hours',
        })
        resources = list(LEARNING_RESOURCES.get(skill, [{
            'title': f'Find a course for {skill}',
            'url': f'https://www.coursera.org/search?query={quote_plus(skill)}',
            'platform': 'Coursera',
        }]))
        job_resources = build_role_resources(skill, job_title)
        if job_resources:
            resources = resources + job_resources
        recs.append({
            'skill': skill,
            'priority': 'High' if index <= 2 else ('Medium' if index <= 4 else 'Low'),
            'reason': meta['reason'],
            'topics': meta['topics'],
            'practice': meta['practice'],
            'learning_order': index,
            'time_to_learn': meta['time_to_learn'],
            'experience_guidance': EXPERIENCE_GUIDANCE.get(experience_level, EXPERIENCE_GUIDANCE['fresher']),
            'learning_path': build_learning_path(skill, experience_level),
            'study_schedule': build_study_schedule(skill, experience_level),
            'learning_resources': resources,
            'job_role_recommendations': job_resources,
        })
    return recs


def build_learning_roadmap(missing_skills):
    roadmap = []
    if 'Python' in missing_skills:
        roadmap.append('Python Fundamentals')
    if 'Statistics' in missing_skills:
        roadmap.append('Statistics')
    if 'Pandas' in missing_skills:
        roadmap.append('Pandas and NumPy')
    if 'Machine Learning' in missing_skills:
        roadmap.append('Machine Learning')
    if 'Deep Learning' in missing_skills:
        roadmap.append('Deep Learning')
    if 'Data Visualization' in missing_skills:
        roadmap.append('Data Visualization')
    if 'SQL' in missing_skills:
        roadmap.append('SQL and Data Modeling')

    if not roadmap:
        roadmap = ['Practical project execution', 'Portfolio polishing', 'Interview preparation']
    return roadmap
