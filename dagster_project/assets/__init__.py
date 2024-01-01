from dagster import AssetKey, AssetExecutionContext, load_assets_from_package_module

from dagster_dbt import (
    DagsterDbtTranslator,
    DbtCliResource,
    dbt_assets,
)

from ..assets import analytics

from pathlib import Path
from typing import Any, Mapping

DBT_PROJECT_DIR = Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve()

manifest_path = DBT_PROJECT_DIR.joinpath("target", "manifest.json")


analytics_assets = load_assets_from_package_module(
    package_module=analytics,
    group_name="analytics",
    key_prefix=["snowflake", "analytics"]
)


class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        return super().get_asset_key(dbt_resource_props).with_prefix("snowflake")

@dbt_assets(
    manifest=manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()