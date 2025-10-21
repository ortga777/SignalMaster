from fastapi import APIRouter

router = APIRouter()  # ← Isso deve existir em cada router

@router.post("/login")
async def login():
    return {"message": "Login endpoint"}
