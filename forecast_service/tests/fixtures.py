import os
import pytest

@pytest.fixture
def requests_fix():
    run_requests = {"run": False}
    try:
        if os.environ["TEST_REQUESTS"] == 'true':
            from forecast_service.parse_instance import (app_url, app_user, 
                app_password)
            run_requests["run"] = True
            run_requests["url"] = app_url
            run_requests["user"] = app_user
            run_requests["password"] = app_password
    except:
        pass
    return run_requests

@pytest.fixture
def db_fix():
    """
    Provides consistent data for all tests
    """
    import test_forecast_service
    test_forecast_service.insert_fake_data() # tear down; keeps the same data after test
    yield None
    if os.environ["APP_MODE"] in ["dev", "devcloud"]:
        test_forecast_service.insert_fake_data() # tear down; keeps the same data after test