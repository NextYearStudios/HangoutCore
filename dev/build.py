import os
import re
import subprocess
import sys

from setuptools_scm import get_version


def run_command(command, check=True, capture_output=False):
    """Run a shell command."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(
        command,
        check=check,
        capture_output=capture_output,
        text=True,
        cwd=os.getcwd(),
        # encoding="UTF-8",
        env=os.environ.copy(),
    )
    if capture_output:
        return result.stdout.strip()
    return None


def get_package_version():
    """Get the current version from setuptools-scm."""
    print("Fetching version from setuptools-scm...")
    version = get_version()
    print(f"Version detected: {version}")
    return version


def sanitize_version(version):
    """
    Simplify the version string by removing metadata.
    Example: '4.0.4.dev0+ge13f316.d20241222' -> '4.0.4.dev'
    """
    match = re.match(r"(\d+\.\d+\.\d+)(\.dev\d+)?", version)
    if match:
        return f"{match.group(1)}{match.group(2) or ''}"
    return version


def create_and_push_tag(version):
    """Create and push a Git tag."""
    sanitized_version = sanitize_version(version)
    tag = f"{sanitized_version}"
    print(f"Creating and pushing Git tag: v{tag}")
    run_command(["git", "tag", "-a", f"v{tag}", "-m", f"Version {tag}"])
    run_command(["git", "push", "origin", f"v{tag}"])


def clean_build_artifacts():
    """Remove old build artifacts."""
    print("Cleaning previous build artifacts...")
    for folder in ["build", "dist", "*.egg-info"]:
        if os.path.exists(folder):
            try:
                os.remove(folder)
                print(f"File '{folder}' has been removed successfully.")
            except FileNotFoundError:
                print(f"File '{folder}' not found.")
            except PermissionError:
                print(f"You don't have permission to delete '{folder}'.")
            except Exception as e:
                print(f"An error occurred: {e}")


def format_files():
    print("Formatting...")
    run_command(["black", os.getcwd()])

    print("Sorting...")
    run_command(["isort", ".", "--skip", "hangoutcore_venv"])


def build_package():
    """Build the package."""
    print("Building the package...")
    run_command([f"{sys.executable}", "-m", "build"])


def main():
    try:
        # Get the package version
        version = get_package_version()

        # Clean old artifacts
        # clean_build_artifacts()

        # Build the package
        build_package()

        # Format and sort files
        format_files()

        # Create and push Git tag
        # create_and_push_tag(version)

        print("\n🎉 Build and tag completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
