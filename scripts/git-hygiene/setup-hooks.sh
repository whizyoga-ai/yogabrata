#!/bin/bash

# ========================================
# Git Hygiene - Hook Setup Script
# ========================================
# This script installs and configures Git hooks
# for preventing large file commits and pushes.
#
# Features:
# - Makes hook scripts executable
# - Validates hook installation
# - Provides feedback on setup status
# - Works across different platforms
# ========================================

set -e

# Configuration
HOOKS_DIR=".git/hooks"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
HOOK_SOURCE_DIR="$PROJECT_ROOT/scripts/git-hygiene"
MAX_FILE_SIZE_MB="${GIT_HYGIENE_MAX_SIZE:-100}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    local color=$1
    local icon=$2
    local message=$3
    echo -e "${color}${icon} ${message}${NC}"
}

print_header() {
    local color=$1
    local message=$2
    echo -e "${color}${BOLD}${message}${NC}"
}

# Function to check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_status $RED "❌" "Error: Not in a Git repository"
        echo "Please run this script from the root of your Git repository."
        exit 1
    fi
}

# Function to make scripts executable
make_executable() {
    local script_path="$1"
    if [ -f "$script_path" ]; then
        if [ ! -x "$script_path" ]; then
            print_status $BLUE "🔧" "Making $script_path executable..."
            chmod +x "$script_path"
        else
            print_status $GREEN "✅" "$script_path is already executable"
        fi
    else
        print_status $RED "❌" "Error: $script_path not found"
        return 1
    fi
}

# Function to install a hook
install_hook() {
    local hook_name="$1"
    local source_path="$HOOK_SOURCE_DIR/$hook_name"
    local target_path="$HOOKS_DIR/$hook_name"

    if [ -f "$source_path" ]; then
        # Create symlink or copy if symlink not supported
        if ln -sf "$source_path" "$target_path" 2>/dev/null; then
            print_status $GREEN "✅" "Installed $hook_name hook (symlink)"
        elif cp "$source_path" "$target_path" 2>/dev/null; then
            print_status $GREEN "✅" "Installed $hook_name hook (copy)"
        else
            print_status $RED "❌" "Failed to install $hook_name hook"
            return 1
        fi
    else
        print_status $YELLOW "⚠️" "Warning: $source_path not found - skipping $hook_name"
    fi
}

# Function to validate hook installation
validate_hooks() {
    local hooks_valid=true

    for hook in "pre-commit" "pre-push"; do
        local hook_path="$HOOKS_DIR/$hook"
        if [ -f "$hook_path" ]; then
            if [ -x "$hook_path" ]; then
                print_status $GREEN "✅" "$hook is properly installed and executable"
            else
                print_status $YELLOW "⚠️" "$hook exists but is not executable"
                print_status $BLUE "🔧" "Making $hook executable..."
                chmod +x "$hook_path"
                print_status $GREEN "✅" "$hook is now executable"
            fi
        else
            print_status $RED "❌" "$hook is not installed"
            hooks_valid=false
        fi
    done

    return $([ "$hooks_valid" = true ] && echo 0 || echo 1)
}

# Main execution
main() {
    print_header $BLUE "🚀 Git Hygiene Setup"
    echo "=================================="

    # Check if we're in a git repository
    check_git_repo

    print_status $BLUE "📁" "Project root: $PROJECT_ROOT"
    print_status $BLUE "📁" "Hooks directory: $HOOKS_DIR"
    print_status $BLUE "📁" "Source directory: $HOOK_SOURCE_DIR"
    print_status $BLUE "📏" "Max file size limit: ${MAX_FILE_SIZE_MB}MB"
    echo ""

    # Make scripts executable
    print_header $YELLOW "🔧 Making scripts executable..."
    make_executable "$HOOK_SOURCE_DIR/check-file-size.sh"

    # Install hooks
    print_header $YELLOW "📦 Installing Git hooks..."
    install_hook "pre-commit"
    install_hook "pre-push"

    # Validate installation
    print_header $YELLOW "🔍 Validating installation..."
    if validate_hooks; then
        print_header $GREEN "🎉 Setup completed successfully!"
        echo ""
        print_status $GREEN "✅" "Git hygiene hooks are now active"
        print_status $BLUE "ℹ️" "Hooks will prevent commits/pushes of files larger than ${MAX_FILE_SIZE_MB}MB"
        echo ""
        echo "📋 What was installed:"
        echo "  • .git/hooks/pre-commit - Blocks large files before commit"
        echo "  • .git/hooks/pre-push - Blocks large files before push"
        echo "  • scripts/git-hygiene/check-file-size.sh - Reusable size checker"
        echo ""
        echo "💡 Tips:"
        echo "  • Use 'git lfs track <file>' for large files you need to keep"
        echo "  • Set GIT_HYGIENE_MAX_SIZE environment variable to change the limit"
        echo "  • Run this script again to update hooks after pulling changes"
    else
        print_header $RED "❌ Setup completed with errors"
        echo ""
        print_status $YELLOW "⚠️" "Some hooks may not be working properly"
        print_status $BLUE "💡" "Try running this script again or check file permissions"
        exit 1
    fi
}

# Run the main function
main "$@"
