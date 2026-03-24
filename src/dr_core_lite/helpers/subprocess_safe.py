import subprocess

def run_command(cmd, capture_output=True, check=False):
    """
    Executes a shell command safely and returns result.
    """
    try:
        result = subprocess.run(
            cmd,
            shell=False if isinstance(cmd, list) else True,
            capture_output=capture_output,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"[!] Command failed: {cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Output: {e.output}")
        return None
