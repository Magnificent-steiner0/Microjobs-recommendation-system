from typing import List, Optional
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime
from enum import Enum

class JobResponseIn(BaseModel):
    id: str
    type: str
    job_title: str
    description: str
    tags: List[str]=[]
    job_category: str
    

class AllJobsResponseIn(BaseModel):
    data: List[JobResponseIn]
    
    
class UserIDRequest(BaseModel):
    user_id: str


class JobPreference(str,Enum):
    engineering = "engineering"
    marketing = "marketing"
    design = "design"
    management = "management"
    finance = "finance"
    micro_jobs = "micro_jobs"
    customer_service = "customer_service"
    writing = "writing"
    data_entry = "data_entry"
    it_support = "it_support"
    sales = "sales"
    consulting = "consulting"
    education = "education"
    healthcare = "healthcare"
    construction = "construction"

        
class JobAction(str,Enum):
    view = "view"
    apply = "apply"
    join = "join"
        
class JobClicks(BaseModel):
    job_type: str
    job_category: str
    job_tags: List[str]=[]
    
class UserProfile(BaseModel):
    id: str
    job_preference: List[JobPreference]
    job_clicks: List[JobClicks]
    
    class Config:
        from_attributes = True