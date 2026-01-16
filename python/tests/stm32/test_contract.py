def send_and_read(ser, cmd: str) -> str:
    ser.reset_input_buffer()
    ser.write((cmd + "\n").encode())
    return ser.readline().decode(errors="ignore").strip()


def test_ping(mcu_serial):
    assert send_and_read(mcu_serial, "PING") == "PONG"


def test_status(mcu_serial):
    assert send_and_read(mcu_serial, "STATUS") == "READY"


def test_echo(mcu_serial):
    payload = "I am a STM32 Nucleo F446RE"
    assert send_and_read(mcu_serial, f"ECHO:{payload}") == f"ECHO:{payload}"
