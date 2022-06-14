/* LogicoFifa: */

CREATE TABLE player (
    sofifa_id INTEGER PRIMARY KEY,
    player_url VARCHAR,
    short_name VARCHAR,
    long_name VARCHAR,
    player_positions VARCHAR,
    overall INTEGER,
    potential INTEGER,
    value_eur INTEGER,
    wage_eur INTEGER,
    dob DATE,
    weight_kg INTEGER,
    height_cm INTEGER,
    club_team_id INTEGER,
    club_position VARCHAR,
    club_jersey_number INTEGER,
    preferred_foot VARCHAR,
    weak_foot INTEGER,
    skill_moves INTEGER,
    international_reputation VARCHAR,
    work_rate VARCHAR,
    body_type VARCHAR,
    release_clause_eur INTEGER,
    player_tags VARCHAR,
    player_traits VARCHAR,
    pace INTEGER,
    shooting INTEGER,
    passing INTEGER,
    dribbling INTEGER,
    defending INTEGER,
    physic INTEGER,
    attacking_crossing INTEGER,
    attacking_finishing INTEGER,
    attacking_heading_accuracy INTEGER,
    skill_dribbling INTEGER,
    skill_curve INTEGER,
    skill_fk_accuracy INTEGER,
    skill_long_passing INTEGER,
    skill_ball_control INTEGER,
    movement_acceleration INTEGER,
    movement_sprint_speed INTEGER,
    movement_agility INTEGER,
    movement_reactions INTEGER,
    movement_balance INTEGER,
    power_shot_power INTEGER,
    power_jumping INTEGER,
    power_stamina INTEGER,
    power_strength INTEGER,
    power_long_shots INTEGER,
    mentality_aggression INTEGER,
    mentality_interceptions INTEGER,
    mentality_positioning INTEGER,
    mentality_vision INTEGER,
    mentality_penalties INTEGER,
    mentality_composure INTEGER,
    defending_marking_awareness INTEGER,
    defending_standing_tackle INTEGER,
    defending_sliding_tackle INTEGER,
    goalkeeping_diving INTEGER,
    goalkeeping_handling INTEGER,
    goalkeeping_kicking INTEGER,
    goalkeeping_positioning INTEGER,
    goalkeeping_reflexes INTEGER,
    goalkeeping_speed INTEGER,
    ls VARCHAR,
    st VARCHAR,
    rs VARCHAR,
    lw VARCHAR,
    lf VARCHAR,
    cf VARCHAR,
    rf VARCHAR,
    rw VARCHAR,
    lam VARCHAR,
    cam VARCHAR,
    ram VARCHAR,
    lm VARCHAR,
    lcm VARCHAR,
    cm VARCHAR,
    rcm VARCHAR,
    rm VARCHAR,
    lwb VARCHAR,
    ldm VARCHAR,
    cdm VARCHAR,
    rdm VARCHAR,
    rwb VARCHAR,
    lb VARCHAR,
    lcb VARCHAR,
    cb VARCHAR,
    rcb VARCHAR,
    rb VARCHAR,
    gk VARCHAR,
    nationality_name VARCHAR,
    fk_club_club_team_id INTEGER
);

CREATE TABLE club (
    club_team_id INTEGER PRIMARY KEY,
    club_name VARCHAR,
    league_name VARCHAR,
    league_level INTEGER
);

CREATE TABLE contract (
    club_team_id INTEGER,
    sofifa_id INTEGER,
    club_joined DATE,
    club_contract_valid_until INTEGER,
    club_loaned_from VARCHAR,
    fk_jogador_sofifa_id INTEGER,
    fk_club_club_team_id INTEGER
);
 
ALTER TABLE jogador ADD CONSTRAINT FK_jogador_2
    FOREIGN KEY (fk_club_club_team_id)
    REFERENCES club (club_team_id)
    ON DELETE CASCADE;
 
ALTER TABLE contract ADD CONSTRAINT FK_contract_1
    FOREIGN KEY (fk_jogador_sofifa_id)
    REFERENCES jogador (sofifa_id)
    ON DELETE CASCADE;
 
ALTER TABLE contract ADD CONSTRAINT FK_contract_2
    FOREIGN KEY (fk_club_club_team_id)
    REFERENCES club (club_team_id)
    ON DELETE RESTRICT;
