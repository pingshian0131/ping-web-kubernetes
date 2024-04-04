# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the app user
RUN adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/ping-web
ENV STATIC=/var/www/personal/static
ENV MEDIA=/var/www/personal/media
RUN mkdir $HOME \
    && mkdir -p $MEDIA \
    && mkdir -p $STATIC \
    && mkdir $APP_HOME \
    && mkdir -p $APP_HOME/media/portfolio
WORKDIR $APP_HOME

COPY ./requirements.txt .

RUN python -m pip install --upgrade pip  \
    && pip install -r $APP_HOME/requirements.txt

# install psycopg2 dependencies
RUN apt-get update \
   && apt-get -y install libpq-dev gcc netcat-traditional redis-server cron vim

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME \
  && chown -R app:app $STATIC \
  && chown -R app:app $MEDIA

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/ping-web/entrypoint.sh"]

# change to root user
USER root

EXPOSE 8001

CMD ["gunicorn", "--log-level=warning", "--bind", "0.0.0.0:8001", "mysite.asgi:application", "-w", "4", "-k", "uvicorn.workers.UvicornWorker"]

