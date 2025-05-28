# dagster example

To update to the latest template

```bash
pixi run tpl-update
```

```bash
# dependency upgrade/change
pixi update


# launch a shell
pixi shell --frozen -e ci-validation
cd src/code_location_interview/code_location_interview_dbt/ && dbt deps
cd ../../../
```

## dagster

set `DAGSTER_HOME` to have persistent logs

```bash
# for a single code location
pixi shell --frozen -e ci-validation

dagster dev
# alternatively:
pixi run -e ci-validation start-dev


dagster job list --location foo
dagster job launch --location foo -j all_assets_job
```

## docker

```bash
docker compose -f docker-compose.yml --profile dagster_onprem up --build
```




## .env  file

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

## cleanup

```bash
pixi run cleanup
```