from dagster_project import defs

def test_defs_can_load():
    assert defs.get_job_def("core_job")
