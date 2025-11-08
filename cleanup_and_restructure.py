#!/usr/bin/env python3
"""
Project Cleanup and Restructure Script
Reorganizes the Student Loan Document Extractor Platform for clarity
"""

import os
import shutil
from pathlib import Path
import sys

# Directories to remove completely
DIRS_TO_REMOVE = [
    "Lab3",
    "frontend", 
    "LoanQA-Integration",
    "Lib",
    "Scripts",
    "extraction",
    "ocr",
    "__pycache__",
    ".pytest_cache",
    "temp"
]

# Documentation files to archive
DOCS_TO_ARCHIVE = [
    "ADVANCED_FEATURES_IMPLEMENTATION.md",
    "AIRFLOW_EXPLORATION_GUIDE.md",
    "AIRFLOW_MLOPS_GUIDE.md",
    "API_INTEGRATION_GUIDE.md",
    "CLEANUP_COMPLETE.md",
    "CLEANUP_PLAN.md",
    "CLEANUP_SUMMARY.md",
    "CODE_QUALITY_REVIEW.md",
    "COMPARISON_ENGINE_IMPLEMENTATION.md",
    "DEPLOYMENT_SUMMARY.md",
    "FEATURE_ROADMAP.md",
    "FEATURES_COMPLETE.md",
    "FINAL_INTEGRATION_STATUS.md",
    "IMPLEMENTATION_COMPLETE_FINAL.md",
    "IMPLEMENTATION_SUMMARY.md",
    "INTEGRATION_ANALYSIS.md",
    "INTEGRATION_COMPLETE.md",
    "INTEGRATION_GUIDE.md",
    "INTEGRATION_SUCCESS.md",
    "MLOPS_COMPLETE_REPORT.md",
    "MLOPS_IMPLEMENTATION_STATUS.md",
    "MLOPS_PHASE1_README.md",
    "MLOPS_PIPELINE_IMPLEMENTATION_PLAN.md",
    "MLOPS_PROJECT_REPORT.md",
    "PROJECT_RESTRUCTURE_PLAN.md",
    "PROJECT_STRUCTURE.md",
    "QUICKSTART.md",  # Keep QUICK_START.md
    "RATE_LIMIT_EXPLAINED.md",
    "SYSTEM_VERIFICATION.md",
    "WHY_DOCKER.md",
    "LOANQA_MLOPS_RESEARCH.md"
]

# Files to keep in root
ROOT_FILES_TO_KEEP = [
    "README.md",
    "CONTRIBUTING.md",
    "DEPLOYMENT.md",
    "DEPLOYMENT_AWS.md",
    "DEPLOYMENT_GCP.md",
    "DOCKER_QUICKSTART.md",
    "DOCKER_README.md",
    "QUICK_START.md",
    "LICENSE",
    "requirements.txt",
    "pyproject.toml",
    "docker-compose.yml",
    "Dockerfile",
    ".env.example",
    ".gitignore",
    ".dockerignore",
    ".dvcignore",
    "dvc.yaml",
    "Makefile"
]


