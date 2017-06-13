import pytest
import sup
import subprocess
from unittest import TestCase
from unittest.mock import Mock

out = """+--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+
        | Name                           | CIDR               | List          | Type  | Authorizing Type | ID                               |
        +================================+===================+===============+=======+==================+==================================+
        | 192.168.1.153                  | 192.168.1.153/32   | authoritative | allow | system_config    |                                  |
        +--------------------------------+-------------------+---------------+-------+------------------+----------------------------------+"""

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
        process.call_process.side_effect = [(0, out, '')]

        acls = sup.get_sbc_acls('cookie')
        assert acls == ['192.168.1.153']

    def test_get_sbc_acls_returns_empty_acl_list(self, process):
        process.call_process.side_effect = [(0, '', '')]

        acls = sup.get_sbc_acls('cookie')

        assert acls == []

    def test_get_sbc_acls_executes_sup_command(self, process):
        sup.get_sbc_acls('cookie')
        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls', 'acl_summary'])

    def test_get_sbc_acls_includes_cookie(self, process):
        sup.get_sbc_acls('newcookie')
        process.call_process.assert_called_once_with(['sup', '-c', 'newcookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'sbc_acls', 'acl_summary'])

    def test_get_sbc_acls_exception_on_error(self, process):
        process.call_process.side_effect = [(10, 'stdout', 'stderr')]

        with pytest.raises(IOError) as err:
            sup.get_sbc_acls('cookie')
            assert 'stderr' in str(err.value)

    def test_add_sbc_acl_adds_sbc_acl(self, process):
        out = """updating authoritative ACLs 192.168.1.153(192.168.1.153/32) to allow traffic
        issued reload ACLs to freeswitch@kazoo.lan"""
        process.call_process.side_effect = [(0, out, '')]

        sup.add_sbc_acl('cookie', '192.168.1.153')

        process.call_process.assert_called_once_with(['sup', '-c', 'cookie', '-n', 'ecallmgr', 'ecallmgr_maintenance', 'allow_sbc', '192.168.1.153', '192.168.1.153'])

