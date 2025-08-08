from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(max_features=500)

def job_vectorizer(jobs):
    job_texts = [
        job.get("title", "")+" "+" ".join(job.get("tags",[])) for job in jobs 
    ]
    matrix = vectorizer.fit_transform(job_texts)
    return matrix.toarray()

def user_vectorizer(user):
    preference_text = " ".join(user.get("job_preference", []))
    click_texts = []
    # here we flattening the job clicks data into a list
    for click in user.get("job_clicks",[]):
        click_texts.append(click.get("job_type",""))
        click_texts.extend(click.get("job_tags", []))
        click_texts.append(click.get("job_category", ""))
        
    click_text_list = " ".join(click_texts)
        
    user_texts = preference_text + " " + click_text_list
    return vectorizer.transform([user_texts]).toarray()