from src.main.api.configs.config import Config


def build_api_url(path: str) -> str:
    base = Config.fetch("backendUrl", "").rstrip("/")
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base}{path}"
