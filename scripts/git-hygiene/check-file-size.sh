#!/bin/bash

# ========================================
# Git Hygiene - File Size Checker
# ========================================
# This script checks file sizes and prevents
# large files (>100MB) from being committed or pushed.
#
# Usage: check-file-size.sh <file-list> <max-size-mb>
# Returns: 0 if all files are OK, 1 if any file is too large
# ========================================

set -e

# Default maximum file size in MB
DEFAULT_MAX_SIZE=100

# Function to display usage information
usage() {
    echo "Usage: $0 <file-list> [max-size-mb]"
    echo "  file-list: Space-separated list of files to check"
    echo "  max-size-mb: Maximum file size in MB (default: $DEFAULT_MAX_SIZE)"
    echo ""
    echo "Example: $0 \"file1.txt file2.jpg\" 50"
    exit 1
}

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    usage
fi

# Get file list and max size
FILE_LIST="$1"
MAX_SIZE_MB="${2:-$DEFAULT_MAX_SIZE}"

# Validate max size is a number
if ! [[ "$MAX_SIZE_MB" =~ ^[0-9]+$ ]]; then
    echo "Error: max-size-mb must be a valid number"
    usage
fi

# Initialize variables
LARGE_FILES=()
EXIT_CODE=0

echo "🔍 Checking file sizes (max: ${MAX_SIZE_MB}MB)..."

# Check each file
for file in $FILE_LIST; do
    if [ -f "$file" ]; then
        # Get file size in bytes
        FILE_SIZE_BYTES=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null || echo "0")

        # Convert to MB
        FILE_SIZE_MB=$(( FILE_SIZE_BYTES / 1024 / 1024 ))

        echo "  📄 $file: ${FILE_SIZE_MB}MB"

        # Check if file is too large
        if [ "$FILE_SIZE_MB" -gt "$MAX_SIZE_MB" ]; then
            LARGE_FILES+=("$file (${FILE_SIZE_MB}MB)")
            EXIT_CODE=1
        fi
    else
        echo "  ⚠️  $file: File not found"
    fi
done

# Report results
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ All files are within size limits"
else
    echo ""
    echo "❌ The following files exceed the ${MAX_SIZE_MB}MB limit:"
    for large_file in "${LARGE_FILES[@]}"; do
        echo "  🚫 $large_file"
    done
    echo ""
    echo "💡 To fix this:"
    echo "  1. Remove large files from commit: git rm --cached <file>"
    echo "  2. Or use Git LFS: git lfs track <file>"
    echo "  3. Or increase the limit in the hook configuration"
fi

exit $EXIT_CODE
