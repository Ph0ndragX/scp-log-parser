CREATE TABLE round
(
    id           SERIAL PRIMARY KEY,
    log_filename VARCHAR,
    start_time   timestamp,
    end_time     timestamp
);

CREATE TABLE event
(
    id    SERIAL PRIMARY KEY,
    round INTEGER   NOT NULL REFERENCES round ON DELETE CASCADE,
    time  timestamp NOT NULL
);

CREATE TABLE event_kill
(
    id          SERIAL PRIMARY KEY,
    event       INTEGER NOT NULL REFERENCES event ON DELETE CASCADE,
    team_kill   BOOLEAN NOT NULL,
    killed_id   VARCHAR NOT NULL,
    killed_name VARCHAR NOT NULL,
    killed_type VARCHAR NOT NULL,
    killer_id   VARCHAR,
    killer_name VARCHAR,
    killer_type VARCHAR,
    specific    VARCHAR
);

CREATE TABLE event_warhead_status_change
(
    id                  SERIAL PRIMARY KEY,
    event               INTEGER NOT NULL REFERENCES event ON DELETE CASCADE,
    player_changed_id   VARCHAR NOT NULL,
    player_changed_name VARCHAR NOT NULL,
    status              VARCHAR NOT NULL
);

CREATE TABLE event_warhead_countdown_started
(
    id                  SERIAL PRIMARY KEY,
    event               INTEGER NOT NULL REFERENCES event ON DELETE CASCADE,
    player_started_id   VARCHAR NOT NULL,
    player_started_name VARCHAR NOT NULL
);

CREATE TABLE event_warhead_detonated
(
    id    SERIAL PRIMARY KEY,
    event INTEGER NOT NULL REFERENCES event ON DELETE CASCADE
);

CREATE TABLE player_alias
(
    name  VARCHAR,
    alias VARCHAR,
    UNIQUE (name, alias)
);
