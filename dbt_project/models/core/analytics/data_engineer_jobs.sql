

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