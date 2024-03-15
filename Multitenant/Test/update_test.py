import pytest
from db.database import session
from db.models import TenantList, UserList, Role, Permission, Application, UserRole, UserApplication, RoleTenant, RolePermission, ApplicationPermission, LoginDetail
from db.update import update_tenant, update_user, transfer_user, assign_revoke_role, add_remove_permission_from_role, assign_revoke_user_application, update_own_user_details, assign_revoke_role_tenant, update_application_permission
from db.login import delete_username_password,set_username_password
from sqlalchemy import select

from unittest.mock import patch




class TestUpdateTenant:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no, expected_output, tenant_id", [
        ("Test Tenant","New Test Tenant", "8410257963", "New Test Owner", "8410257024", 1, None,2,32, ["New Test Tenant", 8410257963, "New Test Owner", 8410257024, [{"Floor": 2,"Plot No.": 3}, {"Floor": 5,"Plot No.": 6},{"Floor": 2,"Plot No.": 32}]], 0),
        (None,"Test Tenant", "8410257963", "New Test Owner", "8410257024", 1, None, 3,32, ["Test Tenant", 8410257963, "New Test Owner", 8410257024, [{"Floor": 2,"Plot No.": 3}, {"Floor": 5,"Plot No.": 6},{"Floor": 2,"Plot No.": 32},{"Floor": 3,"Plot No.": 32}]], 3),
        (None,"Test Tenant", "8410257963", "Old Test Owner", "9876503210", 2, 3, None,None, ["Test Tenant", 8410257963, "Old Test Owner", 9876503210,[{"Floor": 2,"Plot No.": 3}, {"Floor": 5,"Plot No.": 6},{"Floor": 3,"Plot No.": 32}]], 3),
        (None,"Test Tenant", "8410257963", "Old Test Owner", "9876503210", 3, 3, 2, 32, ["Test Tenant", 8410257963, "Old Test Owner", 9876503210,[{"Floor": 2,"Plot No.": 3}, {"Floor": 5,"Plot No.": 6},{"Floor": 2,"Plot No.": 32}]], 3),
        ("Test Tenant","Test Tenant", "8410257963", "New Test Owner", "8410257024", 2, 3,None,None, ["Test Tenant", 8410257963, "New Test Owner", 8410257024, [{"Floor": 2,"Plot No.": 3}, {"Floor": 5,"Plot No.": 6}]], 0),
    ])
    def test_update_tenant_positive(self,old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no, expected_output, tenant_id):
        
        input_values = [old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            update_tenant(tenant_id)

        output = []


        added_tenant = session.scalars(select(TenantList).filter_by(tenant_name=new_tenant_name)).first()
        output.append(added_tenant.tenant_name)
        output.append(added_tenant.tenant_phone_number)
        output.append(added_tenant.owner)
        output.append(added_tenant.owner_contact)
        output.append(added_tenant.plot)

        assert output == expected_output




    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no, expected_output, tenant_id", [
        ("Alpha Tenant",None,None,None,None,None,None,None,None, "No tenant found with name Alpha Tenant. Please check and try again.",0),
        ("",None,None,None,None,None,None,None,None, "Tenant name cannot be empty.",0),
        ("TestTen@nt",None,None,None,None,None,None,None,None, "Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        (None,"Test Tenant","","a","",None,None,None,None, "Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",3),
        (None,"Test Tenant","8410257024","","8410257024",None,None,None,None, "Empty fields can't be stored in the database.",3),
        (None,"Tenant5","159","a5","789",None,None,None,None, "Tenant name and Owner name can only contain uppercase and lowercase letters, spaces, and hyphens.",3),
        (None,"Test Ten@nt", "8410257024", "Old Test Owner", "9876503210",None,None,None,None, "Tenant name and Owner name can only contain uppercase and lowercase letters, spaces, and hyphens.", 3),
        (None,"Tenant","a","a","a",None,None,None,None, "Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",3),
        ("Test Tenant","New Test Tenant", "1234867890", "New Test Owner", "8410257024",None,None,None,None,"Phone number already exists in the database.", 0),
        ("TestxTenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 2,None,None,None, "Cant remove or replace plots when No plots are Assigned",0),
        ("TestxTenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 3, None,None,None, "Cant remove or replace plots when No plots are Assigned",0),
        ("TestxTenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 1,None,"abc",None, "Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",0),
        ("TestxTenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", "abc",None,None,None, "Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",0),
        ("Test Tenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 2, 55,None,None, "Invalid Plot Index!!!",0),
        ("Test Tenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 2, "abc",None,None,"Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",0),
        ("Test Tenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 3, 55,None,None, "Invalid Plot Index!!!",0),
        ("Test Tenant","TestxTenant", "8410257024", "New Test Owner", "8410257024", 3, "abc",None,None, "Please enter valid integer values for phone numbers, floor, choice, plot index and plot number.",0),
        ("Test Tenant","New Test Tenant", "8410257963", "New Test Owner", "8410257024", 1,None, 2,3, "Plot is Already Allocated!!!",0),
        (None,"Test Tenant","841025702","abc","8410257024",None,None,None,None, "Invalid Phone Number!!!",3),
    ])
    def test_update_tenant_negative(self,old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no, expected_output, tenant_id,capsys):

        input_values = [old_tenant_name, new_tenant_name, phone_number, owner_name, owner_contact, task_choice, plot_choice, floor_no, plot_no]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                update_tenant(tenant_id)
                captured = capsys.readouterr()
                print(captured.out)
            assert str(e.value) == expected_output

        captured = capsys.readouterr()
        print(captured.out)




class TestUpdateUser:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, new_user_name, phone_number, expected_output, tenant_id",[
        ("Update User","41","Update Me","9903888298",[41,"Update Me",9903888298],0),
        ("Update Me","41","Update User","9903888298",[41,"Update User",9903888298],3)
    ])
    def test_update_user_positive(self,user_name, user_id, new_user_name, phone_number, expected_output, tenant_id):

        input_values = [user_name, user_id, new_user_name, phone_number]
        
        with patch('builtins.input', side_effect=input_values):
            update_user(tenant_id)

        output=[]
        added_tenant = session.scalars(select(UserList).filter(UserList.user_name==new_user_name, UserList.user_id == user_id)).first()
        output.append(added_tenant.user_id)
        output.append(added_tenant.user_name)
        output.append(added_tenant.user_phone_number)
        assert output==expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, new_user_name, phone_number, expected_output, tenant_id",[
        ("Update User","9903888298",None,None,"Wrong ID!!!",3),
        ("Update User",None,None,None,"No user found with name Update User. Please check and try again.",17),#the user is not with the tenant
        ("",None,None,None,"User name cannot be empty.",0),
        ("Alph@",None,None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("Update User","abc",None,None,"Please enter valid integer values for User Id and phone number",0),
        ("Update User","41","","9903888298","Empty fields can't be stored in the database.",0),
        ("Update User","41","Upd@te Me","9903888298","User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("Update User","41","Update Me","alpha","Please enter valid integer values for User Id and phone number",0),
        ("Update User","41","Update User","9876543210","Phone number already exists in the database.",3),
        ("Update User","41","Update User","987654321","Invalid Phone Number!!!",3),
    ])
    def test_update_user_negative(self,user_name, user_id, new_user_name, phone_number, expected_output, tenant_id):

        input_values=[user_name, user_id, new_user_name, phone_number]
        
        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                update_user(tenant_id)
            assert  str(e.value) == expected_output




class TestTransferUser:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, new_tenant_id, expected_output",[
        ("Update User","41","68",68),
        ("Update User","41","3",3)
    ])
    def test_transfer_user_positive(self,user_name, user_id, new_tenant_id,expected_output):

        input_values = [user_name, user_id, new_tenant_id]

        with patch('builtins.input', side_effect=input_values):
            transfer_user()

        added_tenant = session.scalars(select(UserList.tenant).filter(UserList.user_name==user_name, UserList.user_id == user_id)).first()
        assert added_tenant == expected_output




    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, new_tenant_id, expected_output",[
        ("Update User","17",None,"Wrong ID!!!"),
        ("Upda",None,None,"No user found with name Upda. Please check and try again."),
        ("",None,None,"User name cannot be empty."),
        ("Upd@te",None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Update User","abc",None,"Please enter valid integer values for User Id and Tenant Id"),
        ("Update User","41","abc","Please enter valid integer values for User Id and Tenant Id"),
        ("Update User","",None,"Please enter valid integer values for User Id and Tenant Id"),
        ("Update User","41","","Please enter valid integer values for User Id and Tenant Id"),
    ])
    def test_transfer_user_negative(self,user_name, user_id, new_tenant_id,expected_output):

        input_values = [user_name, user_id, new_tenant_id]

        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                transfer_user()
            assert str(e.value) == expected_output




#Change the Expected Output format for Positive Results
class TestAssignRevokeRole:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, task_choice, role_id, expected_output, tenant_id",[
        ("Update User","41","1","8",8,0),
        ("Update User","41","2",None,None,0),
        ("Update User","41","1","8",8,3),
        ("Update User","41","3","25",25,0),
        ("Update User","41","3","25",25,3),
        ("Update User","41","2",None,None,3)
    ])
    def test_assign_revoke_role_positive(self,user_name, user_id, task_choice, role_id, expected_output, tenant_id):

        input_values = [user_name, user_id, task_choice, role_id]
        while None in input_values:
            input_values.remove(None)
        
        with patch('builtins.input', side_effect=input_values):
            assign_revoke_role(tenant_id)

        role_assigned = session.scalars(select(UserRole.role_id).filter(UserRole.user_id == user_id)).first()
        assert role_assigned == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, task_choice, role_id, expected_output, tenant_id",[
        ("Update User","41","2",None,"Cant remove or replace roles when No Role Assigned",0),
        ("Update User","41","3",None,"Cant remove or replace roles when No Role Assigned",0),
        ("Test Dummy User","7","1","8","Already has a role can't assign another one.",0),
        ("",None,None,None,"User name cannot be empty.",0),
        ("Upd@te User",None,None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("Update User","",None,None,"Please enter valid integer values for User Id, Choice and Role Id",0),
        ("Update User","41","",None,"Please enter valid integer values for User Id, Choice and Role Id",0),
        ("Update User","41","1","abc","Please enter valid integer values for User Id, Choice and Role Id",0),
        ("Update User","41","1","58000","Wrong Role ID!!!",0),
    ])
    def test_assign_revoke_role_negative(self,user_name, user_id, task_choice, role_id, expected_output, tenant_id):

        input_values = [user_name, user_id, task_choice, role_id]
        while None in input_values:
            input_values.remove(None)
        
        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                assign_revoke_role(tenant_id)
            assert str(e.value) == expected_output





