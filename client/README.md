# Client programs

## VIP

### Protocol

1. Connect to webserver.
2. Upon receiving `g` and `p` from webserver, generate `a`, send g^a mod p through ultrasound
3. Upon receiving g^b mod p from client (via ultrasound), calculate shared key and send to webserver

### Run

1. Run webserver first (refer to webserver README)
2. `python vip.py`

## Normal Clients

### Protocol

1. Connect to webserver.
2. Upon receiving `g` and `p` from webserver, generate `b`
3. Upon receiving g^a mod p from VIP (via ultrasound), calculate shared key

### Run

1. Run webserver (refer to webserver README)
2. Run VIP (above)
3. `python client.py`
