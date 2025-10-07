# Git Hygiene Setup

A comprehensive Git hygiene system that prevents large files from being committed or pushed to GitHub. This setup provides multiple layers of protection to maintain repository health and performance.

## 🚀 Quick Start

1. **Install the hooks:**
   ```bash
   ./scripts/git-hygiene/setup-hooks.sh
   ```

2. **Verify installation:**
   ```bash
   ls -la .git/hooks/pre-commit .git/hooks/pre-push
   ```

3. **Test with a large file:**
   ```bash
   echo "Creating large test file..."
   dd if=/dev/zero of=test-large-file.txt bs=1M count=150
   git add test-large-file.txt
   git commit -m "Test large file"
   ```

## 📋 What's Included

### Core Components

- **`.gitignore`** - Comprehensive file exclusions for modern web/backend projects
- **`.gitattributes`** - Git LFS configuration for large file types
- **`scripts/git-hygiene/check-file-size.sh`** - Reusable file size checker
- **`.git/hooks/pre-commit`** - Blocks large files before commit
- **`.git/hooks/pre-push`** - Blocks large files before push
- **`scripts/git-hygiene/setup-hooks.sh`** - Automated hook installation
- **`.github/workflows/check-large-files.yml`** - CI/CD size validation

### Protection Layers

1. **Development** - Pre-commit hooks catch issues locally
2. **Team Integration** - Pre-push hooks prevent force-pushing large files
3. **CI/CD** - GitHub Actions ensure no large files enter main branches
4. **Automation** - Git LFS handles legitimate large files transparently

## ⚙️ Configuration

### File Size Limit

The default limit is **100MB**. Customize it by setting an environment variable:

```bash
# For current session
export GIT_HYGIENE_MAX_SIZE=50

# For specific command
GIT_HYGIENE_MAX_SIZE=200 git commit -m "Large file commit"

# In your shell profile (permanent)
echo 'export GIT_HYGIENE_MAX_SIZE=50' >> ~/.bashrc
```

### Git LFS Integration

The setup includes comprehensive Git LFS patterns in `.gitattributes`. To use:

1. **Install Git LFS:**
   ```bash
   # Ubuntu/Debian
   curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
   sudo apt-get install git-lfs

   # macOS
   brew install git-lfs

   # Windows (via Chocolatey)
   choco install git-lfs
   ```

2. **Initialize in your repository:**
   ```bash
   git lfs install
   ```

3. **Track file types or specific files:**
   ```bash
   # Track all PSD files
   git lfs track "*.psd"

   # Track specific file
   git lfs track "assets/large-video.mp4"
   ```

## 🔧 Manual Installation

If you prefer manual setup:

```bash
# Make scripts executable
chmod +x scripts/git-hygiene/check-file-size.sh
chmod +x scripts/git-hygiene/setup-hooks.sh

# Copy hooks to .git/hooks/
cp scripts/git-hygiene/pre-commit .git/hooks/
cp scripts/git-hygiene/pre-push .git/hooks/

# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

## 🚨 Troubleshooting

### Hooks Not Working

1. **Check if hooks are executable:**
   ```bash
   ls -la .git/hooks/pre-commit .git/hooks/pre-push
   ```

2. **Reinstall hooks:**
   ```bash
   ./scripts/git-hygiene/setup-hooks.sh
   ```

3. **Check for existing hooks:**
   ```bash
   # Backup existing hooks
   mv .git/hooks/pre-commit .git/hooks/pre-commit.backup
   mv .git/hooks/pre-push .git/hooks/pre-push.backup
   ```

### Large Files Already Committed

1. **Remove from Git history:**
   ```bash
   git rm --cached path/to/large-file.mp4
   git commit -m "Remove large file"
   ```

2. **Use Git LFS for existing files:**
   ```bash
   git lfs track "*.mp4"
   git add .gitattributes
   git add path/to/large-file.mp4
   git commit -m "Track large files with LFS"
   ```

3. **Clean repository history:**
   ```bash
   # Remove large files from all history (destructive!)
   git filter-branch --tree-filter 'git lfs track "*.mp4"' HEAD
   ```

### CI/CD Failures

1. **Check workflow logs** in GitHub Actions
2. **Verify file sizes** locally before pushing
3. **Use Git LFS** for legitimate large files
4. **Review `.gitignore`** patterns

## 📊 Monitoring

### Check Repository Health

```bash
# Find large files in repository
find . -type f -not -path "./.git/*" -exec du -h {} + | sort -hr | head -20

# Check Git LFS status
git lfs ls-files

# Verify hook installation
./scripts/git-hygiene/setup-hooks.sh --validate
```

### GitHub Repository Settings

1. **Enable Git LFS** in repository settings
2. **Set branch protection** rules
3. **Configure required status checks** for the "Check Large Files" workflow

## 🔄 Updates

To update the Git hygiene setup:

```bash
# Pull latest changes
git pull origin main

# Reinstall hooks (updates existing ones)
./scripts/git-hygiene/setup-hooks.sh

# Verify everything works
git add . && git commit -m "Update Git hygiene setup"
```

## 🤝 Contributing

To improve this setup:

1. **Test changes** in a separate repository first
2. **Update documentation** for any new features
3. **Consider backward compatibility**
4. **Add tests** for new functionality

## 📝 License

This Git hygiene setup is provided as-is for maintaining repository health. Feel free to customize and adapt for your specific needs.

---

**Happy coding with clean repositories! 🧹✨**