class TestAddRemovePermissionFromRole:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("role_name, task_choice, permission_id, expected_output",[
        ("Admin","1","1",1),
        ("Admin","2","1",None)
    ])
    def test_add_remove_permission_from_role_positive(self,role_name, task_choice, permission_id, expected_output):

        input_values = [role_name, task_choice, permission_id]

        with patch('builtins.input', side_effect=input_values):
            add_remove_permission_from_role()


        permission_assigned = session.scalars(select(RolePermission.permission_id).filter(RolePermission.role_id == 25, RolePermission.permission_id == permission_id)).first()
        assert permission_assigned == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("role_name, task_choice, permission_id, expected_output",[
        ("",None,None,"Role name cannot be empty."),
        ("Upd@te",None,None,"Role name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("No Deleting","",None,"Please enter valid integer values for Choice and Permission Id"),
        ("No Deleting","1","abc","Please enter valid integer values for Choice and Permission Id"),
        ("No Deleting","1","58000","Wrong Permission ID!!!"),
        ("No Deleting","1","2","This Permission is already assigned"),
        ("No Deleting","2","1","The Permission is not Assigned"),
        ("Admin","2",None,"Cant remove permissions when No permissions are Assigned"),
        ("Alpha",None,None,"No role found with name Alpha. Please check and try again."),
    ])
    def test_add_remove_permission_from_role_negative(self,role_name, task_choice, permission_id, expected_output):

        input_values = [role_name, task_choice, permission_id]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                add_remove_permission_from_role()
            assert str(e.value) == expected_output





class TestAssignRevokeUserApplication:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, task_choice, application_id_to_replace, application_id, expected_output, tenant_id",[
        ("Update User","41","1",None,"25",25,0),
        ("Update User","41","1",None,"7",7,0),
        ("Update User","41","3","25","45",45,0),
        ("Update User","41","2",None,"45",None,3),
        ("Update User","41","2",None,"7",None,3),
    ])
    def test_assign_revoke_user_application_positive(self,user_name, user_id, task_choice, application_id_to_replace, application_id, expected_output, tenant_id):

        input_values = [user_name, user_id, task_choice, application_id_to_replace, application_id,]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            assign_revoke_user_application(tenant_id)


        application_assigned = session.scalars(select(UserApplication.application_id).filter(UserApplication.application_id == application_id, UserApplication.user_id == user_id)).first()
        assert application_assigned == expected_output


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, user_id, task_choice, application_id_to_replace, application_id, expected_output, tenant_id",[
        ("",None,None,None,None,"User name cannot be empty.",0),
        ("Upd@te User",None,None,None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
        ("Update User","",None,None,None,"Please enter valid integer values for User Id, Choice and Application Id",0),
        ("Update User","abc",None,None,None,"Please enter valid integer values for User Id, Choice and Application Id",0),
        ("Update User","41","",None,None,"Please enter valid integer values for User Id, Choice and Application Id",0),
        ("Test Dummy Owner","5","1",None,"25","Already has The Application Access!!!",3),
        ("Update User","41","1",None,"58000","Wrong Application ID!!!",0),
        ("Test Dummy Owner","5","3","25","7","Already has The Application Access!!!",0),
        ("Test Dummy Owner","5","2",None,"58000","Wrong Application ID!!!",0),
        ("Update User","41","2",None,None,"Cant remove or replace applications when No applications Assigned",3),
        ("Update User","41","3",None,None,"Cant remove or replace applications when No applications Assigned",3),
        ("ALPHA GAMA",None,None,None,None,"No user found with name ALPHA GAMA. Please check and try again.",0),
    ])
    def test_assign_revoke_user_application_negative(self,user_name, user_id, task_choice, application_id_to_replace, application_id, expected_output, tenant_id,capsys):

        input_values = [user_name, user_id, task_choice, application_id_to_replace, application_id]
        while None in input_values:
            input_values.remove(None)


        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                assign_revoke_user_application(tenant_id)
                captured = capsys.readouterr()
                print(captured.out)
            assert str(e.value) == expected_output
     




