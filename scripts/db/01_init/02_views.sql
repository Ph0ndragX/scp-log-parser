CREATE OR REPLACE VIEW finished_round AS
(
SELECT round.id,
       round.start_time at time zone 'utc' at time zone 'Europe/Warsaw' as start_time,
       round.end_time at time zone 'utc' at time zone 'Europe/Warsaw'   as end_time,
       EXTRACT(EPOCH FROM AGE(end_time, start_time))                    as duration
FROM round
WHERE start_time is not null
  and end_time is not null
    );

CREATE OR REPLACE VIEW round_duration_histogram AS
(
SELECT g.n as up_to_minutes, COUNT(fr.id) as rounds
FROM generate_series(1, 30) g(n)
         LEFT JOIN finished_round fr ON width_bucket(fr.duration, 0, 60 * 60, 60) = g.n
GROUP BY g.n
ORDER BY g.n
    );

CREATE OR REPLACE VIEW total_kills_by_player AS
(
SELECT pa.name, count(*) as count
FROM event_kill ek
         LEFT JOIN player_alias pa ON pa.alias = ek.killer_name
WHERE ek.killer_name is not null
GROUP BY pa.name
ORDER BY count(*)
    );

CREATE OR REPLACE VIEW team_kills_by_player AS
(
SELECT pa.name, count(*) as count
FROM event_kill ek
         JOIN player_alias pa ON pa.alias = ek.killer_name
WHERE ek.team_kill
GROUP BY pa.name
ORDER BY count(*)
    );

CREATE OR REPLACE VIEW most_teamKilled_players AS
(
SELECT killed_alias.name as killed_name, count(*) as count
FROM event_kill ek
         JOIN player_alias killed_alias ON killed_alias.alias = ek.killed_name
WHERE ek.team_kill is true
GROUP BY killed_alias.name
ORDER BY count(*)
    );

CREATE OR REPLACE VIEW team_kills_by_player_pair AS
(
SELECT killer_alias.name as killer_name, killed_alias.name as killed_name, count(*) as count
FROM event_kill ek
         JOIN player_alias killer_alias ON killer_alias.alias = ek.killer_name
         JOIN player_alias killed_alias ON killed_alias.alias = ek.killed_name
WHERE ek.team_kill
GROUP BY killer_alias.name, killed_alias.name
ORDER BY count(*)
    );

CREATE OR REPLACE VIEW other_deaths AS
(
SELECT ek.specific, count(*) as count
FROM event_kill ek
WHERE ek.killer_name is null
GROUP BY ek.specific
ORDER BY count(*)
    );

CREATE OR REPLACE VIEW other_deaths_by_player AS
(
SELECT killed_alias.name as killed_name, ek.specific, count(*) as count
FROM event_kill ek
         JOIN player_alias killed_alias ON killed_alias.alias = ek.killed_name
WHERE ek.killer_name is null
GROUP BY killed_alias.name, ek.specific
ORDER BY count(*)
    );