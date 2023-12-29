SELECT
	player
	
	, ROUND(SUM(CASE WHEN player_won THEN 1::NUMERIC ELSE 0 END) / COUNT(simulation_id), 3) AS win_pct
	
	, SUM(player_won::INT) AS sum_player_won
	, ROUND(COUNT(simulation_id), 1) AS cnt_simulations
	, ROUND(AVG(turns), 1) AS avg_turns
	, ROUND(AVG(lives), 1) AS avg_lives
	, ROUND(AVG(len_deck), 1) AS avg_len_deck

FROM simulations

GROUP BY
	player
	
ORDER BY
	player