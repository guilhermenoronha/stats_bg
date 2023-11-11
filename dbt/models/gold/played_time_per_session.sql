--TODO: find a way in PBI to get average from time column
with

matches as (select * from {{ ref('matches') }}),

played_games as (
    select distinct 
        date, 
        game_id, 
        game_playing_time_real_min
    from matches
),

final as (
    select 
        date, 
        (sum(game_playing_time_real_min)/60.0)*'1 HOUR'::INTERVAL as time_played_per_session_hr 
    from played_games
    group by date
)

select avg(time_played_per_session_hr) as time_played_per_session_hr from final