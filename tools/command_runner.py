import subprocess

def run_command(cmd):
    """
    Run a shell command and show its output and errors.
    """
    try:
        print(f"\n⚙️ Running command: {cmd}\n")
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        print("🟢 Output:\n", result.stdout)
        if result.stderr:
            print("🔴 Errors:\n", result.stderr)
    except Exception as e:
        print("❌ Command execution failed:", str(e))
