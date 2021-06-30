
import pytest
import requests

#@pytest.mark.parametrize("ApiUrl", ['http://73.185.65.150:5555/api/'])
#def test_constantsUrl(supply_constants, ApiUrl):
#    ApiUrl_Imported = supply_constants
#    assert ApiUrl_Imported == ApiUrl, "ApiUrl compaison failed"

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=LoginForm')])
def test_api_LoginForm(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=ManageServer')])
def test_api_ManageServer(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=NewStory')])
def test_api_NewStory(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=NewWisdom')])
def test_api_NewWisdom(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=RegisterForm')])
def test_api_RegisterForm(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=RegisterUserForm')])
def test_api_RegisterUserForm(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("ApiUrl, endpoint", [('http://73.185.65.150:5555/api/', 'form?formKey=UpdatePassword')])
def test_api_UpdatePassword(ApiUrl, endpoint):
    url = ApiUrl + endpoint
    resp = requests.get(url)
    assert resp.status_code == 200

@pytest.mark.parametrize("UIUrl", ['http://skaldbot.isaacbly.com'])
def test_ui_url(UIUrl):
    resp = requests.get(UIUrl)
    assert resp.status_code == 200