class TestAssignRevokeRoleTenant:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("tenant_name, task_choice, role_id_to_replace, role_id, expected_output",[
        ("Testing-Tenant","1",None,"25",25),
        ("Testing-Tenant","1",None,"8",8),
        ("Testing-Tenant","2",None,"8",None),
        ("Testing-Tenant","3","25","8",8),
        ("Testing-Tenant","2",None,"8",None),
    ])
    def test_assign_revoke_role_tenant_positive(self,tenant_name, task_choice, role_id_to_replace, role_id, expected_output):

        input_values = [tenant_name, task_choice, role_id_to_replace, role_id]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            assign_revoke_role_tenant()


        role_assigned = (session.scalars(select(RoleTenant.roles_available)
                        .filter(RoleTenant.roles_available == role_id, 
                                RoleTenant.tenant_id == (session.scalars(select(TenantList.tenant_id)
                                                        .filter_by(tenant_name=tenant_name))
                                                        .first())))
                                    .first())
        assert role_assigned == expected_output





    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("tenant_name, task_choice, role_id_to_replace, role_id, expected_output",[
        ("",None,None,None,"Tenant name cannot be empty."),
        ("Test Ten@nt",None,None,None,"Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Test Tenant","",None,None,"Please enter valid integer values for Choice and Role Id"),
        ("Test Tenant","1",None,"abc","Please enter valid integer values for Choice and Role Id"),
        ("Test Tenant","1",None,"25","Already has The role Access!!!"),
        ("Test Tenant","1",None,"58000","Wrong Role ID!!!"),
        ("Test Tenant","2",None,"58000","Wrong Role ID!!!"),
        ("Test Tenant","3","25","8","Already has The role Access!!!"),
        ("Test Tenant","3",None,"58000","Wrong Role ID!!!"),
        ("Test Tenant","3","25","45","Wrong Role ID!!!"),
        ("Test Tenant","3","25","","Please enter valid integer values for Choice and Role Id"),
        ("Testing-Tenant","2",None,None,"Cant remove or replace roles when No roles Assigned"),
        ("Testing-Tenant","3",None,None,"Cant remove or replace roles when No roles Assigned"),
        ("Test",None,None,None,"No Tenant found with name Test. Please check and try again.")
    ])
    def test_assign_revoke_role_tenant_negative(self,tenant_name, task_choice, role_id_to_replace, role_id, expected_output):

        input_values = [tenant_name, task_choice, role_id_to_replace, role_id]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                assign_revoke_role_tenant()
            assert str(e.value) == expected_output







