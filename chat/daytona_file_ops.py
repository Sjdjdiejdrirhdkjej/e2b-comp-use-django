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
    """Secure file operations using Daytona containers via SDK

    If the Daytona SDK or sandbox is unavailable, methods return a helpful
    error string rather than raising, so the UI can show a clear message.
    """

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
        return (
            "Error: Daytona SDK or sandbox not available. "
            "Install with: pip install daytona and set DAYTONA_API_KEY"
        )

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

    def execute_code(self, code: str, language: str = "python"):
        """Execute code inside the Daytona container sandbox.

        Supports Python by writing a temporary file into the workspace and running it.
        If the Daytona SDK doesn't expose an exec interface, returns a clear error.
        """
        if not self.sandbox:
            return self._use_sdk_fallback("execute_code")

        try:
            if language.lower() != "python":
                return f"Error: Unsupported language '{language}'. Only 'python' is supported."

            # Write code to a temp file inside the workspace
            rel_path = "tmp_daytona_exec.py"
            abs_path = os.path.join(self.workspace_dir, rel_path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w", encoding="utf-8") as f:
                f.write(code)

            # Try common execution methods offered by SDKs
            for method_name in ("exec", "execute", "run"):
                method = getattr(self.sandbox, method_name, None)
                if callable(method):
                    try:
                        result = method(["python", rel_path])
                        # Handle string or rich result objects
                        if isinstance(result, str):
                            return f"Execution result (python):\n{result}"
                        stdout = getattr(result, "stdout", "")
                        stderr = getattr(result, "stderr", "")
                        exit_code = getattr(result, "exit_code", 0)
                        output = stdout or ""
                        if stderr:
                            output += ("\n--- stderr ---\n" + stderr)
                        return f"Execution result (exit={exit_code}):\n" + (output or "<no output>")
                    except Exception:
                        continue

            return (
                "Error: Daytona sandbox execution interface not available. "
                "Ensure your SDK version supports command execution."
            )
        except Exception as e:
            return f"Error executing code: {str(e)}"


# Global instance
daytona_ops = DaytonaFileOperations()
