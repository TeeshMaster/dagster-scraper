{{
    config(
        materialized='incremental',
        unique_key=['JOB_URL']
    )
}}
with daily_jobs as (
    select
        RUN_DATETIME, 
        PUBLISHED_DATE, 
        JOB_TITLE, 
        COMPANY_NAME, 
        LOCATION, 
        SALARY, 
        CATEGORY, 
        SHORT_DESCRIPTION, 
        FEATURED, 
        LATITUDE, 
        LONGITUDE, 
        JOB_URL, 
        SEARCH_JOB_TITLE, 
        SEARCH_JOB_LOCATION
    from {{ source('analytics', 'data_engineer_jobs_stg') }}
    where 
        contains(upper(JOB_TITLE), 'DATA') or
        contains(upper(COMPANY_NAME), 'DATA') or 
        contains(upper(SHORT_DESCRIPTION), 'DATA')
)

select * from daily_jobs

{% if is_incremental() %}

    where RUN_DATETIME > (select max(RUN_DATETIME) from {{ this }})

{% endif %}