import sys
from spalloc import config
from spalloc import \
    ProtocolClient, ProtocolError, ProtocolTimeoutError, SpallocServerException

# The acceptable range of server version numbers
VERSION_RANGE_START = (0, 1, 0)
VERSION_RANGE_STOP = (2, 0, 0)


class Terminate(Exception):
    def __init__(self, code, message=None, *args):
        self._code = code
        if message is None:
            self._msg = None
        elif len(args):
            self._msg = message.format(*args)
        else:
            self._msg = message

    def exit(self):
        if self._msg is not None:
            sys.stderr.write(self._msg + "\n")
        sys.exit(self._code)


def version_verify(client, timeout):
    version = tuple(map(int, client.version(timeout=timeout).split(".")))
    if not (VERSION_RANGE_START <= version < VERSION_RANGE_STOP):
        raise Terminate(2, "Incompatible server version ({})",
                        ".".join(map(str, version)))


class Script(object):
    def __init__(self):
        self.clientFactory = ProtocolClient

    def get_parser(self, cfg):
        """Return a set-up instance of :py:class:`argparse.ArgumentParser`"""

    def verify_arguments(self, args):
        """Check the arguments for sanity and do any second-stage parsing\
        required."""

    def body(self, client, args):
        """How to do the processing of the script once a client has been\
        obtained and verified to be compatible."""

    def build_server_arg_group(self, server_args, cfg):
        server_args.add_argument(
            "--hostname", "-H", default=cfg["hostname"],
            help="hostname or IP of the spalloc server (default: %(default)s)")
        server_args.add_argument(
            "--port", "-P", default=cfg["port"], type=int,
            help="port number of the spalloc server (default: %(default)s)")
        server_args.add_argument(
            "--timeout", default=cfg["timeout"], type=float, metavar="SECONDS",
            help="seconds to wait for a response from the server (default: "
            "%(default)s)")

    def __call__(self, argv=None):
        cfg = config.read_config()
        parser = self.get_parser(cfg)
        server_args = parser.add_argument_group("spalloc server arguments")
        self.build_server_arg_group(server_args, cfg)
        args = parser.parse_args(argv)

        # Fail if server not specified
        if args.hostname is None:
            parser.error("--hostname of spalloc server must be specified")
        self.verify_arguments(args)

        try:
            with self.clientFactory(args.hostname, args.port) as client:
                version_verify(client, args.timeout)
                self.body(client, args)
                return 0
        except (IOError, OSError, ProtocolError, ProtocolTimeoutError) as e:
            sys.stderr.write("Error communicating with server: {}\n".format(e))
            return 1
        except SpallocServerException as srv_exn:
            sys.stderr.write("Error from server: {}\n".format(srv_exn))
            return 1
        except Terminate as t:
            t.exit()
