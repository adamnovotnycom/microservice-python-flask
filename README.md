# Sample microservice - Python, Flask, Firebase

## Docker local development

- Run dev:

        python script/docker.py
        1

- Run tests:

        [open a separate terminal]:
        python script/docker.py
        >> ssh
        >> sut_fs
        pytest --capture=no -vv

## Docs
- API: see docs/swagger.yaml. Import to https://editor.swagger.io//#/ to visualize.

## Upgrade all requirements
- upgrade all pip requirements.txt packages to latest versions:

        pip freeze — local | grep -v ‘^\-e’ | cut -d = -f 1 | xargs -n1 pip install -U