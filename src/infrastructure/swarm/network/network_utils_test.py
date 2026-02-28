# Auto-synced test for infrastructure/swarm/network/network_utils.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "network_utils.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "get_ip"), "get_ip missing"
    assert hasattr(mod, "get_loopback_ip"), "get_loopback_ip missing"
    assert hasattr(mod, "test_bind"), "test_bind missing"
    assert hasattr(mod, "get_hostname"), "get_hostname missing"
    assert hasattr(mod, "get_fqdn"), "get_fqdn missing"
    assert hasattr(mod, "resolve_hostname"), "resolve_hostname missing"
    assert hasattr(mod, "is_valid_ipv6_address"), "is_valid_ipv6_address missing"
    assert hasattr(mod, "is_valid_ipv4_address"), "is_valid_ipv4_address missing"
    assert hasattr(mod, "is_valid_ip_address"), "is_valid_ip_address missing"
    assert hasattr(mod, "normalize_ip"), "normalize_ip missing"
    assert hasattr(mod, "split_host_port"), "split_host_port missing"
    assert hasattr(mod, "join_host_port"), "join_host_port missing"
    assert hasattr(mod, "get_open_port"), "get_open_port missing"
    assert hasattr(mod, "get_open_ports"), "get_open_ports missing"
    assert hasattr(mod, "is_port_open"), "is_port_open missing"
    assert hasattr(mod, "wait_for_port"), "wait_for_port missing"
    assert hasattr(mod, "find_process_using_port"), "find_process_using_port missing"
    assert hasattr(mod, "get_tcp_uri"), "get_tcp_uri missing"
    assert hasattr(mod, "get_distributed_init_method"), "get_distributed_init_method missing"
    assert hasattr(mod, "parse_uri"), "parse_uri missing"
    assert hasattr(mod, "get_zmq_ipc_path"), "get_zmq_ipc_path missing"
    assert hasattr(mod, "get_zmq_inproc_path"), "get_zmq_inproc_path missing"
    assert hasattr(mod, "close_zmq_sockets"), "close_zmq_sockets missing"
    assert hasattr(mod, "zmq_socket_context"), "zmq_socket_context missing"
    assert hasattr(mod, "create_zmq_context"), "create_zmq_context missing"
    assert hasattr(mod, "create_async_zmq_context"), "create_async_zmq_context missing"
    assert hasattr(mod, "get_network_interfaces"), "get_network_interfaces missing"
    assert hasattr(mod, "get_primary_interface"), "get_primary_interface missing"
    assert hasattr(mod, "HAS_ZMQ"), "HAS_ZMQ missing"

