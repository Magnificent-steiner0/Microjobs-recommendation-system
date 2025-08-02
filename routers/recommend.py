from bson import ObjectId
from fastapi import APIRouter, HTTPException
from helper.vectorizer import user_vectorizer
from helper.recommender import get_top_jobs
from schemas import AllJobsResponseIn, UserProfile
from db import database

router = APIRouter(prefix="/recommend", tags=["recommend"])

@router.post("/")
async def recommend_jobs(profile: UserProfile):
    """
    this function has a UserProfile argument. 
    UserProfile is a schema that consists of only the necessary infomartion to predict the recommendation
    
    -> user_vectorizer : It is a function that vectorizes the user's job preference, clicked jobs data.
                        Returns a vector
    
    -> get_top_jobs : This function gets the top jobs similar to the user profile.
                        Returns a list of job ids
                        
    
    """
    user_vector = user_vectorizer(profile.model_dump())
    if user_vector is None:
        raise HTTPException(
            status_code=400,
            detail="User profile is empty or invalid"
        )
    job_ids = get_top_jobs(user_vector)
    
    # print(job_ids)
    
    results = []
    
    for job_id in job_ids:
        job = await database.jobs.find_one({"_id": ObjectId(job_id)})
        if job:
            results.append({
                "id": str(job["_id"]),
                "type": job.get("type", "paid"),
                "job_title": job.get("job_title", ""),
                "description": job.get("description", ""),
                "tags": job.get("tags", []),
                "job_category": job.get("job_category", ""),
            })
        if len(results) == 5:
            break
    return {"jobs": results}
    

