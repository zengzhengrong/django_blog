#!/bin/sh

echo "start nginx"
service nginx start
echo "chmod sock file"
chmod 755 ./demo.sock
echo "makte migrate"
python3 manage.py migrate
echo "populating data"
python3 -m populate.all
echo "run gunicorn"
gunicorn -w 3 --access-logfile gunicorn.log --bind unix:/web/demo.sock blog.wsgi:application



