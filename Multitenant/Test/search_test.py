import pytest
from unittest.mock import patch, Mock
from db.search import search_tenant,search_user, search_roles, search_permissions
from db.database import session
from db.models import TenantList
from sqlalchemy import select

class  TestSearchTenant:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("Test Tenant",1),
    ])
    def test_search_tenant_positive(self,input_values, expected_output, capsys):
        
        with patch('builtins.input', return_value = input_values):
            search_tenant()

        captured = capsys.readouterr()


        tenant_data = session.scalars(select(TenantList).filter_by(tenant_name = "Test Tenant")).first()
        
        
        assert "Tenant ID 3   Tenant: Test Tenant  Phone Number: 8410257963" in captured.out
        assert "Owner Name: New Test Owner Owner Contact: 8410257024" in captured.out
        assert f"Total users of this Tenant: {tenant_data.user_count}" in captured.out
        assert "Plots Rented: " in captured.out
        assert "{'Floor': 2, 'Plot No.': 3}" in captured.out


    '''
        Negativetive Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("Failed Org","No such Tenant is present in our records."),
        ("","Tenant name cannot be empty."),
        ("Failed 0rg","Tenant name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_search_tenant_negative(self,input_values, expected_output):
        
        with patch('builtins.input', return_value = input_values):
            with pytest.raises(ValueError) as e:
                search_tenant()
            assert str(e.value) == expected_output





class TestSearchUser:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output, tenant_id",[
        (["Update User"],["User ID 41   User: Update User  Phone Number: 9903888298","Tenant ID: 3 Tenant Name: Test Tenant"],0),
        (["Test Dummy User"],["User ID 7   User: Test Dummy User  Phone Number: 7741158860","Tenant ID: 3 Tenant Name: Test Tenant"],3),
    ])
    def test_search_user_positive(self,input_values, expected_output, tenant_id, capsys):

        with patch('builtins.input', side_effect = input_values):
            search_user(tenant_id)

        captured = capsys.readouterr()

        for i in expected_output:
            assert i in captured.out



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output, tenant_id",[
        (["Test Dummy"],"No User is present in our records.",3),
        ([""],"User name cannot be empty.",0),
        (["Test Dummy 0wner"],"User name can only contain uppercase and lowercase letters, spaces, and hyphens.",0)
    ])
    def test_search_user_negative(self,input_values, expected_output, tenant_id):

        with patch('builtins.input', side_effect = input_values):
            with pytest.raises(ValueError) as e:
                search_user(tenant_id)
            assert str(e.value) == expected_output





class TestSearchRoles:


    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("No Deleting",["Role ID 8   Role: No Deleting  Role Description: Testing","Permission ID 2   Permission: No Deleting  Permission Description: Testing EveryThing"])
    ])
    def test_search_roles_positive(self,input_values, expected_output, capsys):

        with patch('builtins.input', return_value = input_values):
            search_roles()

        captured = capsys.readouterr()

        for i in expected_output:
            assert i in captured.out



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("Nope","No Role is present in our records."),
        ("","Role name cannot be empty."),
        ("Failed 0rg","Role name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_search_roles_negative(self,input_values, expected_output):

        with patch('builtins.input', return_value = input_values):
            with pytest.raises(ValueError) as e:
                search_roles()
            assert  str(e.value) == expected_output





class TestSearchPermissions:

    '''
        Positive Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("No Deleting","Permission ID 2   Permission: No Deleting  Permission Description: Testing EveryThing")
    ])
    def test_search_permissions_positive(self,input_values, expected_output, capsys):

        with patch('builtins.input', return_value = input_values):
            search_permissions()

        captured = capsys.readouterr()


        assert expected_output in captured.out



    '''
        Negative Scenarios
    '''
    @pytest.mark.parametrize("input_values, expected_output",[
        ("Nope","No Permission is present in our records."),
        ("","Permission name cannot be empty."),
        ("Failed 0rg","Permission name can only contain uppercase and lowercase letters, spaces, and hyphens.")
    ])
    def test_search_permissions_negative(self,input_values, expected_output, capsys):

        with patch('builtins.input', return_value = input_values):
            with pytest.raises(ValueError) as e:
                search_permissions()
            assert str(e.value) == expected_output




