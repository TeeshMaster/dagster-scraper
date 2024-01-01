from dagster import Definitions

from .resources import RESOURCES_DEV, analytics_assets
from .assets import dbt_assets


all_assets = [*analytics_assets, dbt_assets]

resources_by_deployment_name = {
    "dev": RESOURCES_DEV,
}

deployment_name = "dev"

defs = Definitions(
    assets=all_assets,
    resources=resources_by_deployment_name[deployment_name],
)
