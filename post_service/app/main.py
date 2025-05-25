from fastapi import FastAPI
from routes.post_router import router as post_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "suc": 1,
        "msg": "Hello from Post Service"
    }

app.include_router(router=post_router, prefix="/api/v1/posts", tags=["Posts"])