
import pytest
import requests
import os

@pytest.fixture
def supply_constants():
    cwd = os.getcwd()
    os.chdir(os.path.join(cwd, '..', '..', '..'))
    new_cwd = os.getcwd()
    constants_path = os.path.join(new_cwd, 'SkaldbotUI', 'src', 'helpers', 'constants.js')
    with open (constants_path) as constants_file:
        constants = constants_file.read()
        ApiUrl_Imported = (constants.split("'")[1:2])[0]
        
    return ApiUrl_Imported, oauthToken_Imported, githubSecret_Imported