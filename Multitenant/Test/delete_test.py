import pytest
from db.database import session
from unittest.mock import patch, Mock
from db.add import add_tenant, add_user, add_role, add_permission, add_application, add_role_available_for_tenant
from db.delete import delete_user, delete_tenant, delete_role, delete_permission, delete_application
from db.models import TenantList,UserList,Role,Permission,Application,RoleTenant,UserRole,UserApplication,LoginDetail,RolePermission,ApplicationPermission
from sqlalchemy import select



#Setup for testing tenant deletion functionality
@pytest.fixture(scope="module")
def setup_tenant_database():
    input_values = ["Test-Tenant", 7520148693, "Test Owner", 7520148690, 12, 35]
    with patch('builtins.input', side_effect=input_values):
            add_tenant()

class TestDeleteTenant:

    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("tenant,confirmation, expected_output", [
        ("Test-Tenant", "no", "Deletion canceled."),
        ("Test Tenantsss",None, "No such Tenant exists in the Database."),
        ("",None, "Tenant name cannot be empty."),
        ("Test Tenant5",None, "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_delete_tenant_negative(self, setup_tenant_database, tenant,confirmation, expected_output):

        input_values = [tenant,confirmation]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_tenant()
            assert str(e.value) == expected_output



    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("tenant,confirmation, expected_output", [
        ("Test-Tenant", "yes", None),
    ])
    def test_delete_tenant_positive(self, tenant,confirmation, expected_output):

        input_values = [tenant,confirmation]

        with patch('builtins.input', side_effect = input_values):
            delete_tenant()

        tenant_details = session.scalars(select(TenantList).where(TenantList.tenant_name==input_values[0])).first()
        assert tenant_details == expected_output





#Setup for testing user deletion functionality
@pytest.fixture(scope="module")
def setup_user_database():
    input_values = [["New Owner",9976543210,"Test Tenant"],["New User",9776543210,"Test Tenant"]]
    tenant_id = 0
    for input_value in input_values:
        with patch('builtins.input', side_effect=input_value):
            add_user(tenant_id)

class TestDeleteUser:

    '''
        Negative Scenarios
    '''
    #find a way to counter the error
    @pytest.mark.parametrize("user_name, user_id,confirmation, expected_output, tenant_id", [
        ("New Owner",None,"no","Deletion canceled.",0),
        ("New",None,None,"No such User exists in the Database.",0),
        ("",None,None,"User name cannot be empty.",0),
        ("New 0wner",None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("New Owner","xyz","no","Please enter valid integer values for User ID.",0),
        ("New Owner","7825","no","No user with that User ID",0)
        ])
    def test_delete_user_negative(self,setup_user_database,user_name, user_id,confirmation,expected_output,tenant_id):

        input_values = [user_name, user_id,confirmation]

        while None in input_values:
            input_values.remove(None)

        if expected_output == "Deletion canceled.":
            input_values.insert(1,session.scalars(select(UserList.user_id).filter_by(user_name=user_name)).first())
            #input_values.insert(1,14)
            
    
        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_user(tenant_id)
            assert str(e.value) == expected_output



    '''
        Positive Scenarios
    '''
    #find a way to counter the error
    @pytest.mark.parametrize("user_name,confirmation, expected_output, tenant_id",[
            ("New Owner","yes",None,0),
            ("New User","yes",None,3)
            ])
    def test_delete_user_positive(self, user_name,confirmation,expected_output,tenant_id):

        input_values = [user_name,confirmation]


        input_values.insert(1,session.scalars(select(UserList.user_id).filter_by(user_name=user_name)).first())
        #input_values.insert(1,14)

        with patch('builtins.input', side_effect = input_values):
            delete_user(tenant_id)

        user = session.scalars(select(UserList).filter_by(user_id = input_values[1])).first()
        assert user == expected_output
        




#Setup for testing role deletion functionality
@pytest.fixture(scope="module")
def setup_role_database():
    input_values = ["Tester","Testing"]
    with patch('builtins.input', side_effect=input_values):
            add_role()

class TestDeleteRole:

    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("role, confirmation, expected_values",[
        ("Tester","no","Deletion canceled."),
        ("Test Tenantsss",None,"No such Role exists in the Database."),
        ("",None,"Role name cannot be empty."),
        ("a5d",None,"Role name can only contain uppercase and lowercase letters, spaces, and hyphens."),
    ])
    def test_delete_role_negative(self,setup_role_database,role, confirmation,expected_values):

        input_values = [role, confirmation]

        while None in input_values:
            input_values.remove(None)


        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_role()
            assert str(e.value) == expected_values




    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("role, confirmation, expected_values",[
        ("Tester","yes",None),
    ])
    def test_delete_role_positive(self, role, confirmation,expected_values):

        input_values=[role, confirmation]

        while None in input_values:
            input_values.remove(None)
        
        with patch('builtins.input', side_effect = input_values):
            delete_role()


        role_details = session.scalars(select(Role).filter_by(role = role)).first()

        assert role_details == expected_values
    '''        assert connected_permission is None
            assert connected_users is None
            assert connected_tenant is None'''





#Setup for testing permission deletion functionality
@pytest.fixture(scope="module")
def setup_permission_database():
    input_values = ["New Permission","Permission"]
    with patch('builtins.input', side_effect=input_values):
            add_permission()

class TestDeletePermission:

    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("permission, confirmation, expected_values",[
        ("New Permission","no","Deletion canceled."),
        ("Test Tenantsss",None,"No such Permission exists in the Database."),
        ("",None,"Permission name cannot be empty."),
        ("a5d",None,"Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_delete_permission_negative(self,setup_permission_database,permission, confirmation,expected_values):
        
        input_values = [permission, confirmation]
                
        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_permission()
            assert str(e.value) == expected_values
            


    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("permission, confirmation, expected_values",[
        ("New Permission","yes",None),
    ])
    def test_delete_permission_positive(self,permission, confirmation,expected_values):

        input_values=[permission, confirmation]

        
        with patch('builtins.input', side_effect = input_values):
            delete_permission()

        permission_details = session.scalars(select(Permission).filter_by(permission = permission)).first()
        assert permission_details== None




#Setup for testing application deletion functionality
@pytest.fixture(scope="module")
def setup_application_database():
    input_values = ["New Application"]
    with patch('builtins.input', side_effect=input_values):
            add_application()

class TestDeleteApplication:

    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("application, confirmation, expected_values",[
        ("New Application","no","Deletion canceled."),
        ("Test Tenantsss",None,"No such Application exists in the Database."),
        ("",None,"Application name cannot be empty."),
        ("a5d",None,"Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_delete_application_negative(self,setup_application_database,application, confirmation,expected_values):


        input_values = [application, confirmation]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_application()
            assert str(e.value) == expected_values



    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("application, confirmation, expected_values",[
        ("New Application","yes",None),
    ])
    def test_delete_application_positive(self,application, confirmation,expected_values):

        input_values = [application, confirmation]
        
        with patch('builtins.input', side_effect = input_values):
            delete_application()

        application_details = session.scalars(select(Application).filter_by(application_name = application)).first()
        assert application_details == expected_values




