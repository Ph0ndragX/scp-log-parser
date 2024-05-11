# How to


## Start database
```
docker run --name scp-log-parser-db -e POSTGRES_PASSWORD=postgres -v scp-log-parser-db-volume:/var/lib/postgresql/data -p 5432:5432 -d postgres:latest

docker container stop scp-log-parser-db
docker container start scp-log-parser-db
```

## Setup database 
Initialize database executing scripts in `scripts\db\01_init`

## Parse logs
Run parser to import data to the database: `python scp-log-parser <logs_location>`.
Example command `python scp-log-parser "C:\Users\UserName\AppData\Roaming\SCP Secret Laboratory\ServerLogs\7777"`

## Prepare player aliases

Execute scripts from `scripts\db\02_prepare\01_prepare_player_aliases.sql`.

## Statistics

You can check basic statistics using scripts in `scripts\db\statistics.sql`.

## Visualization using `Apcache Superset`

### Setup
https://hub.docker.com/r/apache/superset

```
docker run -d -p 8080:8088 -e "SUPERSET_SECRET_KEY=secret" --name superset apache/superset
docker exec -it superset superset fab create-admin --username admin --firstname Superset --lastname Admin --email admin@superset.com --password admin
docker exec -it superset superset db upgrade
docker exec -it superset superset init
```

http://localhost:8080/

Credentials according to the commands executed in the previous step (admin/admin).

Now, you have to add SQL connection, find IP address of your local host using `ipconfig`. Connection is between two docker containers, so we cannot use localhost address.

Finally, on the dashboards page you can import .zip from `scripts\apache_superset_exported`.
