from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

class JobResponseIn(BaseModel):
    id: str
    type: str
    job_title: str
    description: str
    tags: List[str]=[]
    job_category: str
    

class AllJobsResponseIn(BaseModel):
    data: List[JobResponseIn]


class UserProfile(BaseModel):
    skills:  List[str]=[]
    preferred_type: List[str]=[]