SKILL_CATALOG = {
    'Python': {'category': 'Programming', 'aliases': ['python', 'py', 'python programming']},
    'JavaScript': {'category': 'Web', 'aliases': ['javascript', 'js', 'ecmascript']},
    'TypeScript': {'category': 'Web', 'aliases': ['typescript', 'ts']},
    'SQL': {'category': 'Database', 'aliases': ['sql', 'mysql', 'postgresql', 'postgres', 'database querying']},
    'Pandas': {'category': 'Data', 'aliases': ['pandas', 'dataframes']},
    'NumPy': {'category': 'Data', 'aliases': ['numpy', 'np']},
    'Machine Learning': {'category': 'AI/ML', 'aliases': ['machine learning', 'ml', 'predictive modeling', 'sklearn']},
    'Deep Learning': {'category': 'AI/ML', 'aliases': ['deep learning', 'neural networks', 'cnn', 'rnn', 'transformers']},
    'Statistics': {'category': 'Analytics', 'aliases': ['statistics', 'statistical analysis', 'statistical modeling']},
    'Data Visualization': {'category': 'Analytics', 'aliases': ['data visualization', 'matplotlib', 'seaborn', 'power bi', 'tableau', 'plotly']},
    'React': {'category': 'Web', 'aliases': ['react', 'next.js', 'nextjs']},
    'Node.js': {'category': 'Web', 'aliases': ['node.js', 'nodejs', 'node js']},
    'Git': {'category': 'DevOps', 'aliases': ['git', 'github', 'gitlab']},
    'Docker': {'category': 'DevOps', 'aliases': ['docker', 'containerization']},
    'AWS': {'category': 'Cloud', 'aliases': ['aws', 'amazon web services']},
    'Azure': {'category': 'Cloud', 'aliases': ['azure', 'microsoft azure']},
    'HTML': {'category': 'Web', 'aliases': ['html', 'html5']},
    'CSS': {'category': 'Web', 'aliases': ['css', 'css3']},
    'Java': {'category': 'Programming', 'aliases': ['java']},
    'C++': {'category': 'Programming', 'aliases': ['c++', 'cpp']},
    'TensorFlow': {'category': 'AI/ML', 'aliases': ['tensorflow', 'tf']},
    'PyTorch': {'category': 'AI/ML', 'aliases': ['pytorch', 'torch']},
    'NLP': {'category': 'AI/ML', 'aliases': ['nlp', 'natural language processing']},
    'PostgreSQL': {'category': 'Database', 'aliases': ['postgresql', 'postgres', 'pg']},
    'MongoDB': {'category': 'Database', 'aliases': ['mongodb', 'mongo db']},
    'Kubernetes': {'category': 'DevOps', 'aliases': ['kubernetes', 'k8s']},
    'CI/CD': {'category': 'DevOps', 'aliases': ['ci/cd', 'continuous integration', 'continuous deployment']},
    'Power BI': {'category': 'Analytics', 'aliases': ['power bi', 'powerbi']},
    'Excel': {'category': 'Data', 'aliases': ['excel', 'microsoft excel']},
    'C': {'category': 'Programming', 'aliases': ['c programming']},
    'REST API': {'category': 'Web', 'aliases': ['rest api', 'restful api', 'rest services']},
    'MySQL': {'category': 'Database', 'aliases': ['mysql']},
    'Google Cloud': {'category': 'Cloud', 'aliases': ['google cloud', 'gcp']},
    'Linux': {'category': 'DevOps', 'aliases': ['linux', 'ubuntu']},
    'Communication': {'category': 'Professional', 'aliases': ['communication', 'communicating']},
    'Teamwork': {'category': 'Professional', 'aliases': ['teamwork', 'collaboration']},
    'Problem Solving': {'category': 'Professional', 'aliases': ['problem solving', 'problem-solving']},
    'Presentation': {'category': 'Professional', 'aliases': ['presentation', 'presentations']},
}

