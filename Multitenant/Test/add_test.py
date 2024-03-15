import pytest
from unittest.mock import patch
from db.models import TenantList, UserList, Role, Permission, Application, UserRole, UserApplication, RoleTenant, RolePermission, ApplicationPermission 
from db.add import add_tenant, add_user, add_role, add_permission, add_application, add_role_available_for_tenant
from db.delete import delete_user, delete_tenant, delete_role, delete_permission, delete_application
from db.database import session
from sqlalchemy import select




#Setup for testing tenant addition functionality
@pytest.fixture(scope="class")
def setup_tenant_database():
    #No Setup Needed

    yield

    #Teardown Begins
    input_values = ["Test-Tenant", "yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_tenant()

class TestAddTenant:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no, expected_output", [
        ("Test-Tenant", 7520148693, "Test Owner", 7520148690, 12, 35, ["Test-Tenant", 7520148693, "Test Owner", 7520148690, [{'Floor': 12, 'Plot No.': 35}]])
    ])
    def test_add_tenant_positive(self, tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no, expected_output, capsys):

        input_values = [tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no]
        with patch('builtins.input', side_effect=input_values):
            add_tenant()
            
        added_tenant = session.scalars(select(TenantList).where(TenantList.tenant_name == tenant_name))
        output = []
        for tenants in  added_tenant:
            if tenants.tenant_name == (input_values[0]):
                output.append(tenants.tenant_name)
                output.append(tenants.tenant_phone_number)
                output.append(tenants.owner)
                output.append(tenants.owner_contact)
                output.append(tenants.plot)

        assert output == expected_output


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no, expected_output", [
        ("",None,None,None,None,None, "Tenant name cannot be empty."),
        ("Test-Tenant", None,None,None,None,None, "Tenant Already Exists!!!"),
        ("Tenant Only",75201486,"",75201488,55,36, "Empty fields can't be stored in the database."),
        ("Tester Tenant","",None,None,None,None, "Please enter valid integer values for phone numbers, floor, and plot number."),
        ("Tenant Only","phone_number",None,None,None,None, "Please enter valid integer values for phone numbers, floor, and plot number."),
        ("Tenants",7520148697,"a5",75201482,2,55, "Owner name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Tenant 8nly",None,None,None,None,None, "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Tester Tenant", 7520148693,None,None,None,None, "Phone number already exists in the database."),
        ("TestsTenant", 8520148693, "Test Owner", 75201484, 12, 35,"Plot is Already Allocated!!!"),
        ("TestsTenant", 852014869, "Test Owner", 75201484, 12, 35,"Invalid Phone Number!!!"),
        ("TestsTenant", 8520140693, "Test Owner", 7520148, 12, 35,"Invalid Phone Number!!!")
    ])
    def test_add_tenant_negative(self, setup_tenant_database, tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no, expected_output):
        input_values =[tenant_name, tenant_phone_number, tenant_owner, owner_contact, floor_no, plot_no]
        while None in input_values:
            input_values.remove(None)
        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                add_tenant()
            assert str(e.value) == expected_output





#Setup for testing user addition functionality
@pytest.fixture(scope="class")
def setup_user_database():

    #No Setup Needed
    yield

    #Teardown Begins
    input_values = [["New Owner","yes"],["New User","yes"]]
    for input_value in input_values:
        input_value.insert(1,session.scalars(select(UserList.user_id).filter_by(user_name=input_value[0])).first())
    tenant_id = 0
    for input_value in input_values:
        with patch('builtins.input', side_effect = input_value):
            delete_user(tenant_id)

