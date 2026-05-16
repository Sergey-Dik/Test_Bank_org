import os
import random
import time

from src.main.api.models.create_user_request import CreateUserRequest


def with_unique_username(request: CreateUserRequest) -> CreateUserRequest:
    suffix = f"{os.getpid()}{int(time.time() * 1000)}{random.randint(1000, 9999)}"
    base = request.username[:10]
    request.username = f"{base}{suffix}"[:15]
    return request
