FROM python:3.5.3-slim
RUN apt-get update -qq && apt-get install -y build-essential libgmp-dev libpq-dev
ENV PYTHON_VERSION 3.5.3
RUN mkdir /Flask_Blog
WORKDIR /Flask_Blog
ADD ./requirements.txt .
RUN pip install -r requirements.txt
ADD ./ /Flask_Blog/
EXPOSE 8080
CMD ["gunicorn", "-c", "deploy_config.py", "manage:app"]

