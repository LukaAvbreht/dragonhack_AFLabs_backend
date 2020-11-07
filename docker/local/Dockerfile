FROM python:3.7
RUN apt-get clean && apt-get update && \
    apt-get install -y --no-install-recommends \
           postgresql-client-common \
           postgresql-client \
           netcat-traditional

WORKDIR /app
COPY config/requirements /app/config/requirements
RUN pip install -r config/requirements/local.txt --src=/pip-repos

COPY . /app

EXPOSE 8000
CMD ["/app/docker/local/entrypoint.sh"]