class TestAddUser:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_phone_number, tenant_name, expected_output, tenant_id",[
        ("New Owner",9976543210,"Test Tenant",["New Owner",9976543210,3],0),
        ("New User",9776543210,None,["New User",9776543210,3],3)
    ])
    def test_add_user_positive(self, user_name, user_phone_number, tenant_name, expected_output, tenant_id):
        
        input_values = [user_name, user_phone_number, tenant_name]
        
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            add_user(tenant_id)

        added_user = session.scalars(select(UserList).where(UserList.user_phone_number==user_phone_number))
        output = []
        for user in added_user:
            if user.user_phone_number == int(input_values[1]):
                output.append(user.user_name)
                output.append(user.user_phone_number)
                output.append(user.tenant)

        assert output == expected_output


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_phone_number, tenant_name, expected_output, tenant_id",[
        ("New Owner","9871543210","","Tenant name cannot be empty.",0),
        ("New Owner","9376543210","Non Existing", "No tenant Found",0),
        ("",None,None,"Empty fields can't be stored in the database.",3),
        ("New User","abc",None, "Please enter valid integer values for phone numbers.",3),
        ("New Owner","9076543210","Non Exi5ting", "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("New 0wner",None,None, "User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("New Owner","9876543210",None,"Phone number already exists in the database.",0),
        ("New Owner","987654321",None,"Invalid Phone Number!!!",0)
    ])
    def test_add_user_negative(self,setup_user_database, user_name, user_phone_number, tenant_name, expected_output, tenant_id):
        
        input_values=[user_name, user_phone_number, tenant_name]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                add_user(tenant_id)
            assert str(e.value) == expected_output





