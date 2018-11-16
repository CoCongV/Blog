FROM python:3.6.7-alpine3.8
RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev
ENV PYTHON_VERSION 3.6.7
RUN mkdir /Flask_Blog
WORKDIR /Flask_Blog
RUN pip install .
ADD ./ /Flask_Blog/
EXPOSE 8080
CMD ["gunicorn", "--log-level", "error", "-w", "2", "-k", "gevent", "blog.manage:app", "-b", "localhost:8080"]
