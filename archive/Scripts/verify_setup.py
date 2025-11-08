"""
Verification script to check if all dependencies and setup are correct
"""

import sys
import os


def check_python_version():
    """Check if Python version meets requirements"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"✗ Python version {version.major}.{version.minor}.{version.micro} is too old. Need 3.10+")
        return False


def check_module(module_name, package_name=None):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name or module_name} is NOT installed")
        return False


def check_directories():
    """Check if required directories exist"""
    required_dirs = ['ocr', 'extraction', 'normalization', 'storage', 'api', 'dashboard']
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"✗ Directory '{dir_name}' is missing")
            all_exist = False
    
    return all_exist


def check_config_files():
    """Check if configuration files exist"""
    config_files = ['requirements.txt', 'pyproject.toml', 'Dockerfile', 'docker-compose.yml', '.env.example']
    all_exist = True
    
    for file_name in config_files:
        if os.path.isfile(file_name):
            print(f"✓ Config file '{file_name}' exists")
        else:
            print(f"✗ Config file '{file_name}' is missing")
            all_exist = False
    
    return all_exist


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Student Loan Document Extractor - Setup Verification")
    print("=" * 60)
    print()
    
    print("Checking Python version...")
    python_ok = check_python_version()
    print()
    
    print("Checking project structure...")
    dirs_ok = check_directories()
    print()
    
    print("Checking configuration files...")
    config_ok = check_config_files()
    print()
    
    print("Checking core dependencies...")
    deps_ok = True
    deps_ok &= check_module('pydantic')
    deps_ok &= check_module('fastapi')
    deps_ok &= check_module('streamlit')
    deps_ok &= check_module('PIL', 'Pillow')
    deps_ok &= check_module('pdfplumber')
    print()
    
    print("=" * 60)
    if python_ok and dirs_ok and config_ok:
        print("✓ Project structure setup is COMPLETE")
        if deps_ok:
            print("✓ All core dependencies are installed")
        else:
            print("⚠ Some dependencies are missing. Run: pip install -r requirements.txt")
    else:
        print("✗ Setup is INCOMPLETE. Please review the errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
