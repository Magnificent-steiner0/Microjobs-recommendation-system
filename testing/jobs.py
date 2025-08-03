#   ----------------It is a test route to get all the jobs--------------


from fastapi import APIRouter, HTTPException
from schemas import AllJobsResponseIn
from db import database

router = APIRouter(prefix="/test/jobs", tags=["jobs"])



async def get_all_jobs():
    """
    this function fetched all the job data from database and formats it according to the schmea
    
    we only need job title, type, description, tags and category
    """
    try:
        cursor = database.jobs.find({})
        jobs = await cursor.to_list(length=None) 
        formatted_jobs = []
        
        for job in jobs:
            job["id"] = str(job["_id"])
            del job["_id"]
            formatted_job = {
                "id": job["id"],
                "type": job.get("type", "paid"),
                "job_title": job.get("job_title", ""),
                "description": job.get("description", ""),
                "tags": job.get("tags", []),
                "job_category": job.get("job_category", "")
            }
            
            formatted_jobs.append(formatted_job)
            
        return AllJobsResponseIn(
            data=formatted_jobs
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Error fetching jobs: {str(e)}"
        )

@router.get("/all", response_model=AllJobsResponseIn)
async def fetch_all_jobs():
    return await get_all_jobs()

