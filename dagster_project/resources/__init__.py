
from dagster import load_assets_from_package_module, EnvVar
from dagster._utils import file_relative_path
from dagster_dbt import DbtCliResource
from dagster_snowflake_pandas import SnowflakePandasIOManager

from ..assets import staging

DBT_PROJECT_DIR = file_relative_path(__file__, "../../dbt_project")

dbt_dev_resource = DbtCliResource(
    project_dir=DBT_PROJECT_DIR,
    target="dev",
)

staging_assets = load_assets_from_package_module(
    package_module=staging,
    group_name="staging"
)

RESOURCES_DEV = {
    "snowflake_io_manager": SnowflakePandasIOManager(
        account=EnvVar("SNOWFLAKE_ACCOUNT"),
        user=EnvVar("SNOWFLAKE_USER"),
        password=EnvVar("SNOWFLAKE_PASSWORD"),
        database=EnvVar("SNOWFLAKE_DATABASE"),
        warehouse=EnvVar("SNOWFLAKE_WAREHOUSE"),
        schema=EnvVar("SNOWFLAKE_SCHEMA")
    ),
    "dbt": dbt_dev_resource,
}