import os
import pytest
import serial
import time

from python.config import SERIAL_PORT, BAUDRATE, TIMEOUT_S

def _sync_board(ser: serial.Serial) -> None:
    """
    Bring the board into a known state before running tests.

    Strategy:
      - wait a bit for any auto-reset on port open
      - flush any boot banner / junk
      - send STATUS a few times until we see READY
    """
    # Let ST-LINK finish resetting the MCU after opening the port
    time.sleep(0.5)

    # Clear banner + garbage
    ser.reset_input_buffer()

    for _ in range(5):
        ser.write(b"STATUS\n")
        line = ser.readline().decode(errors="ignore").strip()
        print("SYNC got:", repr(line))

        if not line:
            # nothing yet, try again
            continue

        if line == "READY":
            # we're in sync
            return

        # If we see ERR:UNKNOWN COMMAND or a banner line, just loop again

    # If you want to be strict, you can raise here:
    # raise RuntimeError("Failed to sync with board")
    # For now it's OK to just fall through and let tests fail loudly.
    return

def pytest_addoption(parser):
    parser.addoption("--port", action="store", default=SERIAL_PORT)


@pytest.fixture(scope="session")
def mcu_serial(pytestconfig):
    port = pytestconfig.getoption("--port")

    # Allow running tests without hardware connected
    if not os.path.exists(port):
        pytest.skip(f"Serial port not found: {port}")

    ser = serial.Serial(port, BAUDRATE, timeout=TIMEOUT_S)
    _sync_board(ser)

    ser.reset_input_buffer()

    yield ser
    ser.close()
