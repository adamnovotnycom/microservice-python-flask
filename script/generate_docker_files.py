# collect all secrets from instance folders (not committed to git), 
# and generate all necessary files containing secrets.
# Example: docker-compose with environmental variables
import argparse
import configparser
import os
import subprocess

def main(mode):
    # secrets
    # postgres_db, postgres_user, postgres_password = load_secrets(mode)
    delete_dockerfile("Dockerfile")
    delete_dockerfile("Dockerfile.test")
    delete_dockerfile("Dockerfile.web")
    generate_docker_compose(mode=mode)
    generate_dockerfile(mode=mode, web=False, sut=False)
    generate_dockerfile(mode=mode, web=True, sut=False)
    generate_dockerfile(mode=mode, web=False, sut=True)

def load_secrets(mode):
    # load secrets
    CONFIG = configparser.ConfigParser()
    CONFIG.read(os.path.abspath(os.path.join(os.curdir, 
        "forecast_service", "forecast_service", "instance", "secrets.ini")))
    postgres_db = CONFIG[mode]["POSTGRES_DB"]
    postgres_user = CONFIG[mode]["POSTGRES_USER"]
    postgres_password = CONFIG[mode]["POSTGRES_PASSWORD"]
    return postgres_db, postgres_user, postgres_password

def generate_docker_compose(mode):
    filename = 'docker-compose.yml'
    destination_dir = os.path.join(os.path.abspath(os.curdir))
    
    # Before creating files, check that the destination directory exists
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)

    file_text = (
"""version: '3'
services:
  forecast_service:
    container_name: forecast_service
    image: projecttrust_forecastservice
    restart: always
    build:
      context: ./forecast_service
      dockerfile: Dockerfile
    environment:
      APP_MODE: {0}
      APP_VERSION: 0.1.0
    volumes:
      - ./forecast_service:/mnt/app
    stdin_open: true
    tty: true
    ports:
      - "5002:5000"
  sut_fs:
    container_name: sut_fs
    image: projecttrust_forecastservice_sut
    restart: always
    build:
      context: ./forecast_service
      dockerfile: Dockerfile.test
    environment:
      APP_MODE: {0}
      TEST_REQUESTS: 'true'
    volumes:
      - ./forecast_service:/mnt/app
    stdin_open: true
    tty: true
    depends_on:
      - forecast_service
    """
    ).format(mode)

    # Write file
    with open(os.path.join(destination_dir, filename), "w") as file_object:
        file_object.write(file_text)

def generate_dockerfile(mode, web, sut):
    destination_dir = os.path.join(os.path.abspath(os.curdir), "forecast_service")
    
    # Before creating files, check that the destination directory exists
    if not os.path.isdir(destination_dir):
        os.makedirs(destination_dir)
    
    filename = 'Dockerfile'
    requirements_dev = ""
    expose_port = """
EXPOSE 5000
"""
    new_user = """
# Run the image as a non-root user
RUN useradd -m myuser
USER myuser
"""
    run_cmd = """CMD GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000  --chdir /mnt/app/forecast_service --reload True --log-level debug --capture-output" gunicorn wsgi """
    if web:
        filename = 'Dockerfile.web'
        expose_port = ""
        run_cmd = """CMD GUNICORN_CMD_ARGS="--bind=0.0.0.0:$PORT  --chdir /mnt/app/forecast_service" gunicorn wsgi"""
    if sut:
        filename = 'Dockerfile.test'
        requirements_dev = "_dev"
        expose_port = ""
        new_user = ""
        run_cmd = ""
        
    file_text = (
"""FROM python:3.6.2

# update installation
RUN apt-get -y update
RUN apt-get -y upgrade

# create directories and copy files
RUN mkdir -p /mnt/app
ADD . /mnt/app
WORKDIR /mnt/app

# install dependencies and app
RUN pip install -r requirements{2}.txt
RUN pip install -e /mnt/app/ --force # install app using setup.py

ENV APP_MODE {3}
{4}
{0}
# CMD ["forecast-service"] # run directly for dev only
{1}
""").format(expose_port, run_cmd, requirements_dev, mode, new_user)

    # Write file
    with open(os.path.join(destination_dir, filename), "w") as file_object:
        file_object.write(file_text)

def delete_dockerfile(name):
    destination_dir = os.path.join(os.path.abspath(os.curdir), "forecast_service")
    cmd = """
    rm -rf {0}/{1};
    """.format(destination_dir, name)
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    # mode
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mode",  help="Select mode", 
    choices=["dev", "dev_rds", "dev_cloud", "stage", "prod"], dest="mode")
    args = parser.parse_args()
    mode = args.mode
    #secrets
    postgres_db, postgres_user, postgres_password = load_secrets(mode)
    delete_dockerfile("Dockerfile")
    delete_dockerfile("Dockerfile.test")
    delete_dockerfile("Dockerfile.web")
    generate_docker_compose(mode=mode, postgres_db=postgres_db, 
        postgres_user=postgres_user, postgres_password=postgres_password)
    generate_dockerfile(mode=mode, web=False, sut=False)
    generate_dockerfile(mode=mode, web=True, sut=False)
    generate_dockerfile(mode=mode, web=False, sut=True)