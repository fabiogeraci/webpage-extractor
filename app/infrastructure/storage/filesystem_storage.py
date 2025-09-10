import os
from datetime import datetime
from ...domain.ports import StoragePort
from ...config import settings


class FilesystemStorage(StoragePort):
    def __init__(self, base_dir: str | None = None) -> None:
        self.base_dir = base_dir or settings.base_data_dir
        
        # Map host paths to container paths
        if os.path.isabs(self.base_dir) and self.base_dir.startswith("/home/"):
            self.base_dir = os.path.normpath(os.path.join("/host", self.base_dir.lstrip("/")))
            print(f"Mapped base_dir to container path: {self.base_dir}")
        
        # Ensure the directory exists and is accessible
        try:
            os.makedirs(self.base_dir, exist_ok=True)
            # Test write access
            test_file = os.path.join(self.base_dir, ".test_write")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
            print(f"Base directory accessible: {self.base_dir}")
        except (OSError, PermissionError) as e:
            raise ValueError(f"Cannot access or create directory '{self.base_dir}': {e}")


    def list_destinations(self) -> list[str]:
        return [d for d in sorted(os.listdir(self.base_dir)) if os.path.isdir(os.path.join(self.base_dir, d))]


    def ensure_destination(self, name: str) -> str:
        # allow alnum, dash, underscore, slash (subfolders), but keep inside base
        safe = name.strip().strip("/ ")
        if not safe:
            safe = datetime.now().strftime("export-%Y%m%d-%H%M%S")
        
        # If the name is an absolute path, map it to the host filesystem
        if os.path.isabs(safe):
            # Map host path to container path via /host/home mount
            if safe.startswith("/home/"):
                dest = os.path.normpath(os.path.join("/host", safe.lstrip("/")))
            else:
                # For other absolute paths, try to map them
                dest = os.path.normpath(os.path.join("/host", safe.lstrip("/")))
            print(f"Mapping host path {safe} to container path {dest}")
            print(f"Checking if destination exists: {os.path.exists(dest)}")
        else:
            dest = os.path.normpath(os.path.join(self.base_dir, safe))
            # Only check for directory traversal if using relative path
            if not dest.startswith(os.path.abspath(self.base_dir)):
                raise ValueError("Destination escapes base directory")
        
        print(f"Creating destination directory: {dest}")
        os.makedirs(dest, exist_ok=True)
        os.makedirs(os.path.join(dest, "images"), exist_ok=True)
        print(f"Destination directory created successfully: {dest}")
        return dest


    def save_markdown(self, dest: str, filename: str, content: str) -> str:
        path = os.path.join(dest, filename)
        print(f"Saving markdown to: {path}")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Markdown saved successfully: {path}")
        return path


    def save_binary(self, dest: str, filename: str, content: bytes) -> str:
        path = os.path.join(dest, filename)
        print(f"Saving binary file to: {path}")
        with open(path, "wb") as f:
            f.write(content)
        print(f"Binary file saved successfully: {path}")
        return path