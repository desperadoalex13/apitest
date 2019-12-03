FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install gettext cron -y
COPY apitest/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN groupadd django && useradd -m -g django -s /bin/bash django && \
    mkdir /home/django/app
RUN LANG=en_US.UTF-8 && LC_ALL=en_US.UTF-8

WORKDIR /home/django/
ADD apitest app/
COPY .env /tmp/

RUN bash -c 'python app/manage.py collectstatic <<<yes \
    && python app/manage.py makemessages --all -e py,html,jinja'

