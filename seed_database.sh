rm db.sqlite3
rm -rf ./spacemonkeyapi/migrations
python3 manage.py makemigrations spacemonkeyapi
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata rareuser
python3 manage.py loaddata tokens
python3 manage.py loaddata categories
python3 manage.py loaddata posts
python3 manage.py loaddata tags
python3 manage.py loaddata comments
