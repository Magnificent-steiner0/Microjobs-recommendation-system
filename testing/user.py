#   ----------------It is a test route to get the user data--------------


from fastapi import APIRouter, HTTPException
from schemas import  UserProfile
from db import database
from bson import ObjectId

router = APIRouter(prefix="/test/user", tags=["user"])



async def get_user_data(user_id: str):
    """
    this function fetched all the job data from database and formats it according to the schmea
    
    we only need job title, type, description, tags and category
    """
    try:
        
        cursor = database.jobclicks.find({"userId": ObjectId(user_id)})
        jobs = await cursor.to_list(length=None)
        formatted_job_clicks = []
        
        for job in jobs:
            job["id"] = str(job["jobId"])
            del job["_id"]
            formatted_job = {
                "job_type": job.get("jobType", "paid"),
                "job_tags": job.get("jobTags", []),
                "job_category": job.get("jobCategory", "")
            }
            
            formatted_job_clicks.append(formatted_job)
            
            
        user = await database.users.find_one({"_id": ObjectId(user_id)})
        formatted_user_data = {
            "id": str(user["_id"]),
            "job_preference": user.get("jobPreference",[]),
            "job_clicks": formatted_job_clicks
            }
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
            
        return formatted_user_data
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f"Error fetching user data: {str(e)}"
        )

@router.get("/{user_id}", response_model=UserProfile)
async def fetch_user_data(user_id: str):
    return await get_user_data(user_id)