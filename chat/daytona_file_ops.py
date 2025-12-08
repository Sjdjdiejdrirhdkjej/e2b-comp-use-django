import os
import json
from pathlib import Path
from django.conf import settings

try:
    from daytona import Daytona, DaytonaConfig

    DAYTONA_AVAILABLE = True
except ImportError:
    DAYTONA_AVAILABLE = False


class DaytonaFileOperations:
    """Secure file operations using Daytona containers via SDK"""

    def __init__(self):
        self.workspace_dir = "/home/runner/workspace"
        self.container_name = "file-ops-sandbox"
        self.daytona_config = self._load_daytona_config()
        self.sandbox = None
        self._init_daytona_sandbox()

    def _load_daytona_config(self):
        """Load Daytona configuration"""
        try:
            with open("/home/runner/workspace/daytona.json", "r") as f:
                return json.load(f)
        except Exception:
            return {"daytona": {"environment": "python"}}

    def _init_daytona_sandbox(self):
        """Initialize Daytona sandbox"""
        if not DAYTONA_AVAILABLE:
            return

        try:
            # Initialize Daytona client
            api_key = os.getenv("DAYTONA_API_KEY")
            api_url = os.getenv("DAYTONA_API_URL")

            if api_key:
                config = DaytonaConfig(api_key=api_key, api_url=api_url)
                daytona = Daytona(config)
            else:
                # Use environment variables by default
                daytona = Daytona()

            # Create sandbox
            self.sandbox = daytona.create()
        except Exception as e:
            print(f"Failed to initialize Daytona sandbox: {e}")
            self.sandbox = None

    def _validate_path(self, file_path):
        """Validate and sanitize file path"""
        # Map legacy /project/workspace to the sandbox workspace
        if isinstance(file_path, str) and file_path.startswith("/project/workspace"):
            suffix = file_path[len("/project/workspace"):]
            file_path = os.path.join(self.workspace_dir, suffix.lstrip("/"))

        # Convert to absolute path
        if not os.path.isabs(file_path):
            file_path = os.path.join(self.workspace_dir, file_path)

        # Security: Ensure path is within workspace
        try:
            path_obj = Path(file_path).resolve()
            workspace_obj = Path(self.workspace_dir).resolve()

            if not str(path_obj).startswith(str(workspace_obj)):
                return None, "Access denied: Path must be within workspace directory"

            return str(path_obj), None
        except Exception as e:
            return None, f"Invalid path: {str(e)}"

    def _use_sdk_fallback(self, operation, *args, **kwargs):
        """Fallback method when SDK is not available"""
        return f"Error: Daytona SDK not available. Install with: pip install daytona"

    def read_file(self, file_path):
        """Read file content securely in container"""
        validated_path, error = self._validate_path(file_path)
        if error or not validated_path:
            return error or "Error: Invalid file path"

        if not self.sandbox:
            return self._use_sdk_fallback("read_file")

        try:
            # Check file size (limit to 10MB) using local stat for validation
            file_size = os.path.getsize(validated_path)
            if file_size > 10 * 1024 * 1024:  # 10MB
                return "Error: File too large (max 10MB)"

            # Read file using Daytona SDK
            # Convert absolute path to relative path for sandbox
            relative_path = os.path.relpath(validated_path, self.workspace_dir)

            # Use sandbox filesystem to read file
            content = self.sandbox.fs.read_file(relative_path)
            return f"File content from {file_path}:\n\n{content}"

        except FileNotFoundError:
            return f"Error: File '{file_path}' not found"
        except PermissionError:
            return f"Error: Permission denied reading '{file_path}'"
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"

    def write_file(self, file_path, content):
        """Write file content securely in container"""
        validated_path, error = self._validate_path(file_path)
        if error or not validated_path:
            return error or "Error: Invalid file path"

        if not self.sandbox:
            return self._use_sdk_fallback("write_file")

        try:
            # Check content size (limit to 10MB)
            if len(content.encode("utf-8")) > 10 * 1024 * 1024:
                return "Error: Content too large (max 10MB)"

            # Create directory if needed using local filesystem for validation
            dir_name = os.path.dirname(validated_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)

            # Write file using Daytona SDK
            relative_path = os.path.relpath(validated_path, self.workspace_dir)
            self.sandbox.fs.write_file(relative_path, content)

            return f"Successfully wrote to {file_path}"

        except PermissionError:
            return f"Error: Permission denied writing '{file_path}'"
        except Exception as e:
            return f"Error writing file '{file_path}': {str(e)}"

    def delete_file(self, file_path):
        """Delete file securely in container"""
        validated_path, error = self._validate_path(file_path)
        if error or not validated_path:
            return error or "Error: Invalid file path"

        if not self.sandbox:
            return self._use_sdk_fallback("delete_file")

        try:
            if not os.path.exists(validated_path):
                return f"Error: File '{file_path}' does not exist"

            # Delete file using Daytona SDK
            relative_path = os.path.relpath(validated_path, self.workspace_dir)
            self.sandbox.fs.delete_file(relative_path)

            return f"Successfully deleted {file_path}"

        except Exception as e:
            return f"Error deleting file '{file_path}': {str(e)}"

    def list_files(self, directory_path):
        """List directory contents securely in container"""
        validated_path, error = self._validate_path(directory_path)
        if error or not validated_path:
            return error or "Error: Invalid directory path"

        if not self.sandbox:
            return self._use_sdk_fallback("list_files")

        try:
            if not os.path.exists(validated_path):
                return f"Error: Directory '{directory_path}' does not exist"

            if not os.path.isdir(validated_path):
                return f"Error: '{directory_path}' is not a directory"

            # List files using Daytona SDK
            relative_path = os.path.relpath(validated_path, self.workspace_dir)
            files = self.sandbox.fs.list_files(relative_path)

            if files:
                formatted_files = []
                for file_info in files:
                    file_type = "DIR" if file_info.is_dir else "FILE"
                    formatted_files.append(f"{file_type}: {file_info.name}")

                return f"Contents of {directory_path}:\n\n" + "\n".join(
                    sorted(formatted_files)
                )
            else:
                return f"Contents of {directory_path}:\n\n(empty directory)"

        except PermissionError:
            return f"Error: Permission denied accessing '{directory_path}'"
        except Exception as e:
            return f"Error listing directory '{directory_path}': {str(e)}"

    def get_file_info(self, file_path):
        """Get file information (size, type, permissions)"""
        validated_path, error = self._validate_path(file_path)
        if error or not validated_path:
            return error or "Error: Invalid file path"

        if not self.sandbox:
            return self._use_sdk_fallback("get_file_info")

        try:
            if not os.path.exists(validated_path):
                return f"Error: File '{file_path}' does not exist"

            # Get file info using local stat for now (SDK doesn't have direct file info method)
            stat_info = os.stat(validated_path)
            file_type = "Directory" if os.path.isdir(validated_path) else "File"
            size_mb = stat_info.st_size / (1024 * 1024)

            return f"""File Information for {file_path}:
Type: {file_type}
Size: {size_mb:.2f} MB ({stat_info.st_size} bytes)
Modified: {stat_info.st_mtime}
Permissions: {oct(stat_info.st_mode)[-3:]}"""

        except Exception as e:
            return f"Error getting file info '{file_path}': {str(e)}"


# Global instance
daytona_ops = DaytonaFileOperations()
