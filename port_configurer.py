import jack, time, sys

def get_ports_containing(client, string):
    ret_ports = []
    try:
        for port in client.get_ports():
            if string.lower() in port.name.lower():
                ret_ports.append(port)
    except jack.JackError:
        return []
    return ret_ports

def attempt_disconnect(client, port1, port2, debug=False):
    try:
        client.disconnect(port1, port2)
        return True
    except:
        if debug:
            print("Port " + port1.name + " and port " + port2.name + " have no connection")
        return False

def attempt_connect(client, port1, port2, debug=False):
    try:
        client.connect(port1, port2)
        return True
    except:
        if debug:
            print("Port " + port1.name + " and port " + port2.name + " already connected")
        return False

def alsa_can_connect(client):
    alsa_ports = get_ports_containing(client, 'alsa-jack')
    if len(alsa_ports) < 2:
        return False
    sink_ports = get_ports_containing(client, 'sink')
    try:
        port_connectable = attempt_connect(client, sink_ports[0], alsa_ports[0])
    except IndexError:
        return False

    return port_connectable

def reconfigure_port_connections(client):
    alsa_ports = get_ports_containing(client, 'alsa-jack')
    sink_ports = get_ports_containing(client, 'sink')
    source_ports = get_ports_containing(client, 'source')
    capture_ports = get_ports_containing(client, 'capture')
    playback_ports = get_ports_containing(client, 'playback')
    
    attempt_disconnect(client, capture_ports[0], source_ports[0])
    attempt_disconnect(client, capture_ports[1], source_ports[1])
    attempt_disconnect(client, sink_ports[0], playback_ports[0])
    attempt_disconnect(client, sink_ports[1], playback_ports[1])
    attempt_disconnect(client, capture_ports[0], alsa_ports[0])
    attempt_disconnect(client, capture_ports[1], alsa_ports[1])
    
    attempt_connect(client, sink_ports[0], source_ports[0])
    attempt_connect(client, sink_ports[1], source_ports[1])
    attempt_connect(client, sink_ports[0], alsa_ports[0])
    attempt_connect(client, sink_ports[1], alsa_ports[1])

def main(argv):
    client = jack.Client('JackClient')
    client.activate()
    reconfigurations_needed = False

    #Watch for port to open
    while True:
        if alsa_can_connect(client):
            reconfigure_port_connections(client)
            
if __name__ == "__main__":
    main(sys.argv)
