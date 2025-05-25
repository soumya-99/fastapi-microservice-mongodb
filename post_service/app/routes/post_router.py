from datetime import datetime
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from models.post import Post, PostUpdate
from db.config import db

router = APIRouter()

# Helper to convert MongoDB ObjectId to string
def post_helper(post: Post) -> dict:
    return {
        "_id": str(post["_id"]),
        "slug": str(post["slug"]),
        "title": str(post["title"]),
        "description": str(post["description"]),
        "content": str(post["content"]),
        "image": str(post["image"]),
        "created_at": str(post["created_at"]),
    }

@router.post("/", response_description="Add new post")
async def create_post(post: Post):
    post_dict = post.model_dump(by_alias=True)
    post_dict["_id"] = str(uuid4())
    result = await db.md_posts.insert_one(post_dict)
    new_post = await db.md_posts.find_one({"_id": result.inserted_id})

    return {
        "status": 201,
        "result": [post_helper(new_post)]
    }

@router.get("/", response_description="List all posts")
async def list_posts():
    posts = await db.md_posts.find().to_list(length=100)
    return {
        "status": 200,
        "result": [post_helper(post) for post in posts]
    }

@router.get("/{id}", response_description="Get a single post")
async def get_post(id: str):
    if (post := await db.md_posts.find_one({"_id": id})) is not None:
        return {
            "status": 200,
            "result": [post_helper(post)]
        }
    raise HTTPException(status_code=404, detail=f"Post {id} not found!")

# @router.put("/{id}", response_description="Update a post")
# async def update_post(id: str, post: PostUpdate):
#     post_dict = {k: v for k, v in post.model_dump(by_alias=True).items() if v is not None}
#     if len(post_dict) >= 1:
#         update_result = await db.md_posts.update_one(
#             {"_id": id}, {"$set": post_dict}
#         )
#         if update_result.modified_count == 1:
#             if (updated_post := await db.md_posts.find_one({"_id": id})) is not None:
#                 return {
#                     "status": 200,
#                     "result": [post_helper(updated_post)]
#                 }
#     if (existing_post := await db.md_posts.find_one({"_id"})) is not None:
#         return {
#             "status": 200,
#             "result": [post_helper(existing_post)]
#         }
    
#     raise HTTPException(status_code=404, detail="Post not found!")
@router.put("/{id}", response_description="Update a post")
async def update_post(id: str, post: PostUpdate):
    update_data = {k: v for k, v in post.model_dump(by_alias=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update fields provided.")

    updated_post = await db.md_posts.find_one_and_update(
        {"_id": id},
        {"$set": update_data},
        return_document=True
    )

    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found.")
    
    return {
        "status": 200,
        "result": [post_helper(updated_post)]
    }

# @router.delete("/{id}", response_description="Delete a post")
# async def delete_post(id: str):
#     delete_result = await db.md_posts.delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return {
#             "status": 200,
#             "result": [f"Post {id} deleted successfully"]
#         }
#     raise HTTPException(status_code=404, detail="Post not found!")
@router.delete("/{id}", response_description="Delete a post")
async def delete_post(id: str):
    deleted_post = await db.md_posts.find_one_and_delete({"_id": id})
    
    if deleted_post:
        deleted_post["deleted_at"] = datetime.now(datetime.timezone.utc)
        
        await db.td_deleted_posts.insert_one(deleted_post)
        
        return {
            "status": 200,
            "result": [f"Post {id} deleted successfully and archived."]
        }
    
    raise HTTPException(status_code=404, detail="Post not found!")