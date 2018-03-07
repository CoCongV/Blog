FROM python:3.6.4-alpine3.7
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
ENV PYTHON_VERSION 3.6.4
RUN mkdir /Flask_Blog
WORKDIR /Flask_Blog
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./ /Flask_Blog/
EXPOSE 8080
CMD ["gunicorn", "-c", "deploy_config.py", "manage:app"]

