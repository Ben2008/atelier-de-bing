#!/bin/bash

# Initialize local repository
git init

# Stage all project files
git add .

# Commit changes
git commit -m "Initial commit with FastAPI setup"

# Rename branch to main
git branch -M main

# Link and push to your existing GitHub repository
git remote add origin https://github.com/Ben2008
git push -u origin main
