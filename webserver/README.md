# WebSocket Server for [CRASH][crash]

A websocket server and client test for [CRASH][crash] (Confined Room Authentication System for/by Hugh)

## Protocol

### Server

1. `onOpen`: queue the client for authentication. It is managed by Python's `threading.Lock` object
2. On `Lock` acquire: sends "yourTurn" message to the client
3. On "turn_ready" message from client:
    * Sends `generator`, `prime`, and `sharedValue` to the "VIP" in the room to enable the authentication protocol
3. On receiving back `sharedValue`/`sharedKey` from VIP: send to the client a  url of a page to be opened
    * Message is in the form "url:xxx"

### Client

1. `onmessage` "yourTurn": invoke [CRASH][crash] protocol. Replies "turn_ready"
2. `onmessage` "url:xxx": `window.open(xxx)`

### Run

1. `python server.py`
2. Open browser, URL: http://localhost:8080
    * To simulate multiple client, the URL above can be opened in multiple tabs.
3. When "yourTurn" message is received (it will be logged), send "turn_ready" message without the quotes

[crash]: https://github.com/Kaikj/CRASH
