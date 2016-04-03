# WebSocket Server for [CRASH][crash]

A websocket server and client test for [CRASH][crash]

## Protocol

### Server

1. `onOpen`: queue the client for authentication by returning `turn_promise`, a promise that the client will get its turn to authenticate. The promise will be fulfilled in a FIFO manner.
2. On `turn_promise` return: return `auth_promise`, a promise that the client will be authenticated. On another thread, start authenticating the client. Currently it just waits for 2 seconds to simulate the blocking due to authentication. Possible actual protocol:
    * Sends "yourTurn" message to the client
    * Sends some data to the "VIP" in the room to enable the authentication protocol (undecided)
    * Carry out the [CRASH][crash] UltraSound authentication protocol with that client
3. On `auth_promise` return: send the url of the page to be opened
    * Message is in the form "url:xxx"

### Client

1. `onmessage` "yourTurn": invoke [CRASH][crash] protocol
2. `onmessage` "url:xxx": `window.open(xxx)`

## Development

### Requirements

- Python 2.7

### Setup

1. `pip install -r requirements.txt`

### Run

1. `python CRASHserver.py`
2. Open browser, URL: http://localhost:8080
    * To simulate multiple client, the URL above can be opened in multiple tabs.

[crash]: https://github.com/Kaikj/CRASH
