FROM python:3.10-slim

WORKDIR /usr/src/app
ENV DAGSTER_HOME=/usr/src/app

COPY . /usr/src/app

RUN pip install --no-cache -r requirements.txt

EXPOSE 3000

CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]