import socket

orig_getaddrinfo = socket.getaddrinfo


def getaddrinfoIPv4(host, port, family=0, type=0, proto=0, flags=0):
    return orig_getaddrinfo(
        host=host, port=port, family=socket.AF_INET, type=type, proto=proto, flags=flags
    )
