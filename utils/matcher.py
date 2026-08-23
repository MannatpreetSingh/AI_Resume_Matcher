SKILLS=[
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "flask",
    "django",
    "mysql",
    "sql",
    "mongodb",
    "git",
    "github",
    "docker",
    "aws",
    "react",
    "node.js",
    "php",
    "laravel",
    "machine learning",
    "data analysis",
    "pandas",
    "numpy",
    "scikit-learn"   
]
def extract_skills(text):
    text=text.lower()
    found_skills=[]
    
    for skill in SKILLS:
        
        if skill  in text:
            found_skills.append(skill)
    return found_skills
    
def calculate_match(resume_text, job_description):
    resume_skills=extract_skills(resume_text)
    job_skills=extract_skills(job_description)
    
    matched_skills =[]
    
    for skills in job_skills:   
        
        if skills in resume_skills:
                matched_skills.append(skills)
    missing_skill=[
        skill for skill in job_skills
        if skill not in resume_skills
    ]            
    if len(job_skills)==0:
            match_percentage=0
    else:
        match_percentage=(
            len(matched_skills)/len(job_skills)
        )*100
        return{
            "match_percentage": round(match_percentage,2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skill
        }