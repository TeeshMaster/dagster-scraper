from dagster import Definitions

from .resources import RESOURCES_DEV, staging_assets


all_assets = [*staging_assets]

resources_by_deployment_name = {
    "dev": RESOURCES_DEV,
}

deployment_name = "dev"

defs = Definitions(
    assets=all_assets,
    resources=resources_by_deployment_name[deployment_name],
)
