FROM zengzhengrong889/ubuntu:2019919
MAINTAINER zengzhengrong
ENV PYTHONUNBUFFERED 1

WORKDIR /web
COPY . /web

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple gunicorn
RUN rm /etc/nginx/sites-enabled/*

COPY django_nginx.conf /etc/nginx/sites-enabled/
RUN python3 manage.py collectstatic


ENTRYPOINT ["./wait-for-it.sh","-h","db","-p","5432","-s","--","./django-command.sh"]
