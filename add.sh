echo "Commit message: " $1

git rm --cached commit.sh
git rm --cached add.sh
git add -A
git reset config.py
git reset modules/wolfram/config.py

# Modules
git rm --cached -r modules/broadcast
git rm --cached -r modules/wolfram
git rm --cached -r modules/yesno
git rm --cached -r modules/poker
git rm --cached -r modules/poll2

git commit -m "$1"