import os

class EnvWrapper:
    @staticmethod
    def get(key: str, default: str = None) -> str:
        return os.getenv(key, default)

    @staticmethod
    def get_bool(key: str, default: bool = False) -> bool:
        val = os.getenv(key, str(default)).lower()
        return val in ("true", "1", "yes")

    @staticmethod
    def get_int(key: str, default: int = 0) -> int:
        return int(os.getenv(key, str(default)))
