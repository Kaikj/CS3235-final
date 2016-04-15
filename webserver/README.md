# WebSocket Server for [CRASH][crash]

A websocket server and client test for [CRASH][crash] (Confined Room Authentication System for/by Hugh)

## Protocol

### Server

1. `onOpen`: queue the client for authentication. It is managed by Python's `threading.Lock` object
2. On `Lock` acquire: send `g` (generator) and `p` (prime) to the client
3. On "turn_ready" message from client:
    * Send `g` and `p` to the "VIP" in the room to enable the authentication protocol
3. On receiving back `sharedValue`/`sharedKey` from VIP: do nothing for now

### Client

There are 2 versions of client. One is browser-based (here), the other one is just a websocket (in the client/ directory)

1. `onmessage` "g=xxx" and "p=xxx": invoke [CRASH][crash] protocol. Replies "turn_ready"

### Run

1. `python -m webserver` (from project's root directory)
2. Open browser, URL: http://localhost:8080/webserver/
    * To simulate multiple client, the URL above can be opened in multiple tabs.
3. When `g` and `p` values are received (it will be logged), send "turn_ready" message without the quotes

[crash]: https://github.com/Kaikj/CRASH
