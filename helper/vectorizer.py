from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=500)

def job_vectorizer(jobs):
    job_texts = [
        job.get("title", "")+" "+" ".join(job.get("tags",[])) for job in jobs 
    ]
    matrix = vectorizer.fit_transform(job_texts)
    return matrix.toarray()

def user_vectorizer(user):
    user_texts = " ".join(user.get("skills", [])) + " ".join(user.get("preferred_type", []))
    return vectorizer.transform([user_texts]).toarray()