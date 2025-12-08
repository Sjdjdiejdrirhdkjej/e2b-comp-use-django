import os
from pathlib import Path


class MockDaytonaSandbox:
    """Mock sandbox for demonstration when no API key is available.

    Ensures all file operations are confined to the sandbox workspace.
    """

    def __init__(self, workspace_dir: str = "/home/runner/workspace"):
        self.workspace_dir = workspace_dir

    def _resolve_within_workspace(self, file_path: str):
        workspace = Path(self.workspace_dir).resolve()
        p = Path(file_path)
        try:
            if p.is_absolute():
                # Allow legacy /project/workspace paths by mapping them into the sandbox
                try:
                    rel = p.relative_to("/project/workspace")
                    full = workspace / rel
                except Exception:
                    # If path is already within the real workspace, map it
                    try:
                        rel = p.relative_to(workspace)
                        full = workspace / rel
                    except Exception:
                        return None, "Access denied: Path must be within workspace directory"
            else:
                full = (workspace / p)

            full_resolved = full.resolve()
            if not str(full_resolved).startswith(str(workspace)):
                return None, "Access denied: Path must be within workspace directory"

            return str(full_resolved), None
        except Exception as e:
            return None, f"Invalid path: {str(e)}"

    def read_file(self, file_path: str) -> str:
        """Mock file read operation"""
        try:
            full_path, error = self._resolve_within_workspace(file_path)
            if error:
                return error

            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Return path shown as provided by user to avoid leaking internal layout
            return f"File content from {file_path}:\n\n{content}"
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"

    def write_file(self, file_path: str, content: str) -> str:
        """Mock file write operation"""
        try:
            full_path, error = self._resolve_within_workspace(file_path)
            if error:
                return error

            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file '{file_path}': {str(e)}"

    def delete_file(self, file_path: str) -> str:
        """Mock file delete operation"""
        try:
            full_path, error = self._resolve_within_workspace(file_path)
            if error:
                return error

            if Path(full_path).exists():
                Path(full_path).unlink()
                return f"Successfully deleted {file_path}"
            else:
                return f"Error: File '{file_path}' does not exist"
        except Exception as e:
            return f"Error deleting file '{file_path}': {str(e)}"

    def list_files(self, directory_path: str) -> str:
        """Mock directory listing operation"""
        try:
            full_path, error = self._resolve_within_workspace(directory_path)
            if error:
                return error

            p = Path(full_path)
            if not p.exists():
                return f"Error: Directory '{directory_path}' does not exist"

            items = []
            for item in p.iterdir():
                item_type = "DIR" if item.is_dir() else "FILE"
                size = item.stat().st_size if item.is_file() else 0
                items.append(f"{item_type}: {item.name} ({size} bytes)")

            if not items:
                return f"Contents of {directory_path}:\n\n(empty directory)"

            return f"Contents of {directory_path}:\n\n" + "\n".join(sorted(items))
        except Exception as e:
            return f"Error listing directory '{directory_path}': {str(e)}"

    def get_file_info(self, file_path: str) -> str:
        """Mock file info operation"""
        try:
            full_path, error = self._resolve_within_workspace(file_path)
            if error:
                return error

            p = Path(full_path)
            if not p.exists():
                return f"Error: File '{file_path}' does not exist"

            stat_info = p.stat()
            file_type = "Directory" if p.is_dir() else "File"

            return f"""File Information for {file_path}:
Type: {file_type}
Size: {stat_info.st_size} bytes
Modified: {stat_info.st_mtime}
Permissions: {oct(stat_info.st_mode)[-3:]}"""
        except Exception as e:
            return f"Error getting file info '{file_path}': {str(e)}"

    def execute_code(self, code: str, language: str) -> str:
        """Mock code execution operation"""
        return f"Mock code execution ({language}):\n{code}\n\n[Mock mode - actual execution requires Daytona API key]"


class SecureDaytonaOperations:
    """Secure file operations using mock implementation."""

    def __init__(self, workspace_dir: str = "/home/runner/workspace"):
        self.mock_mode = True
        self.workspace_dir = workspace_dir

    def _get_sandbox(self):
        return MockDaytonaSandbox(self.workspace_dir)

    def read_file(self, file_path: str) -> str:
        return self._get_sandbox().read_file(file_path)

    def write_file(self, file_path: str, content: str) -> str:
        return self._get_sandbox().write_file(file_path, content)

    def delete_file(self, file_path: str) -> str:
        return self._get_sandbox().delete_file(file_path)

    def list_files(self, directory_path: str) -> str:
        return self._get_sandbox().list_files(directory_path)

    def get_file_info(self, file_path: str) -> str:
        return self._get_sandbox().get_file_info(file_path)

    def execute_code(self, code: str, language: str = "python") -> str:
        return self._get_sandbox().execute_code(code, language)


# Global instance for secure operations
secure_daytona_ops = SecureDaytonaOperations()
