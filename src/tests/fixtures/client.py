import pytest
import os

from starlette.testclient import TestClient
from ...app.main import app
from testcontainers.mysql import MySqlContainer

data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
funds_json = os.path.join(data_folder, 'funds.json')
fund_options_json = os.path.join(data_folder, 'fund-options.json')
fund_values_basic_csv = os.path.join(data_folder, 'fund-values-basic.csv')
holidays_csv = os.path.join(data_folder, 'holidays.csv')

@pytest.fixture()
def client(backend_mysql: MySqlContainer) -> TestClient:
    """Fixture for test REST client

    Returns:
        TestClient: test REST client
    """

    os.environ["FUND_JSON"] = funds_json
    os.environ["FUND_OPTIONS_JSON"] = fund_options_json
    os.environ["FUND_VALUES_BASIC_CSV"] = fund_values_basic_csv
    os.environ["HOLIDAYS_CSV"] = holidays_csv

    return TestClient(app)
