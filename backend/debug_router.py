import sys
import os

# Add backend to path
sys.path.append(os.getcwd())

from core.apis.routers.user_router import user_router

print("Routes in user_router:")
for route in user_router.routes:
    print(f"Path: {route.path}, Name: {route.name}")