#Setup for testing role addition functionality
@pytest.fixture(scope="class")
def setup_role_database():

    #No Setup Needed
    yield

    #Teardown Begins
    input_values = ["Tester","yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_role()

class TestAddRole:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("role,description, expected_output",[
        ("Tester","Testing",["Tester","Testing"]),
    ])
    def test_add_role_positive(self, role,description, expected_output,capsys):

        input_values = [role,description]
        while None in input_values:
            input_values.remove(None)
        #Test case for new Role
        with patch('builtins.input', side_effect = input_values):
            add_role()

        output=[]
        
        added_role = session.scalars(select(Role).where(Role.role==input_values[0]))

        for role in added_role:
            if role.role == input_values[0] and role.description == input_values[1]:
                output.append(role.role)
                output.append(role.description)
        
        assert output == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("role,description, expected_output",[
        ("Tester",None,"Role already Exists"),
        ("",None,"Role name cannot be empty."),
        ("asd","","Role Description cannot be empty."),
        ("a5d","","Role name can only contain uppercase and lowercase letters, spaces, and hyphens."),
    ])
    def test_add_role_negative(self, setup_role_database, role,description, expected_output):

        input_values = [role,description]

        while None in input_values:
            input_values.remove(None)
        #Test case for new Role
        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                add_role()
            assert  str(e.value) == expected_output





#Setup for testing permission addition functionality
@pytest.fixture(scope="class")
def setup_permission_database():

    #No Setup Needed
    yield

    #Teardown Begins
    input_values = ["New Permission","yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_permission()

class TestAddPermission:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("permission,description, expected_output",[
        ("New Permission","Permission",["New Permission","Permission"])
    ])
    def test_add_permission_positive(self,permission,description,expected_output):

        input_values = [permission,description]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            add_permission()

        output =[]
        

        added_permission = session.scalars(select(Permission).where(Permission.permission==input_values[0]))

        for permission in added_permission:
            if permission.permission == input_values[0] and permission.description == input_values[1]:
                output.append(permission.permission)
                output.append(permission.description)

        assert output == expected_output
        


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("permission,description, expected_output",[
        ("New Permission",None,"Permission already Exists"),
        ("",None,"Permission name cannot be empty."),
        ("New Permissions","","Permission description cannot be empty."),
        ("New 9rmissi0ns",None,"Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_add_permission_negative(self,setup_permission_database, permission,description,expected_output,capsys):

        input_values = [permission,description]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                add_permission()
            assert str(e.value) == expected_output
        





#Setup for testing application addition functionality
@pytest.fixture(scope="class")
def setup_application_database():

    #No Setup Needed
    yield

    #Teardown Begins
    input_values = ["New Application","yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_application()

class TestAddApplication:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("application, expected_output",[
        ("New Application","New Application"),
    ])
    def test_add_application_positive(self,application,expected_output,capsys):

        input_values = [application]


        with patch('builtins.input', side_effect = input_values):
            add_application()


        added_application = session.scalars(select(Application).where(Application.application_name==application))

        for application in added_application:
            if  application.application_name == application:
                assert application.application_name == expected_output


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("application, expected_output",[
        ("New Application","Application already Exists"),
        ("","Application name cannot be empty."),
        ("Version2","Application name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_add_application_negative(self, setup_application_database,application,expected_output,capsys):

        input_values = [application]


        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                add_application()
            assert str(e.value) == expected_output






#Setup for testing tenant role assigning functionality
@pytest.fixture(scope="class")
def setup_for_add_role_available_for_tenant():

    #Setup Begins for Tenant
    input_values = ["Test-Tenant", 7520148693, "Test Owner", 7520148690, 12, 35]

    with patch('builtins.input', side_effect = input_values):
        add_tenant()

    #Setup Begins for Role
    input_values = ["Tester","Testing"]

    with patch('builtins.input', side_effect = input_values):
        add_role()

    yield

    #Teardown Begins for Tenant
    input_values = ["Test-Tenant", "yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_tenant()

    #Teardown Begins for Role
    input_values = ["Tester","yes"]

    with patch('builtins.input', side_effect = input_values):
        delete_role()

class TestAddRoleAvailableForTenant:
    
    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("tenant_name, role,confirmation, expected_output",[
        ("Test-Tenant","Tester","No",[]),
    ])
    def test_add_role_available_for_tenant_positive(self,setup_for_add_role_available_for_tenant,tenant_name, role,confirmation,expected_output):
        input_values =[tenant_name, role,confirmation]
        expected_output.append(session.scalars(select(TenantList).where(TenantList.tenant_name==tenant_name)).first().tenant_id)
        expected_output.append(session.scalars(select(Role).where(Role.role==role)).first().role_id)


        with patch('builtins.input', side_effect = input_values):
            add_role_available_for_tenant()
        
        output=[]

        role_details = session.scalars(select(Role).where(Role.role==role)).first()
        tenant_details = session.scalars(select(TenantList).where(TenantList.tenant_name==tenant_name)).first()
        added_tenant_role = session.scalars(select(RoleTenant).where(RoleTenant.tenant_id == tenant_details.tenant_id, RoleTenant.roles_available == role_details.role_id)).first()
        output.append(added_tenant_role.tenant_id)
        output.append(added_tenant_role.roles_available)
        assert output == expected_output
        



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("tenant,role,confirmation, expected_output",[
        ("Test-Tenant","Tester","No","Role already Assigned"),
        ("Test-Tenant","Testing","No","Role does not Exist!!!"),
        ("Non Existent Org",None,None,"Tenant does not Exist!!!"),
        ("Test Tenant","",None,"Role name cannot be empty."),
        ("",None,None,"Tenant name cannot be empty."),
        ("Test-Ten@nt",None,None,"Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Test-Tenant","Test!ng","No","Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_add_role_available_for_tenant_negative(self,setup_for_add_role_available_for_tenant,tenant,role,confirmation,expected_output,capsys):
        input_values =[tenant,role,confirmation,]

        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with  pytest.raises(ValueError) as e:
                add_role_available_for_tenant()
            assert str(e.value) == expected_output
        



'''class TestAdding:

    @pytest.mark.parametrize("user_name, user_phone_number, tenant_name, expected_output, tenant_id",[
            ("New Owner",9976543210,"Test Tenant",["New Owner",9976543210,3],0),
            ("New User",9776543210,None,["New User",9776543210,3],3)
        ])
    def test_adding_user_positive(self, user_name, user_phone_number, tenant_name, expected_output, tenant_id):
            
            input_values = [user_name, user_phone_number, tenant_name]
            
            while None in input_values:
                input_values.remove(None)

            with patch('builtins.input', side_effect = input_values):
                add_user(tenant_id)

            added_user = session.scalars(select(UserList).where(UserList.user_phone_number==user_phone_number))
            output = []
            for user in added_user:
                if user.user_phone_number == int(input_values[1]):
                    output.append(user.user_name)
                    output.append(user.user_phone_number)
                    output.append(user.tenant)

            assert output == expected_output'''






