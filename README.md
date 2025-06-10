# Coding assignement for Data Scientist position in Magenta 

Hello! You made it! You passed to the second round of interview to become a Data Scientist in Magenta!
This last step is meant to allow us to get to know eah other a bit better: you will have the opportunity to code in a developing environment that resamble the one we are going to use in Magenta!


This repository contains example pipelines and data for interview challenges.

> This is an instance of https://github.com/l-mds/local-data-stack it may be useful for your own data projects.

## tools

- pixi: https://pixi.sh/latest/advanced/installation/
- Dagster: https://dagster.io/ (for futher learning: https://courses.dagster.io/)

## usage
- then: `pixi run start-dev`
- go to https://<your-code-space-name>-<random-chars>-3000.app.github.dev/
- work on the assignments

### Structure of the repository
Here



## advanced usage
# ## docker

```bash
docker compose -f docker-compose.yml --profile dagster_onprem up --build
```

### .env  file

Post install:

- update the secrets in the `.env` files by executing: `openssl rand -base64 32` and setting a suitable secret
- ensure the `.env.enc` can be created by following the instructions in [documentation/secops]

here you find an example `.env` file which should have been auto-generated

```
DO_NOT_TRACK=1

WAREHOUSE_DAGSTER_HOSTNAME=dagster_db
WAREHOUSE_DAGSTER_DB=dagster
WAREHOUSE_DAGSTER_USER=dagster
# openssl rand -base64 32
WAREHOUSE_DAGSTER_PASSWORD=<<your-secret>>

# only set this for dev mode!
DAGSTER_IS_DEV_CLI=True

# only set in the container (should be done from CI pipeline)
#DAGSTER_CLOUD_DEPLOYMENT_NAME=techexploration
#DAGSTER_CLOUD_GIT_URL=https://github.com/myorg/interview
#DAGSTER_CLOUD_GIT_SHA=<<your sha>>
#DAGSTER_CLOUD_GIT_BRANCH=main
```
