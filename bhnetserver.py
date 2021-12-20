import sys
import socket
import getopt
import threading
import subprocess

def run_command(command):
    return subprocess.check_output(
            command, stderr=subprocess.STDOUT, shell=True)

def create_server():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def str_to_byte(value):
    return value.encode('utf-8')

def byte_to_str(value):
    return value.decode('utf-8')

def usage():
    print('BHP Net Server Tool')
    print('Usage: bhnet.py -p port')
    print
    print(' Examples:')
    print('bhnet.py -p 5555')
    sys.exit(0)

def args(argv):

    opts, args = getopt.getopt(
            argv[1:],
            'hle:t:p:cu:',
            ['help', 'port='])

    help = False
    port = 0

    for o, a in opts:
        if o in ('-h', '--help'):
            help = True
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'

    return help, port

def client_handler(
        port,
        forever=True,
        run_command=run_command,
        create_server=create_server
    ):

    target = '0.0.0.0'
    prompt = '<BHP:#> '

    server = create_server()
    server.bind((target, port))

    server.listen(5)

    print('started to listen %i port' % port)

    client_socket, addr = server.accept()
    print('socket connected')
    client_socket.send(str_to_byte(prompt))

    while True:
        buffer = b''
        while b'\n' not in buffer:
            buffer+= client_socket.recv(1024)

        buffer.rstrip()
        response = run_command(byte_to_str(buffer))
        response+= str_to_byte(prompt)

        client_socket.send(response)

        if not forever:
            break

def main():

    help, port = args(sys.argv)

    if help:
        usage()
    else:
        threading.Thread(target=client_handler, args=(port,)).start()

if __name__ == '__main__':
    main()
