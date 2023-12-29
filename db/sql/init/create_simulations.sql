CREATE TABLE IF NOT EXISTS simulations (
    simulation_id SERIAL PRIMARY KEY,
    dt_entered TIMESTAMP WITH TIME ZONE,
    player VARCHAR(255),
    is_playable BOOLEAN,
    player_won BOOLEAN,
    turns SMALLINT,
    lives SMALLINT,
    len_deck SMALLINT,
    state_initial JSONB,
    state_end JSONB
);