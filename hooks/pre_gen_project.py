#!/usr/bin/env python3

"""
Pre-generation hook for cookiecutter-rbfx.

This hook validates user inputs before generating the project.
"""

import re
import sys

# Access the cookiecutter context (populated by Jinja2 during rendering)
project_slug = "{{ cookiecutter.project_slug }}"


def validate_project_slug(slug):
    """Validate that project_slug is a proper identifier, not a path."""
    # Check for path separators
    if any(char in slug for char in ['/', '\\', ':']):
        return False, "project_slug cannot contain path separators (/, \\, :). Use a simple identifier like 'my-game' or 'awesome-project'."
    
    # Check for empty string
    if not slug:
        return False, "project_slug cannot be empty."
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    if not re.match(r'^[a-zA-Z0-9_-]+$', slug):
        return False, "project_slug can only contain letters, numbers, hyphens, and underscores."
    
    # Check for reasonable length
    if len(slug) > 50:
        return False, "project_slug must be 50 characters or less."
    
    return True, ""


def main():
    """Main validation function."""
    is_valid, error_message = validate_project_slug(project_slug)
    
    if not is_valid:
        print(f"ERROR: Invalid project_slug '{project_slug}': {error_message}")
        print("")
        print("Examples of valid project_slug values:")
        print("  sample-project")
        print("  my-awesome-game")
        print("  space_shooter")
        print("  Project123")
        print("")
        print("Examples of INVALID project_slug values:")
        print("  C:\\Folder\\Name    (contains path separators)")
        print("  /home/user/Name    (contains path separators)")
        print("  ../other-project   (contains path separators)")
        print("  my project         (contains spaces - use hyphens instead)")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
