gunicorn -w 3 --access-logfile gunicorn.log \
--bind unix:/web/demo.sock blog.wsgi:application
