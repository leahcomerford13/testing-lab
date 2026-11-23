from scripts.validate_config import validate_config

PORT_ERR = "port must be between 1 and 65535"
INT_ERR = "interval_seconds must be a positive integer"
TIME_ERR = "timeout_seconds must be a positive number"
REL_ERR = "timeout_seconds must be less than interval_seconds"


def valid_config():
    return {
        "service": "Campus Status",
        "port": 443,
        "interval_seconds": 60,
        "timeout_seconds": 5,
    }


def test_valid_configuration_is_accepted():
    assert validate_config(valid_config()) == []


def test_port_zero_is_rejected():
    config = valid_config()
    config["port"] = 0
    assert PORT_ERR in validate_config(config)


def test_lowest_valid_port_is_accepted():
    config = valid_config()
    config["port"] = 1
    assert validate_config(config) == []


def test_highest_valid_port_is_accepted():
    config = valid_config()
    config["port"] = 65535
    assert validate_config(config) == []


def test_port_above_range_is_rejected():
    config = valid_config()
    config["port"] = 65536
    assert PORT_ERR in validate_config(config)


def test_interval_one_is_accepted():
    config = valid_config()
    config["interval_seconds"] = 1
    config["timeout_seconds"] = 0.5
    assert validate_config(config) == []


def test_interval_60_is_accepted():
    config = valid_config()
    config["interval_seconds"] = 60
    config["timeout_seconds"] = 5
    assert validate_config(config) == []


def test_interval_zero_is_rejected():
    config = valid_config()
    config["interval_seconds"] = 0
    config["timeout_seconds"] = 5
    assert INT_ERR in validate_config(config)


def test_interval_negative_is_rejected():
    config = valid_config()
    config["interval_seconds"] = -1
    config["timeout_seconds"] = 5
    assert INT_ERR in validate_config(config)


def test_interval_decimal_is_rejected():
    config = valid_config()
    config["interval_seconds"] = 1.5
    config["timeout_seconds"] = 0.5
    assert INT_ERR in validate_config(config)


def test_timeout_5_is_accepted():
    config = valid_config()
    config["timeout_seconds"] = 5
    assert validate_config(config) == []


def test_timeout_decimal_is_accepted():
    config = valid_config()
    config["timeout_seconds"] = 2.5
    assert validate_config(config) == []


def test_timeout_zero_is_rejected():
    config = valid_config()
    config["timeout_seconds"] = 0
    assert TIME_ERR in validate_config(config)


def test_timeout_negative_is_rejected():
    config = valid_config()
    config["timeout_seconds"] = -1
    assert TIME_ERR in validate_config(config)


def test_timeout_59_is_accepted():
    config = valid_config()
    config["timeout_seconds"] = 59
    assert validate_config(config) == []


def test_timeout_equal_to_interval_is_rejected():
    config = valid_config()
    config["timeout_seconds"] = 60
    assert REL_ERR in validate_config(config)


def test_timeout_above_interval_is_rejected():
    config = valid_config()
    config["timeout_seconds"] = 61
    assert REL_ERR in validate_config(config)