def create_backup():
    """Create backup before cleanup"""
    print("📦 Creating backup...")
    backup_dir = Path("../Lab3_backup_" + str(int(time.time())))
    
    try:
        shutil.copytree(".", backup_dir, ignore=shutil.ignore_patterns('.git', '__pycache__', 'node_modules'))
        print(f"✅ Backup created: {backup_dir}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False


def remove_directories():
    """Remove redundant directories"""
    print("\n🗑️ Removing redundant directories...")
    
    for dir_name in DIRS_TO_REMOVE:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            try:
                shutil.rmtree(dir_path)
                print(f"  ✅ Removed: {dir_name}")
            except Exception as e:
                print(f"  ❌ Failed to remove {dir_name}: {e}")


def archive_documentation():
    """Archive old documentation files"""
    print("\n📚 Archiving old documentation...")
    
    archive_dir = Path("docs/archive")
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    for doc_file in DOCS_TO_ARCHIVE:
        doc_path = Path(doc_file)
        if doc_path.exists() and doc_path.is_file():
            try:
                shutil.move(str(doc_path), str(archive_dir / doc_file))
                print(f"  ✅ Archived: {doc_file}")
            except Exception as e:
                print(f"  ❌ Failed to archive {doc_file}: {e}")


def create_docs_structure():
    """Create organized docs directory"""
    print("\n📁 Creating docs structure...")
    
    docs_dirs = [
        "docs/api",
        "docs/deployment",
        "docs/architecture",
        "docs/user-guide",
        "docs/archive"
    ]
    
    for dir_path in docs_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"  ✅ Created: {dir_path}")
    
    # Move deployment docs
    deployment_docs = ["DEPLOYMENT_AWS.md", "DEPLOYMENT_GCP.md", "DOCKER_QUICKSTART.md", "DOCKER_README.md"]
    for doc in deployment_docs:
        if Path(doc).exists():
            shutil.move(doc, f"docs/deployment/{doc}")
            print(f"  ✅ Moved {doc} to docs/deployment/")


def create_src_structure():
    """Create src directory and move core modules"""
    print("\n📦 Creating src structure...")
    
    src_dir = Path("src")
    src_dir.mkdir(exist_ok=True)
    
    # Modules to move to src/
    modules = ["api", "dashboard", "processing", "normalization", "storage", "mlops"]
    
    for module in modules:
        module_path = Path(module)
        if module_path.exists() and module_path.is_dir():
            target = src_dir / module
            if not target.exists():
                try:
                    shutil.move(str(module_path), str(target))
                    print(f"  ✅ Moved {module} to src/")
                except Exception as e:
                    print(f"  ❌ Failed to move {module}: {e}")


def update_import_paths():
    """Update import paths in Python files"""
    print("\n🔧 Updating import paths...")
    
    # This would require parsing and updating all Python files
    # For now, just log that it needs to be done
    print("  ⚠️ Manual step: Update imports from 'api.' to 'src.api.'")
    print("  ⚠️ Manual step: Update imports from 'processing.' to 'src.processing.'")
    print("  ⚠️ Manual step: Update imports from 'storage.' to 'src.storage.'")


def cleanup_pycache():
    """Remove all __pycache__ directories"""
    print("\n🧹 Cleaning __pycache__ directories...")
    
    for root, dirs, files in os.walk("."):
        if "__pycache__" in dirs:
            pycache_path = Path(root) / "__pycache__"
            try:
                shutil.rmtree(pycache_path)
                print(f"  ✅ Removed: {pycache_path}")
            except Exception as e:
                print(f"  ❌ Failed: {e}")


def main():
    """Main cleanup execution"""
    print("=" * 60)
    print("🚀 Student Loan Document Extractor - Project Cleanup")
    print("=" * 60)
    
    # Confirm with user
    print("\n⚠️ This will restructure the project and remove redundant files.")
    print("A backup will be created before proceeding.")
    
    response = input("\nProceed with cleanup? (yes/no): ")
    if response.lower() != "yes":
        print("❌ Cleanup cancelled")
        return
    
    # Execute cleanup steps
    import time
    
    # Step 1: Backup
    if not create_backup():
        print("❌ Backup failed - aborting cleanup")
        return
    
    # Step 2: Remove redundant directories
    remove_directories()
    
    # Step 3: Archive old documentation
    archive_documentation()
    
    # Step 4: Create new structure
    create_docs_structure()
    
    # Step 5: Cleanup cache
    cleanup_pycache()
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("✅ Cleanup Complete!")
    print("=" * 60)
    print("\n📋 Next Steps:")
    print("1. Review the changes")
    print("2. Update import paths in Python files")
    print("3. Run tests: pytest tests/")
    print("4. Update docker-compose.yml paths")
    print("5. Commit changes")
    print("\n⚠️ Note: Some manual updates may be required")


if __name__ == "__main__":
    main()
