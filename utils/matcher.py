SKILLS_ALIASES = {
    "python": ["python", "python3"],

    "flask": ["flask"],

    "django": ["django"],

    "mysql": ["mysql", "mysql database"],

    "sql": ["sql", "structured query language"],

    "html": ["html", "html5"],

    "css": ["css", "css3"],

    "javascript": ["javascript", "js"],

    "react": ["react", "reactjs", "react.js"],

    "node.js": ["node.js", "nodejs", "node"],

    "git": ["git", "github", "gitlab"],

    "docker": ["docker", "containerization"],

    "aws": ["aws", "amazon web services"],

"machine learning": [
    "machine learning",
    "ml",
    "machine-learning"
],

"scikit-learn": [
    "scikit-learn",
    "sklearn"
],

"pandas": ["pandas"],

"numpy": ["numpy"],

"java": ["java"],

"c++": ["c++"],

"php": ["php"]
}
def extract_skills(text):
    text=text.lower()
    found_skills=[]
    
    for skill, aliases in SKILLS_ALIASES.items():
        for alias in aliases:
            if alias in text:
                found_skills.append(skill)
                break
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
