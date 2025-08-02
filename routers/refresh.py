from fastapi import APIRouter, HTTPException
from db import database
from helper.recommender import build_faiss_index
from helper.vectorizer import job_vectorizer
from bson import ObjectId
import numpy as np

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/refresh")
async def get_all_jobs():
    """
        Everytime the user hits the jobs page or refreshes it will be called.
        Fetches all jobs into a list and then formats it
    """
    try:
        cursor = database.jobs.find({})
        jobs = await cursor.to_list(length=None) 
        formatted_jobs = []
        job_ids = []
        
        for job in jobs:
            job["id"] = str(job["_id"])
            job_ids.append(job["id"])
            
            formatted_job = {
                "id": job["id"],
                "type": job.get("type", "paid"),
                "job_title": job.get("job_title", ""),
                "description": job.get("description", ""),
                "tags": job.get("tags", []),
                "job_category": job.get("job_category", "")
            }
            formatted_jobs.append(formatted_job)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Error fetching jobs: {str(e)}"
        )
          
    from helper.vectorizer import vectorizer  # ensure it uses same global instance
    try:
        job_vectors = job_vectorizer(formatted_jobs)
        build_faiss_index(np.array(job_vectors), job_ids)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while vectorizing or building FAISS index: {str(e)}"
        )
  
    return {"message": f"{len(jobs)} jobs refreshed and indexed."}
       

# @router.post("/refresh")
# async def refresh_jobs():
#     jobs_cursor = database.jobs.find({"status": "open"})
#     jobs = await jobs_cursor.to_list(length=None)

#     if not jobs:
#         return {"error": "No open jobs found"}

#     formatted_jobs = []
#     job_ids = []

#     for job in jobs:
#         job_id = str(job["_id"])
#         job_ids.append(job_id)

#         formatted_job = {
#             "id": job_id,
#             "type": job.get("type", "paid"),
#             "job_title": job.get("job_title", ""),
#             "description": job.get("description", ""),
#             "tags": job.get("tags", []),
#             "job_category": job.get("job_category", ""),
#             "status": job.get("status", "open"),
#         }

#         # Cache in Redis
#         redis_client.set(f"job:{job_id}", json.dumps(formatted_job))
#         formatted_jobs.append(formatted_job)

#     from vectorizer import vectorizer  # ensure it uses same global instance
#     job_vectors = build_job_matrix(formatted_jobs)
#     build_faiss_index(np.array(job_vectors), job_ids)

#     return {"message": f"{len(jobs)} jobs refreshed and indexed."}