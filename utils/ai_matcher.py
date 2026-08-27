from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

def caluclate_similarity(resume_text , job_description):
    documents=[
        resume_text,
        job_description
    ]
    Vectorizer = TfidfVectorizer()
    
    vectors = Vectorizer.fit_transform(documents)
    
    similarity = cosine_similarity(vectors[0],vectors[1])
    
    percentage = similarity[0][0]*100
    
    return round(percentage,2)


if __name__ == "__main__":

    resume = """
    Python developer with experience in Flask,
    MySQL, Git and web development.
    """

    job = """
    We are looking for a Python developer with
    Flask, MySQL and Git experience for web development.
    """

    result = caluclate_similarity(resume, job)

    print("Similarity:", result, "%")