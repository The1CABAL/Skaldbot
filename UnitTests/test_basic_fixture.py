
import pytest

@pytest.mark.parametrize("ApiUrl", ['http://73.185.65.150:5555/api/'])

def test_constantsUrl(supply_constants, ApiUrl):
    ApiUrl_Imported, oauthToken_Imported, githubSecret_Imported = supply_constants
    assert ApiUrl_Imported == ApiUrl, "ApiUrl compaison failed"