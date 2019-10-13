FROM zengzhengrong889/ubuntu:2019919
MAINTAINER zengzhengrong
ENV PYTHONUNBUFFERED 1

# COPY sources.list /etc/apt/sources.list
WORKDIR /web
COPY . /web

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
RUN rm /etc/nginx/sites-enabled/*

COPY django_nginx.conf /etc/nginx/sites-enabled/
RUN python3 manage.py collectstatic

# RUN python3 manage.py migrate
# RUN python3 -m populate.all 
    # service nginx start \

ENTRYPOINT [ "django-command.sh" ]
