import os
import pytest
import serial

from python.config import SERIAL_PORT, BAUDRATE, TIMEOUT_S


def pytest_addoption(parser):
    parser.addoption("--port", action="store", default=SERIAL_PORT)


@pytest.fixture(scope="session")
def mcu_serial(pytestconfig):
    port = pytestconfig.getoption("--port")

    # Allow running tests without hardware connected
    if not os.path.exists(port):
        pytest.skip(f"Serial port not found: {port}")

    ser = serial.Serial(port, BAUDRATE, timeout=TIMEOUT_S)
    yield ser
    ser.close()