class TestUpdateApplicationPermission:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("application_name, task_choice, permission_id, expected_output",[
        ("AAATest","1","2",2),
        ("AAATest","1","1",1),
        ("AAATest","2","2",None),
        ("AAATest","2","1",None)
    ])
    def test_update_application_permission_positive(self,application_name, task_choice, permission_id, expected_output):

        input_values = [application_name, task_choice, permission_id]
        
        with patch('builtins.input', side_effect=input_values):
            update_application_permission()

        permission_assigned = (session.scalars(select(ApplicationPermission.permission_id)
                        .filter(ApplicationPermission.permission_id == permission_id,
                                ApplicationPermission.application_id == (session.scalars(select(Application.application_id)
                                                        .filter_by(application_name=application_name))
                                                        .first())))
                                                        .first())
        assert permission_assigned == expected_output




    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("application_name, task_choice, permission_id, expected_output",[
        ("",None,None,"Application name cannot be empty."),
        ("Test Ten@nt",None,None,"Application name can only contain uppercase and lowercase letters, spaces, and hyphens."),
        ("Test Beta","",None,"Please enter valid integer values for Choice and Permission Id"),
        ("Test Beta","1","abc","Please enter valid integer values for Choice and Permission Id"),
        ("Test Beta","1","2","This Permission is already assigned"),
        ("Test Beta","1","58000","Wrong Permission ID!!!"),
        ("Test Beta","2","58000","Wrong Permission ID!!!"),
        ("AAATest","2",None,"Cant remove permissions when No permissions are Assigned"),
        ("Alpha",None,None,"No application found with name Alpha. Please check and try again."),
    ])
    def test_update_application_permission_negative(self, application_name, task_choice, permission_id, expected_output):

        input_values = [application_name, task_choice, permission_id]
        while None in input_values:
            input_values.remove(None)
        
        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                update_application_permission()
            assert  str(e.value) == expected_output





