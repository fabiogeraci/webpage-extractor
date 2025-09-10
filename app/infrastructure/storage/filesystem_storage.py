import os
from datetime import datetime
from ...domain.ports import StoragePort
from ...config import settings


class FilesystemStorage(StoragePort):
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or settings.base_data_dir
        # Ensure the directory exists and is accessible
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            # Test write access
            test_file = os.path.join(self.base_dir, ".test_write")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except (OSError, PermissionError) as e:
            raise ValueError(f"Cannot access or create directory '{self.base_dir}': {e}")


    def list_destinations(self) -> list[str]:
        return [d for d in sorted(os.listdir(self.base_dir)) if os.path.isdir(os.path.join(self.base_dir, d))]


    def ensure_destination(self, name: str) -> str:
        # allow alnum, dash, underscore, slash (subfolders), but keep inside base
        safe = name.strip().strip("/ ")
        if not safe:
            safe = datetime.now().strftime("export-%Y%m%d-%H%M%S")
        dest = os.path.normpath(os.path.join(self.base_dir, safe))
        if not dest.startswith(os.path.abspath(self.base_dir)):
            raise ValueError("Destination escapes base directory")
        os.makedirs(dest, exist_ok=True)
        os.makedirs(os.path.join(dest, "images"), exist_ok=True)
        return dest


    def save_markdown(self, dest: str, filename: str, content: str) -> str:
        path = os.path.join(dest, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path


    def save_binary(self, dest: str, filename: str, content: bytes) -> str:
        path = os.path.join(dest, filename)
        with open(path, "wb") as f:
            f.write(content)
        return path