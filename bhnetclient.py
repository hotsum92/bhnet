import sys
import socket
import getopt
import threading
import subprocess

def create_client():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def str_to_byte(value):
    return value.encode('utf-8')

def byte_to_str(value):
    return value.decode('utf-8')


def usage():
    print('BHP Net Client Tool')
    print('Usage: bhnet.py -t target_host -p port')
    print
    print(' Examples:')
    print('bhnetclient.py -t 192.168.0.1 -p 5555')
    sys.exit(0)

def args(argv):

    opts, args = getopt.getopt(
            argv[1:],
            'hle:t:p:cu:',
            ['help', 'target=', 'port='])

    help = False
    port = 0
    target = 'localhost'

    for o, a in opts:
        if o in ('-h', '--help'):
            help = True
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-t', '--target'):
            target = a
        else:
            assert False, 'Unhandled Option'

    return help, port, target

def client_sender(
        port,
        target,
        forever=True,
        create_client=create_client
        ):

    client = create_client()
    client.connect((target, port))

    while True:
        response = b''

        while True:
            data = client.recv(4096)
            response+= data

            if len(data) < 4096:
                 break

        print(byte_to_str(response), end='')

        buffer = input('')
        buffer+= '\n'

        client.send(str_to_byte(buffer))

        if not forever:
            break

def main():

    help, port, target = args(sys.argv)

    if help:
        usage()
    else:
        threading.Thread(target=client_sender, args=(port, target)).start()

if __name__ == '__main__':
    main()
