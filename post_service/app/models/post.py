from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    slug: str
    title: str
    description: str
    content: str
    image: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "slug": "example-post",
                "title": "Example Post Title",
                "description": "Description of the post",
                "image": "https://picsum.photos/200",
                "content": "Content of the example post"
            }
        }

class PostUpdate(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    slug: str = None
    title: str = None
    description: str = None
    content: str = None
    image: Optional[str] = None
    created_at: Optional[datetime] = Field(default_factory=datetime.now)