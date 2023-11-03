{{
    config(
        materialized='incremental',
        unique_key=['JOB_URL']
    )
}}

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

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  -- (uses > to include records whose timestamp occurred since the last run of this model)
  where RUN_DATETIME > (select max(RUN_DATETIME) from {{ this }})

{% endif %}