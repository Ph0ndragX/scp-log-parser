WITH aliases AS (SELECT distinct killer_name as name, killer_name as alias
                 FROM event_kill
                 WHERE killer_name is not null
                 UNION
                 DISTINCT
                 SELECT distinct killed_name as name, killed_name as alias
                 FROM event_kill
                 WHERE killer_name is not null)
INSERT
INTO player_alias(name, alias)
SELECT name, alias
FROM aliases;
