from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import user_router
from routes.events import event_router
from database.connection import initialize_database
import uvicorn
app = FastAPI()


#register origins
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.on_event("startup")
async def connect():
    await initialize_database()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080,
                reload=True)
