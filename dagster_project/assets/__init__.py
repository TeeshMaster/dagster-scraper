from dagster import AssetKey, AssetExecutionContext

from dagster_dbt import (
    DagsterDbtTranslator,
    DbtCliResource,
    dbt_assets,
)

from pathlib import Path
from typing import Any, Mapping

DBT_PROJECT_DIR = Path(__file__).joinpath("..", "..", "..", "dbt_project").resolve()

manifest_path = DBT_PROJECT_DIR.joinpath("target", "manifest.json")

class CustomDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        return super().get_asset_key(dbt_resource_props).with_prefix("snowflake")

@dbt_assets(
    manifest=manifest_path,
    dagster_dbt_translator=CustomDagsterDbtTranslator(),
)
def dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()