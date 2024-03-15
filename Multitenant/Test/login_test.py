import pytest
from unittest.mock import patch, Mock
from db.login import check_login,set_username_password,change_own_password, change_password, delete_username_password
from db.models import LoginDetail,UserList
from db.database import session
from sqlalchemy import select


#Setup for testing setup of username and password functionality
@pytest.fixture(scope="class")
def setup_login_database_setting_login_details():
    #No Setup needed
    yield

    #Teardown Begins
    input_values = [["Test Dummy User",7,"yes"],["Test Dummy Owner",5,"yes"]]
    tenant_id = 0

    for input_value in input_values:
        with patch('builtins.input', side_effect = input_value):
            delete_username_password(tenant_id)

class TestSetUsernamePassword:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("username, user_id, login_username, password, expected_output, tenant_id",[
        ("Test Dummy User",7,"TDU","123",[7,"TDU","123"],0),
        ("Test Dummy Owner",5,"TDO","123",[5,"TDO","123"],3),
    ])
    def test_set_username_password_positive(self,username, user_id, login_username, password,expected_output,tenant_id):

        input_values = [username, user_id, login_username, password]

        with patch('builtins.input', side_effect = input_values):
            set_username_password(tenant_id)

        output =[]
        login_details = session.scalars(select(LoginDetail).filter_by(user_name = login_username)).first()
        output.append(login_details.user_id)
        output.append(login_details.user_name)
        output.append(login_details.user_password)

        assert  output ==  expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output, tenant_id",[
        (["Test Dummy User"],"No User with the given username",6),
        (["Test Dummy User",session.scalars(select(UserList.user_id).filter_by(user_name="Test Dummy User")).first(),"TDU"],"Username Already Exists!!!",3),
        (["Test Dummy User","555"],"Wrong User ID!!!",3),
        (["Test Dummy User",session.scalars(select(UserList.user_id).filter_by(user_name="Test Dummy User")).first(),""],"LogIn Username cannot be empty.",3),
        ([""],"User name cannot be empty.",0),
        (["Test @123"],"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
    ])
    def test_set_username_password_negative(self,setup_login_database_setting_login_details,input_values,expected_output,tenant_id):

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                set_username_password(tenant_id)
            assert str(e.value) == expected_output




class TestChangeOwnPassword:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("old_password, new_password, expected_output, user_name",[
        ("123","321","321","TDUU"),
        ("321","123","123","TDUU"),
    ])
    def test_change_own_password_positive(self,old_password, new_password,expected_output,user_name):

        input_values = [old_password, new_password]

        with patch('builtins.input', side_effect = input_values):
            change_own_password(user_name)

        login = session.scalars(select(LoginDetail).filter_by(user_name = user_name)).first()
        assert login.user_password == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output, user_name",[
        (["366","366","366"],"Too many Attempts!!!","TDUU"),
        ([""],"Password cannot be empty.","TDUU"),
        (["123",""],"Password cannot be empty.","TDUU"),
    ])
    def test_change_own_password_negative(self,input_values,expected_output,user_name):
        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                change_own_password(user_name)
            assert str(e.value) == expected_output




#Setup for testing changing password functionality
@pytest.fixture(scope="class")
def setup_login_database_for_changing_password():
    #setup process
    input_values = [["Test Dummy User",7,"TDU","123"],["Test Dummy Owner",5,"TDO","123"]]
    tenant_id = 0

    for input_value in input_values:
        with patch('builtins.input', side_effect = input_value):
            set_username_password(tenant_id)
    yield

    #teardownprocess
    input_values = [["Test Dummy User",7,"yes"],["Test Dummy Owner",5,"yes"]]
    
    for input_value in input_values:
        with patch('builtins.input', side_effect = input_value):
            delete_username_password(tenant_id)
    
class TestChangePassword:

    '''
        Positive Scenarios
    '''    
    @pytest.mark.parametrize("login_username, password, expected_output, tenant_id",[
        ("TDO","789","789",0),
        ("TDU","321","321",3),
    ])
    def test_change_password_positive(self,setup_login_database_for_changing_password,login_username, password,expected_output,tenant_id):

        input_values = [login_username, password]

        with patch('builtins.input', side_effect = input_values):
            change_password(tenant_id)

        login = session.scalars(select(LoginDetail).filter_by(user_name = login_username)).first()
        assert login.user_password == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output, tenant_id",[
        (["person_5"],"Username Doesnot Exist!!!",0),
        ([""],"LogIn Username cannot be empty.",0),
        (["TDU",""],"Password cannot be empty.",0),
    ])
    def test_change_password_negative(self,input_values,expected_output,tenant_id):
        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                change_password(tenant_id)
            assert  str(e.value) == expected_output




#Setup for testing login check functionality
@pytest.fixture(scope="class")
def setup_login_database_for_login_check():
    #setup process
    input_values = ["Test Dummy Owner",5,"TDO","789"]
    tenant_id = 0

    with patch('builtins.input', side_effect = input_values):
        set_username_password(tenant_id)

    yield

    #teardownprocess
    input_values = ["Test Dummy Owner",5,"yes"]
    
    with patch('builtins.input', side_effect = input_values):
        delete_username_password(tenant_id)
    
class TestCheckLogin:

    @pytest.mark.parametrize("login_username, password, application_id, expected_output",[
        ("TDO","789", "25",True),#Positive Case
        ("TDO", "600", "25",False)#Negative Case
    ])
    def test_check_login(self,setup_login_database_for_login_check,login_username, password, application_id,expected_output):
        assert check_login(login_username, password, application_id) == expected_output



