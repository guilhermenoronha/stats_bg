with 

bg_themes as (select * from {{ ref('bg_themes') }}),
themes as (select * from {{ ref('themes') }}),
bg_mechanics as (select * from {{ ref('bg_mechanics') }}),
mechanics as (select * from {{ ref('mechanics') }}),
bg_categories as (select * from {{ ref('bg_categories') }}),
categories as (select * from {{ ref('categories') }}),
distinct_matches as (select distinct "id", "game_id" from {{ ref('matches') }}),

themes_per_match as(
    select 
        t."name", 
        count(bt."theme_id")::integer as total_played,
        'T'::char as taxonomy_type
    from distinct_matches m
    left join bg_themes bt on m."game_id" = bt."game_id"
    left join themes t on cast(t."id" as int) = bt."theme_id"
    where t."name" is not null
    group by 1
),

mechanics_per_match as (
    select 
        m2."name", 
        count(bm."mechanic_id")::integer as total_played,
        'M'::char as taxonomy_type 
    from distinct_matches m
    left join bg_mechanics bm on m."game_id" = bm."game_id"
    left join mechanics m2 on cast(m2."id" as int) = bm."mechanic_id"
    where m2."name" is not null
    group by 1
),

categories_per_type as(
    select 
        c."name", 
        count(bc."category_id")::integer as total_played,
        'C'::char as taxonomy_type
    from distinct_matches m
    left join bg_categories bc on m."game_id" = bc."game_id"
    left join categories c on cast(c."id" as int) = bc."category_id"
    where c."name" is not null
    group by 1
),

final as (
    select * from themes_per_match
    union all
    select * from mechanics_per_match
    union all
    select * from categories_per_type
)

select * from final

