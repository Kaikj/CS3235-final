# Web Socket test for [CRASH][crash]

A web socket server and client test for [CRASH][crash]

## Protocol

### Server

1. `onConnect`: store handler to the client in a list
2. `onOpen` from 127.0.0.1: start authenticating clients in the list via [CRASH][crash] protocol
3. `onAuthSuccess`: send the url of the page to be opened

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

[crash]: https://github.com/Kaikj/CRASH
