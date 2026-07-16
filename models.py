from typing import Optional
from pydantic import BaseModel


class Books(BaseModel):
    name : str
    author : str
    status : str
    borrower : Optional[str] = None
        
