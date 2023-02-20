FROM python:3.9-slim

EXPOSE 8001

WORKDIR /app

# Install dependencies
RUN set -x; \
        apt-get update \
        && apt-get install -y --no-install-recommends \
            curl \
            dirmngr \
            git \
            libpq-dev \
            python-dev \
            gcc-aarch64-linux-gnu \
            g++ \
            locales

ENV TZ=Asia/Bangkok
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1
ENV FLASK_DEBUG 1
ENV DB_HOST generator_postgres
ENV DB_PORT 5432
ENV DB_NAME benerator
ENV DB_USER benerator
ENV DB_PASSWORD benerator

#CMD [ "gunicorn", "--timeout", "3000", "--bind", "0.0.0.0:8001", "main:run()" ]