#Setup for testing updating own user details functionality
@pytest.fixture(scope="class")
def setup_login_database():
    #setup process
    input_values = ["Test Dummy User",7,"TDU","123"]
    tenant_id = 0

    with patch('builtins.input', side_effect = input_values):
        set_username_password(tenant_id)

    yield

    #teardownprocess
    input_values = ["Test Dummy User",7,"yes"]
    
    with patch('builtins.input', side_effect = input_values):
            delete_username_password(tenant_id)
    
class TestUpdateOwnUserDetails:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("user_name, phone_number, expected_output, login_username",[
        ("Test Dummy","7742158860",["Test Dummy",7742158860],"TDU"),
        ("Test Dummy User","7741158860",["Test Dummy User",7741158860],"TDU")
    ])
    def test_update_own_user_details(self,setup_login_database,user_name, phone_number, expected_output, login_username):

        input_values = [user_name, phone_number]

        with patch('builtins.input', side_effect=input_values):
            update_own_user_details(login_username)

        output = []

        details = session.execute(select(LoginDetail,UserList).filter_by(user_name = login_username).join(UserList,UserList.user_id == LoginDetail.user_id)).first()
        _, user = details

        

        output.append(user.user_name)
        output.append(user.user_phone_number)
        assert output == expected_output


    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("user_name, phone_number, expected_output, username",[
        ("",None,"User name cannot be empty.","TDU"),
        ("Test Dum153my",None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.","TDU"),
        ("Test Dummy","abc","Please enter valid integer values for User Phone Number","TDU"),
        ("Test Dummy User","9903888298","Phone number already exists in the database.","TDU"),
        ("Test Dummy User","990388828","Invalid Phone Number!!!","TDU")
    ])
    def test_update_own_user_details_(self, setup_login_database, user_name, phone_number, expected_output, username):

        input_values = [user_name, phone_number]

        with patch('builtins.input', side_effect=input_values):
            with pytest.raises(ValueError) as e:
                update_own_user_details(username)
            assert  str(e.value) == expected_output

        




#Setup for testing deletion of username and password functionality
@pytest.fixture(scope="class")
def setup_login_database_for_deletion():
    #setup process
    input_values = [["Test Dummy User",7,"TDU","123"],["Test Dummy Owner",5,"TDO","123"]]
    tenant_id = 0

    for input_value in input_values:
        with patch('builtins.input', side_effect = input_value):
            set_username_password(tenant_id)

#For Alphabetic execution of Test Files. It should be in Login_test.py
class TestDeleteUsernamePassword:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("username, user_id, confirmation, expected_output, tenant_id",[
        ("Test Dummy User",7,"yes",None,0),
        ("Test Dummy Owner",session.scalars(select(UserList.user_id).filter_by(user_name="Test Dummy Owner")).first(),"yes",None,3),
    ])
    def test_delete_username_password_positive(self,setup_login_database_for_deletion,username, user_id, confirmation,expected_output,tenant_id):

        input_values = [username, user_id, confirmation]

        with patch('builtins.input', side_effect = input_values):
            delete_username_password(tenant_id)


        user_details = session.scalars(select(UserList).filter(UserList.user_id == input_values[1])).first()
        login_details = session.scalars(select(LoginDetail).filter_by(user_id = user_details.user_id)).first()

        assert login_details == expected_output



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("username, user_id, confirmation, expected_output, tenant_id",[
        ("Test Dummy User",None,None,"No User with the given username",6),
        ("Test Dummy Owner",session.scalars(select(UserList.user_id).filter_by(user_name="Test Dummy Owner")).first(),None,"User has no Login Detail!!!",3),
        ("Test Dummy User","555",None,"Wrong User ID!!!",3),
        ("Test Dummy User",47,"no","Deletion Cancelled!!!",3),
        ("",None,None,"User name cannot be empty.",0),
        ("Test @123",None,None,"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0),
    ])
    def test_delete_username_password_negative(self,username, user_id, confirmation,expected_output,tenant_id):

        input_values = [username, user_id, confirmation]
        while None in input_values:
            input_values.remove(None)

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                delete_username_password(tenant_id)
            assert str(e.value) == expected_output

