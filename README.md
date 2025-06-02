# Interview 

This repository contains example pipelines and data for interview challenges.

> This is an instance of https://github.com/l-mds/local-data-stack it may be useful for your own data projects.

## usage

- pixi: https://pixi.sh/latest/advanced/installation/
- then: `pixi run start-dev`
- go to http://localhost:3000
- work on the assignments


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
