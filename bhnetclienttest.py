import unittest
from unittest.mock import MagicMock
import bhnetclient

class BhnetServerTest(unittest.TestCase):

    def test_args(self):

        help   = False
        port   = 0
        target = 'localhost'

        args = [
            ['', '-h'],
            ['', '--help'],
            ['', '-p',       '22'],
            ['', '--port',   '200'],
            ['', '-t',       '172.0.0.1'],
            ['', '--target', '172.0.0.1'],
        ]

        expected = [
            (True, port, target),
            (True, port, target),
            (help, 22,   target),
            (help, 200,  target),
            (help, port, '172.0.0.1'),
            (help, port, '172.0.0.1'),
        ]

        for i in range(len(expected)):
            result = bhnetclient.args(args[i])

            self.assertEqual(
                result, expected[i],
                'Item {0} {1} != {2}'.format(i, result, expected[i])
            )

    def test_client_handler(self):

        create_client = unittest.mock.MagicMock()
        client = unittest.mock.MagicMock()
        socket = unittest.mock.MagicMock()

        create_client.return_value = client
        client.accept.return_value = socket

        socket.recv.return_value = b'\n'

        bhnetclient.client_sender(
            0,
            'localhost',
            forever=False,
            create_client=create_client
        )


if __name__ == '__main__':
    unittest.main()
