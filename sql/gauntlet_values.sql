-- # Overview
-- assign a value (or difficulty) to a guantlet's initial state
-- assuming cards closer to 8 are more difficult to guess on
-- compared to cards at the extremes (e.g., 2 or Ace)

WITH

	-- ranks
	-- the absolute value doesn't matter
	-- the relative value (e.g., Ace is higher than King) is all that really matters here
	ranks AS (
		SELECT 'Ace' AS str, 6 AS val
		UNION ALL
		SELECT 'King', 5
		UNION ALL
		SELECT 'Queen', 4
		UNION ALL
		SELECT 'Jack', 3
		UNION ALL
		SELECT '10', 2
		UNION ALL
		SELECT '9', 1
		UNION ALL
		SELECT '8', 0
		UNION ALL
		SELECT '7', 1
		UNION ALL
		SELECT '6', 2
		UNION ALL
		SELECT '5', 3
		UNION ALL
		SELECT '4', 4
		UNION ALL
		SELECT '3', 5
		UNION ALL
		SELECT '2', 6
	)
	
	-- gauntlet
	-- expose gauntlet
	, gauntlet AS (
		SELECT
			simulation_id
			
			, JSONB_EXTRACT_PATH(state_initial, 'stacks', 'gauntlet') AS gauntlet
			
		FROM simulations s

        WHERE player != 'PlayerRandom(p_higher=0.5)'  -- they always lose
	)
	
	-- gauntlet_keys
	-- get gauntlet keys
	, gauntlet_keys AS (
		SELECT 
			*
			, JSONB_OBJECT_KEYS(gauntlet) AS idx
		FROM gauntlet g
	)
	
	-- gauntlet_keys_vals
	-- with keys, get gauntlet vals too
	, gauntlet_keys_vals AS (
		SELECT
			g.*
			, JSONB_EXTRACT_PATH_TEXT(gauntlet, g.idx, 'top') AS card
		FROM gauntlet_keys g
	)
	
	-- card_values
	-- get values for each card
	, card_values AS (
		SELECT
			simulation_id

			, SUBSTRING(card FROM '(.*) of .*') AS card_str
			, r.val AS card_val
		
		FROM gauntlet_keys_vals g
		
		LEFT JOIN ranks r
		ON SUBSTRING(card FROM '(.*) of .*') = r.str
	)
	
	-- gauntlet_values
	-- agg values to gauntlet/simulation
	, gauntlet_values AS (
		SELECT 
			simulation_id
			
			, SUM(card_val) AS sum_card_val
			
		FROM card_values
		GROUP BY simulation_id
	)
	
	-- sims_gauntlet_vals
	-- join simulations with gauntlet values
	, sims_gauntlet_vals AS (
		SELECT
			s.*
			, gv.sum_card_val
		FROM simulations s
		LEFT JOIN gauntlet_values gv
		ON s.simulation_id = gv.simulation_id
	)
	
	-- agg
	, agg AS (
		SELECT
			player
            , sum_card_val
			
			, ROUND(COUNT(simulation_id), 1) AS cnt_simulations
			, ROUND(SUM(CASE WHEN player_won THEN 1::NUMERIC ELSE 0 END) / COUNT(simulation_id), 3) AS win_pct
		
		FROM sims_gauntlet_vals

		GROUP BY
            player
			, sum_card_val
			
		ORDER BY
            player ASC 
			, sum_card_val ASC
	)
	
	, main AS (
		SELECT * FROM agg
	)
	
SELECT * FROM main

