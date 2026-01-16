# HW–SW Contract (v0)

## Transport
- UART 115200 8N1
- Commands and responses are single-line ASCII terminated by '\n'
- One command -> one response (single line)

## Commands
- PING -> PONG
- STATUS -> READY
- ECHO:<text> -> ECHO:<text>

## Errors
- ERR:<reason> (single line)
