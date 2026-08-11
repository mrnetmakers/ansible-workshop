# Publish This Workshop to GitHub

This package intentionally does not contain a `.git` directory. After unpacking it, create a new empty GitHub repository and push this directory as its initial content.

## 1. Unpack

For the `.tar.gz` package:

```bash
tar -xzf ansible-deep-dive-workshop.tar.gz
cd ansible-deep-dive-workshop
```

Or for the ZIP package:

```bash
unzip ansible-deep-dive-workshop.zip
cd ansible-deep-dive-workshop
```

## 2. Initialize Git

```bash
git init
git branch -M main
git add .
git commit -m "Initial Ansible deep-dive workshop"
```

## 3. Create an empty repository on GitHub

Create a repository in the GitHub web interface. Do not add a README, `.gitignore`, or license there because they already exist in this package.

## 4. Connect and push

Use the repository URL GitHub gives you:

```bash
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git push -u origin main
```

## 5. Student workflow

Students can then run:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL> ~/ansible-workshop
cd ~/ansible-workshop
```

They should begin with section **0. Get the workshop repository** in `README.md`.

## Optional: GitHub template repository

For repeated classes, mark the GitHub repository as a template repository. This makes it easy to create a fresh copy for each class or student while preserving the original workshop material.
