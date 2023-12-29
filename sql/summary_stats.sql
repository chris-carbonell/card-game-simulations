SELECT
	player
	, player_won
	
	, ROUND(COUNT(simulation_id), 1) AS cnt_simulations
	, ROUND(AVG(turns), 1) AS avg_turns
	, ROUND(AVG(lives), 1) AS avg_lives
	, ROUND(AVG(len_deck), 1) AS avg_len_deck

FROM simulations

GROUP BY
	player
	, player_won
	
ORDER BY
	player
	, player_won