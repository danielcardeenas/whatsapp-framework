echo "Commit message: " $1

git rm --cached commit.sh
git rm --cached add.sh
git add -A
git reset config.py
git reset modules/wolfram/config.py

git commit -m "$1"