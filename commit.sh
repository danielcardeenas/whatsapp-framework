echo "Commit message: " $1

git add -A
git reset ~/workspace/run.py
git commit -m "$1"
git status
git push