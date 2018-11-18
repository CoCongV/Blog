FROM python:3.6.7-alpine3.8
RUN apk update && \
    apk add --no-cache --virtual build-deps gcc python-dev musl-dev && \
    apk --no-cache add postgresql-dev \
                       jpeg-dev \
                       zlib-dev \
                       freetype-dev \
                       lcms2-dev \
                       openjpeg-dev \
                       tiff-dev \
                       tk-dev \
                       tcl-dev \
                       harfbuzz-dev \
                       fribidi-dev
ENV PYTHON_VERSION 3.6.7
RUN mkdir /Blog
WORKDIR /Blog
ADD ./ /Blog/
RUN pip --no-cache-dir install .
EXPOSE 8080
CMD ["gunicorn", "--log-level", "error", "-w", "2", "-k", "gevent", "blog.manage:app", "-b", "localhost:8080"]
