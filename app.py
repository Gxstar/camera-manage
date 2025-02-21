from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.cameras import routes as camera_router
from api.lenses import routes as lens_router
from api.brands import routes as brand_router
from api.users import routes as user_router

app = FastAPI(
    title="Camera Lens Catalog API",
    description="An API for managing camera and lens information.",
    version="0.1.0",
)

# 允许所有来源的请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(camera_router.router, prefix="/cameras", tags=["cameras"])
app.include_router(lens_router.router, prefix="/lenses", tags=["lenses"])
app.include_router(brand_router.router, prefix="/brands", tags=["brands"])
app.include_router(user_router.router, prefix="/users", tags=["users"])


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Camera Lens Catalog API!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
