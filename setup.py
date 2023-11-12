from setuptools import find_packages, setup

setup(
    name="dagster_project",
    packages=find_packages(exclude=["test"]),
    install_requires=[
        "dagster",
        "dagster-webserver",
        "dagster_postgres",
        "dagster-dbt",
        "dagster-pandas",
        "dagster-snowflake-pandas",
        "dbt-snowflake",
        "pandas",
        "requests",
        "bs4",
        "googlemaps"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"], "tests": ["mypy", "pylint", "pytest"]},
)
