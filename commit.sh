echo "Commit message: " $1

git add -A
git reset run.py
git commit -m "$1"
git status
git push