-- |player|sum_card_val|cnt_simulations|win_pct|
-- |------|------------|---------------|-------|
-- |PlayerExtreme()|9|8.0|0.000|
-- |PlayerExtreme()|10|16.0|0.125|
-- |PlayerExtreme()|11|38.0|0.026|
-- |PlayerExtreme()|12|93.0|0.032|
-- |PlayerExtreme()|13|191.0|0.016|
-- |PlayerExtreme()|14|407.0|0.027|
-- |PlayerExtreme()|15|725.0|0.018|
-- |PlayerExtreme()|16|1244.0|0.029|
-- |PlayerExtreme()|17|1977.0|0.027|
-- |PlayerExtreme()|18|3065.0|0.027|
-- |PlayerExtreme()|19|4398.0|0.031|
-- |PlayerExtreme()|20|6585.0|0.035|
-- |PlayerExtreme()|21|8827.0|0.033|
-- |PlayerExtreme()|22|11441.0|0.036|
-- |PlayerExtreme()|23|14577.0|0.039|
-- |PlayerExtreme()|24|17630.0|0.042|
-- |PlayerExtreme()|25|20792.0|0.042|
-- |PlayerExtreme()|26|23658.0|0.047|
-- |PlayerExtreme()|27|25782.0|0.048|
-- |PlayerExtreme()|28|27575.0|0.051|
-- |PlayerExtreme()|29|27959.0|0.053|
-- |PlayerExtreme()|30|27579.0|0.058|
-- |PlayerExtreme()|31|26155.0|0.059|
-- |PlayerExtreme()|32|24251.0|0.060|
-- |PlayerExtreme()|33|21216.0|0.065|
-- |PlayerExtreme()|34|18422.0|0.072|
-- |PlayerExtreme()|35|15125.0|0.075|
-- |PlayerExtreme()|36|11896.0|0.077|
-- |PlayerExtreme()|37|9202.0|0.076|
-- |PlayerExtreme()|38|6683.0|0.084|
-- |PlayerExtreme()|39|4648.0|0.096|
-- |PlayerExtreme()|40|3248.0|0.099|
-- |PlayerExtreme()|41|2059.0|0.103|
-- |PlayerExtreme()|42|1201.0|0.106|
-- |PlayerExtreme()|43|680.0|0.126|
-- |PlayerExtreme()|44|343.0|0.120|
-- |PlayerExtreme()|45|206.0|0.117|
-- |PlayerExtreme()|46|88.0|0.125|
-- |PlayerExtreme()|47|34.0|0.088|
-- |PlayerExtreme()|48|11.0|0.091|
-- |PlayerExtreme()|49|4.0|0.500|
-- |PlayerExtreme()|50|2.0|0.000|
-- |PlayerModal()|9|4.0|0.000|
-- |PlayerModal()|10|5.0|0.000|
-- |PlayerModal()|11|3.0|0.000|
-- |PlayerModal()|12|21.0|0.000|
-- |PlayerModal()|13|54.0|0.000|
-- |PlayerModal()|14|118.0|0.093|
-- |PlayerModal()|15|209.0|0.072|
-- |PlayerModal()|16|390.0|0.067|
-- |PlayerModal()|17|516.0|0.068|
-- |PlayerModal()|18|892.0|0.068|
-- |PlayerModal()|19|1312.0|0.073|
-- |PlayerModal()|20|1872.0|0.067|
-- |PlayerModal()|21|2584.0|0.071|
-- |PlayerModal()|22|3407.0|0.078|
-- |PlayerModal()|23|4233.0|0.079|
-- |PlayerModal()|24|5145.0|0.087|
-- |PlayerModal()|25|6018.0|0.087|
-- |PlayerModal()|26|6843.0|0.091|
-- |PlayerModal()|27|7434.0|0.101|
-- |PlayerModal()|28|7776.0|0.100|
-- |PlayerModal()|29|8041.0|0.112|
-- |PlayerModal()|30|7983.0|0.112|
-- |PlayerModal()|31|7630.0|0.113|
-- |PlayerModal()|32|6863.0|0.117|
-- |PlayerModal()|33|6397.0|0.132|
-- |PlayerModal()|34|5307.0|0.138|
-- |PlayerModal()|35|4290.0|0.132|
-- |PlayerModal()|36|3463.0|0.146|
-- |PlayerModal()|37|2700.0|0.166|
-- |PlayerModal()|38|1889.0|0.163|
-- |PlayerModal()|39|1413.0|0.163|
-- |PlayerModal()|40|933.0|0.160|
-- |PlayerModal()|41|602.0|0.179|
-- |PlayerModal()|42|346.0|0.173|
-- |PlayerModal()|43|181.0|0.166|
-- |PlayerModal()|44|106.0|0.198|
-- |PlayerModal()|45|61.0|0.246|
-- |PlayerModal()|46|24.0|0.250|
-- |PlayerModal()|47|8.0|0.250|
-- |PlayerModal()|48|4.0|0.000|
-- |PlayerModal()|49|1.0|1.000|
-- |PlayerRandom(p_higher=0.5)||22583.0|0.000|