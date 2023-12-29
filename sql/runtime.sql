WITH

	agg AS (
		SELECT 
			COUNT(*) AS cnt_records
			, EXTRACT(EPOCH FROM (MAX(dt_entered) - MIN(dt_entered))) AS total_seconds
			, MAX(dt_entered) AS max_dt_entered
		FROM simulations
	)
	
SELECT
	a.*
	, ROUND(a.cnt_records / a.total_seconds, 2) AS simulations_per_second
FROM agg a