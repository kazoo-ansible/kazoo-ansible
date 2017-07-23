import pytest
import sup
import subprocess
from unittest import TestCase
from unittest.mock import Mock
@pytest.fixture
def process():
    sup.process = Mock(spec=sup.process)
    sup.process.call_process.side_effect = [(0, '', '')]
    return sup.process

class TestProcess:
    def test_call_process(self):
        process = sup.Process()
        exitcode, stdout, stderr = process.call_process(['echo', 'test'])

        assert exitcode == 0
        assert stdout == 'test\n'
        assert stderr == ''

class TestSup:
    def test_get_sbc_acls_returns_acl_ips(self, process):
        out = """+--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+
        | Name                           | CIDR               | List          | Type  | Authorizing Type | ID                               |
        +================================+===================+===============+=======+==================+==================================+
        | 192.168.1.153                  | 192.168.1.153/32   | authoritative | allow | system_config    |                                  |
        +--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+"""

        process.call_process.side_effect = [(0, out, '')]

        acls = sup.get_sbc_acls('cookie')
        assert acls == ['192.168.1.153']

    def test_get_acls_returns_empty_acl_list(self, process):
        process.call_process.side_effect = [(0, '', '')]

        acls = sup.get_sbc_acls('cookie')

        assert acls == []

    def test_get_carrier_acls_executes_sup_command(self, process):
        sup.get_carrier_acls('cookie')
        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'carrier_acls', 'acl_summary'])

    def test_get_sbc_acls_executes_sup_command(self, process):
        sup.get_sbc_acls('cookie')
        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls', 'acl_summary'])

    def test_get_acls_includes_cookie(self, process):
        sup.get_sbc_acls('newcookie')
        process.call_process.assert_called_once_with(['sup', '-c', 'newcookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls', 'acl_summary'])

    def test_get_acls_exception_on_error(self, process):
        process.call_process.side_effect = [(10, 'stdout', 'stderr')]

        with pytest.raises(IOError) as err:
            sup.get_sbc_acls('cookie')
            assert 'stderr' in str(err.value)

    def test_add_carrier_acl_adds_carrier_acl(self, process):
        out = """updating authoritative ACLs 192.168.1.153(192.168.1.153/32) to allow traffic
        issued reload ACLs to freeswitch@kazoo.lan"""
        process.call_process.side_effect = [(0, out, '')]

        sup.add_carrier_acl('cookie', '192.168.1.153')

        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'allow_carrier', '192.168.1.153', '192.168.1.153'])

    def test_add_sbc_acl_adds_sbc_acl(self, process):
        out = """updating authoritative ACLs 192.168.1.153(192.168.1.153/32) to allow traffic
        issued reload ACLs to freeswitch@kazoo.lan"""
        process.call_process.side_effect = [(0, out, '')]

        sup.add_sbc_acl('cookie', '192.168.1.153')

        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'allow_sbc', '192.168.1.153', '192.168.1.153'])

    def test_remove_carrier_acl_removes_sbc_acl(self, process):
        out = """+--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+
        | Name                           | CIDR               | List          | Type  | Authorizing Type | ID                               |
        +================================+===================+===============+=======+==================+==================================+
        | 192.168.1.1                    | 192.168.1.1/32     | authoritative | allow | system_config    |                                  |
        +--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+"""
        
        process.call_process.side_effect = [(0, out, ''), (0, '', '')]

        sup.remove_carrier_acl('cookie', '192.168.1.1')

        process.call_process.assert_called_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'remove_acl', '192.168.1.1'])
    
    def test_remove_sbc_acl_removes_sbc_acl(self, process):
        out = """+--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+
        | Name                           | CIDR               | List          | Type  | Authorizing Type | ID                               |
        +================================+===================+===============+=======+==================+==================================+
        | 192.168.1.1                    | 192.168.1.1/32     | authoritative | allow | system_config    |                                  |
        +--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+"""
        
        process.call_process.side_effect = [(0, out, ''), (0, '', '')]

        sup.remove_sbc_acl('cookie', '192.168.1.1')

        process.call_process.assert_called_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'remove_acl', '192.168.1.1'])

    def test_get_fs_nodes_returns_fs_nodes(self, process):
        process.call_process.side_effect = [(0, 'freeswitch@kazoo.lan\nfreeswitch@kazoo2.lan', '')]

        fs_nodes = sup.get_fs_nodes('cookie')

        assert fs_nodes == ['kazoo.lan', 'kazoo2.lan']

    def test_add_fs_node_adds_fs_node(self, process):
        process.call_process.side_effect = [(0, 'ok', '')]

        sup.add_fs_node('cookie', 'kazoo.lan')

        process.call_process.assert_called_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'add_fs_node', 'freeswitch@kazoo.lan'])

    def test_add_fs_node_handles_duplicates(self, process):
        process.call_process.side_effect = [(1, '{error,node_exists}\n', '')]

        sup.add_fs_node('cookie', 'kazoo.lan')

    def test_remove_fs_node_removes_fs_node(self, process):
        process.call_process.side_effect = [(0, 'ok\n', '')]

        sup.remove_fs_node('cookie', 'kazoo.lan')

    def test_import_media_imports_media(self, process):
        process.call_process.side_effect = [(0, '', '')]

        sup.import_media('cookie')

        process.call_process.assert_called_with(['sup', '-c', 'cookie', '-n', 'kazoo_apps', 'kazoo_media_maintenance', 'import_prompts', '/opt/kazoo/sounds/en/us/'])

