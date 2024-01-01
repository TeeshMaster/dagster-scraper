from dagster import Definitions

from .resources import RESOURCES_DEV
from .assets import analytics_assets, dbt_assets
from .jobs import analytics_job


all_assets = [*analytics_assets, dbt_assets]

resources_by_deployment_name = {
    "dev": RESOURCES_DEV,
}

deployment_name = "dev"

defs = Definitions(
    assets=all_assets,
    resources=resources_by_deployment_name[deployment_name],
    jobs=[analytics_job]
)
