SELECT *
FROM finished_round
ORDER BY start_time;

SELECT *
FROM round_duration_histogram;

SELECT *
FROM total_kills_by_player
ORDER BY count DESC;

SELECT *
FROM team_kills_by_player;

SELECT *
FROM most_teamKilled_players
ORDER BY count DESC;

SELECT *
FROM team_kills_by_player_pair
ORDER BY count DESC;

SELECT *
FROM other_deaths
ORDER BY count DESC;

SELECT *
FROM other_deaths_by_player
ORDER BY count DESC;