JOB_ROLE_SEED = {
    'Python Developer': {
        'description': 'Build backend services and data processing solutions using Python and modern web tooling.',
        'skills': {'Python': 10, 'SQL': 8, 'Git': 6, 'Docker': 5, 'AWS': 5, 'REST API': 7}
    },
    'Data Analyst': {
        'description': 'Analyze business and operational data to produce insight and dashboards.',
        'skills': {'SQL': 10, 'Python': 8, 'Excel': 7, 'Statistics': 8, 'Data Visualization': 8, 'Power BI': 7}
    },
    'Data Scientist': {
        'description': 'Solve analytical and predictive problems using statistical methods and ML workflows.',
        'skills': {'Python': 10, 'Machine Learning': 10, 'SQL': 8, 'Statistics': 8, 'Pandas': 7, 'NumPy': 6, 'Data Visualization': 6, 'Deep Learning': 5}
    },
    'Machine Learning Engineer': {
        'description': 'Design, train, evaluate and deploy production-ready ML systems.',
        'skills': {'Python': 10, 'Machine Learning': 10, 'Deep Learning': 9, 'TensorFlow': 7, 'PyTorch': 7, 'SQL': 6, 'Docker': 5, 'AWS': 5}
    },
    'AI Engineer': {
        'description': 'Integrate AI capabilities into software products and workflows.',
        'skills': {'Python': 10, 'Machine Learning': 9, 'NLP': 8, 'Deep Learning': 8, 'TensorFlow': 7, 'PyTorch': 7, 'SQL': 6}
    },
    'Frontend Developer': {
        'description': 'Develop responsive user interfaces and interactive experiences.',
        'skills': {'HTML': 9, 'CSS': 9, 'JavaScript': 10, 'React': 10, 'TypeScript': 8, 'Git': 5}
    },
    'Backend Developer': {
        'description': 'Build core application logic, integrations and APIs.',
        'skills': {'Python': 9, 'JavaScript': 6, 'Node.js': 8, 'SQL': 8, 'REST API': 9, 'Docker': 5, 'Git': 5}
    },
    'Full Stack Developer': {
        'description': 'Combine frontend, backend and database skills to deliver full applications.',
        'skills': {'JavaScript': 9, 'React': 8, 'Node.js': 8, 'Python': 7, 'SQL': 8, 'Git': 6, 'Docker': 5}
    },
    'Cloud Engineer': {
        'description': 'Design and maintain cloud infrastructure and deployment workflows.',
        'skills': {'AWS': 9, 'Azure': 8, 'Docker': 8, 'Kubernetes': 8, 'CI/CD': 7, 'Git': 6}
    },
    'DevOps Engineer': {
        'description': 'Automate deployment, reliability and infrastructure operations.',
        'skills': {'Docker': 9, 'Kubernetes': 9, 'CI/CD': 9, 'Git': 8, 'AWS': 7, 'Linux': 6}
    },
    'Software Engineer': {
        'description': 'Design, build and maintain reliable software products across the development lifecycle.',
        'skills': {'Python': 8, 'Java': 8, 'JavaScript': 7, 'SQL': 7, 'Git': 7, 'Docker': 5}
    },
    'Business/Data Intelligence Analyst': {
        'description': 'Turn business data into decisions through analysis, reporting and stakeholder communication.',
        'skills': {'SQL': 10, 'Excel': 8, 'Power BI': 9, 'Statistics': 7, 'Data Visualization': 8, 'Presentation': 6}
    },
    'Cybersecurity Analyst': {
        'description': 'Monitor systems, investigate threats and improve security controls and operational resilience.',
        'skills': {'Linux': 8, 'Python': 6, 'SQL': 5, 'Communication': 5, 'Problem Solving': 7, 'Git': 4}
    },
    'Database Developer': {
        'description': 'Develop performant data models, queries and database-backed application solutions.',
        'skills': {'SQL': 10, 'PostgreSQL': 8, 'MySQL': 8, 'Python': 6, 'Git': 5}
    },
    'QA/Automation Engineer': {
        'description': 'Build automated quality practices and reliable test coverage for software products.',
        'skills': {'Python': 7, 'JavaScript': 6, 'SQL': 5, 'Git': 7, 'CI/CD': 8, 'Docker': 5}
    }
}
