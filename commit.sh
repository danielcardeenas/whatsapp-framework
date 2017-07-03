echo "Commit message: " $1

git add -A
git reset config.py
git reset commit.sh
git commit -m "$1"
git status
git push