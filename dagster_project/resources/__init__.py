import os

from dagster import load_assets_from_package_module
from dagster._utils import file_relative_path
from dagster_dbt import load_assets_from_dbt_project, DbtCliClientResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

from ..assets import analytics

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")
DBT_PROFILES_DIR = file_relative_path(__file__, "../../dbt_project/")

dbt_assets = load_assets_from_dbt_project(
    project_dir=DBT_PROJECT_DIR,
    profiles_dir=DBT_PROFILES_DIR,
    source_key_prefix=["snowflake"],
    key_prefix=["dbt_project"]
)

analytics_assets = load_assets_from_package_module(
    package_module=analytics,
    group_name="analytics",
    key_prefix=["snowflake", "analytics"]
)

RESOURCES_DEV = {
    "snowflake_io_manager": SnowflakePandasIOManager(
        account=os.environ['SNOWFLAKE_ACCOUNT'],
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        warehouse=os.environ['SNOWFLAKE_WAREHOUSE'],
        database=os.environ['SNOWFLAKE_DATABASE']
    ),
    "dbt": DbtCliClientResource(
        project_dir=DBT_PROJECT_DIR,
        profiles_dir=DBT_PROFILES_DIR
    )
}