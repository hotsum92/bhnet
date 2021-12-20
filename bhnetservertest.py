import unittest
from unittest.mock import MagicMock
import bhnetserver

class BhnetServerTest(unittest.TestCase):

    def test_args(self):

        help    = False
        port    = 0

        args = [
            ['', '-h'],
            ['', '--help'],
            ['', '-p',      '22'],
            ['', '--port',  '200']
        ]

        expected = [
            (True, port),
            (True, port),
            (help,   22),
            (help,  200)
        ]

        for i in range(len(expected)):
            result = bhnetserver.args(args[i])

            self.assertEqual(
                result, expected[i],
                'Item {0} {1} != {2}'.format(i, result, expected[i])
            )

    def test_client_handler(self):

        run_command = unittest.mock.MagicMock()
        run_command.return_value = b''

        create_server = unittest.mock.MagicMock()
        server = unittest.mock.MagicMock()
        socket = unittest.mock.MagicMock()

        create_server.return_value = server
        server.accept.return_value = socket

        socket.recv.return_value = b'\n'

        class TestException(Exception):
            pass

        send_counter = [0]
        def send(value):
            send_counter[0] += 1
            if(send_counter[0] > 1):
                raise TestException

        socket.send = send

        with self.assertRaises(TestException):
            bhnetserver.client_handler(
                0,
                run_command=run_command,
                create_server=create_server
            )


if __name__ == '__main__':
    unittest.main()
