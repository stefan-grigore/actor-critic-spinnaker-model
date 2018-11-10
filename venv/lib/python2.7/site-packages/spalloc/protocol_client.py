"""A simple blocking spalloc_server protocol implementation."""

import socket
import json
from threading import current_thread, RLock, local
from collections import deque
from spalloc._utils import time_left, timed_out, make_timeout
import errno
import sys


class ProtocolError(Exception):
    """Thrown when a network-level problem occurs during protocol handling."""


class ProtocolTimeoutError(Exception):
    """Thrown upon a protocol-level timeout."""


class SpallocServerException(Exception):
    """Thrown when something went wrong on the server side that caused us to\
    be sent a message.
    """


class _ProtocolThreadLocal(local):
    """Subclass of threading.local to ensure that we get sane initialisation\
    of our state in each thread.
    """
    # See https://github.com/SpiNNakerManchester/spalloc/issues/12
    def __init__(self):
        self.buffer = b""
        self.sock = None


class ProtocolClient(object):
    """A simple (blocking) client implementation of the `spalloc-server
    <https://github.com/project-rig/spalloc_server>`_ protocol.

    This minimal implementation is intended to serve both simple applications
    and as an example implementation of the protocol for other applications.
    This implementation simply implements the protocol, presenting an RPC-like
    interface to the server. For a higher-level interface built on top of this
    client, see :py:class:`spalloc.Job`.

    Usage examples::

        # Connect to a spalloc_server
        with ProtocolClient("hostname") as c:
            # Call commands by name
            print(c.call("version"))  # '0.1.0'

            # Call commands as if they were methods
            print(c.version())  # '0.1.0'

            # Wait an event to be received
            print(c.wait_for_notification())  # {"jobs_changed": [1, 3]}

        # Done!
    """

    def __init__(self, hostname, port=22244, timeout=None):
        """Define a new connection.

        .. note::

            Does not connect to the server until :py:meth:`.connect` is called.

        Parameters
        ----------
        hostname : str
            The hostname of the server.
        port : str
            The port to use (default: 22244).
        """
        self._hostname = hostname
        self._port = port
        # Mapping from threads to sockets. Kept because we need to have way to
        # shut down all sockets at once.
        self._socks = dict()
        # Thread local variables
        self._local = _ProtocolThreadLocal()
        # A queue of unprocessed notifications
        self._notifications = deque()
        self._dead = True
        self._socks_lock = RLock()
        self._notifications_lock = RLock()
        self._default_timeout = timeout

    def __enter__(self):  # pragma: no cover
        self.connect(self._default_timeout)
        return self

    def __exit__(self, type,  # @ReservedAssignment # pragma: no cover
                 value, tb):  # @UnusedVariable # pragma: no cover
        self.close()
        return False

    def _get_connection(self, timeout):
        if self._dead:
            if sys.version_info[0] > 2:
                raise OSError(errno.ENOTCONN, "not connected")
            else:
                raise socket.error(errno.ENOTCONN, "not connected")
        connect_needed = False
        key = current_thread()
        with self._socks_lock:
            sock = self._socks.get(key, None)
            if sock is None:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # The socket connected to the server or None if disconnected.
                self._socks[key] = sock
                connect_needed = True

        if connect_needed:
            # A buffer for incoming, but incomplete, lines of data
            self._local.buffer = b""
            self._local.sock = sock
            sock.settimeout(timeout)
            if not self._do_connect(sock):  # pragma: no cover
                self._close(key)
                return self._get_connection(timeout)

        sock.settimeout(timeout)
        return sock

    def _do_connect(self, sock):
        success = False
        try:
            sock.connect((self._hostname, self._port))
            success = True
        except OSError as e:
            if e.errno != errno.EISCONN:
                raise
        except socket.error as e:
            if e[0] != errno.EISCONN:
                raise
        return success

    def _has_open_socket(self):
        return self._local.sock is not None

    def connect(self, timeout=None):
        """(Re)connect to the server.

        Raises
        ------
        OSError, IOError
            If a connection failure occurs.
        """
        # Close any existing connection
        if self._has_open_socket():
            self._close()
        self._dead = False
        self._connect(timeout)

    def _connect(self, timeout):
        """Try to (re)connect to the server."""
        try:
            return self._get_connection(timeout)
        except (IOError, OSError):
            # Failure, try again...
            self._close()
            # Pass on the exception
            raise

    def _close(self, key=None):
        if key is None:
            key = current_thread()
        with self._socks_lock:
            sock = self._socks.get(key, None)
            if sock is None:  # pragma: no cover
                return
            del self._socks[key]
        if key == current_thread():
            self._local.sock = None
            self._local.buffer = b""
        sock.close()

    def close(self):
        """Disconnect from the server."""
        self._dead = True
        with self._socks_lock:
            keys = list(self._socks.keys())
        for key in keys:
            self._close(key)
        self._local = _ProtocolThreadLocal()

    def _recv_json(self, timeout=None):
        """Receive a line of JSON from the server.

        Parameters
        ----------
        timeout : float or None
            The number of seconds to wait before timing out or None if this
            function should try again forever.

        Returns
        -------
        object or None
            The unpacked JSON line received.

        Raises
        ------
        ProtocolTimeoutError
            If a timeout occurs.
        OSError
            If the socket is unusable or becomes disconnected.
        """
        sock = self._get_connection(timeout)

        # Wait for some data to arrive
        while b"\n" not in self._local.buffer:
            try:
                data = sock.recv(1024)
            except socket.timeout:
                raise ProtocolTimeoutError("recv timed out.")

            # Has socket closed?
            if len(data) == 0:
                raise OSError("Connection closed.")

            self._local.buffer += data

        # Unpack and return the JSON
        line, _, self._local.buffer = self._local.buffer.partition(b"\n")
        return json.loads(line.decode("utf-8"))

    def _send_json(self, obj, timeout=None):
        """Attempt to send a line of JSON to the server.

        Parameters
        ----------
        obj : object
            The object to serialise.
        timeout : float or None
            The number of seconds to wait before timing out or None if this
            function should try again forever.

        Raises
        ------
        ProtocolTimeoutError
            If a timeout occurs.
        OSError
            If the socket is unusable or becomes disconnected.
        """
        sock = self._get_connection(timeout)

        # Send the line
        data = json.dumps(obj).encode("utf-8") + b"\n"
        try:
            if sock.send(data) != len(data):
                # XXX: If can't send whole command at once, just fail
                raise OSError("Could not send whole command.")
        except socket.timeout:
            raise ProtocolTimeoutError("send timed out.")

    def call(self, name, *args, **kwargs):
        """Send a command to the server and return the reply.

        Parameters
        ----------
        name : str
            The name of the command to send.
        timeout : float or None
            The number of seconds to wait before timing out or None if this
            function should wait forever. (Default: None)

        Returns
        -------
        object
            The object returned by the server.

        Raises
        ------
        ProtocolTimeoutError
            If a timeout occurs.
        ProtocolError
            If the connection is unavailable or is closed.
        """
        try:
            timeout = kwargs.pop("timeout", None)
            finish_time = make_timeout(timeout)

            # Construct the command message
            command = {"command": name, "args": args, "kwargs": kwargs}
            self._send_json(command, timeout=timeout)

            # Command sent! Attempt to receive the response...
            while not timed_out(finish_time):
                obj = self._recv_json(timeout=time_left(finish_time))
                if "return" in obj:
                    # Success!
                    return obj["return"]
                if "exception" in obj:
                    raise SpallocServerException(obj["exception"])
                # Got a notification, keep trying...
                with self._notifications_lock:
                    self._notifications.append(obj)
        except (IOError, OSError) as e:
            raise ProtocolError(str(e))

    def wait_for_notification(self, timeout=None):
        """Return the next notification to arrive.

        Parameters
        ----------
        name : str
            The name of the command to send.
        timeout : float or None
            The number of seconds to wait before timing out or None if this
            function should try again forever.

            If negative only responses already-received will be returned. If no
            responses are available, in this case the function does not raise a
            ProtocolTimeoutError but returns None instead.

        Returns
        -------
        object
            The notification sent by the server.

        Raises
        ------
        ProtocolTimeoutError
            If a timeout occurs.
        ProtocolError
            If the socket is unusable or becomes disconnected.
        """
        # If we already have a notification, return it
        with self._notifications_lock:
            if self._notifications:
                return self._notifications.popleft()

        # Check for a duff timeout
        if timeout is not None and timeout < 0.0:
            return None

        # Otherwise, wait for a notification to arrive
        try:
            return self._recv_json(timeout)
        except (IOError, OSError) as e:  # pragma: no cover
            raise ProtocolError(str(e))

    # The bindings of the Spalloc protocol methods themselves; simplifies use
    # from IDEs.

    def version(self, timeout=None):  # pragma: no cover
        return self.call("version", timeout=timeout)

    def create_job(self, *args, **kwargs):  # pragma: no cover
        # If no owner, don't bother with the call
        if "owner" not in kwargs:
            raise SpallocServerException(
                "owner must be specified for all jobs.")
        return self.call("create_job", *args, **kwargs)

    def job_keepalive(self, job_id, timeout=None):  # pragma: no cover
        return self.call("job_keepalive", job_id, timeout=timeout)

    def get_job_state(self, job_id, timeout=None):  # pragma: no cover
        return self.call("get_job_state", job_id, timeout=timeout)

    def get_job_machine_info(self, job_id, timeout=None):  # pragma: no cover
        return self.call("get_job_machine_info", job_id, timeout=timeout)

    def power_on_job_boards(self, job_id, timeout=None):  # pragma: no cover
        return self.call("power_on_job_boards", job_id, timeout=timeout)

    def power_off_job_boards(self, job_id, timeout=None):  # pragma: no cover
        return self.call("power_off_job_boards", job_id, timeout=timeout)

    def destroy_job(self, job_id, reason=None,
                    timeout=None):  # pragma: no cover
        return self.call("destroy_job", job_id, reason, timeout=timeout)

    def notify_job(self, job_id=None, timeout=None):  # pragma: no cover
        return self.call("notify_job", job_id, timeout=timeout)

    def no_notify_job(self, job_id=None, timeout=None):  # pragma: no cover
        return self.call("no_notify_job", job_id, timeout=timeout)

    def notify_machine(self, machine_name=None,
                       timeout=None):  # pragma: no cover
        return self.call("notify_machine", machine_name, timeout=timeout)

    def no_notify_machine(self, machine_name=None,
                          timeout=None):  # pragma: no cover
        return self.call("no_notify_machine", machine_name, timeout=timeout)

    def list_jobs(self, timeout=None):  # pragma: no cover
        return self.call("list_jobs", timeout=timeout)

    def list_machines(self, timeout=None):  # pragma: no cover
        return self.call("list_machines", timeout=timeout)

    def get_board_position(self, machine_name, x, y, z,
                           timeout=None):  # pragma: no cover
        return self.call("get_board_position", machine_name, x, y, z,
                         timeout=timeout)

    def get_board_at_position(self, machine_name, x, y, z,
                              timeout=None):  # pragma: no cover
        return self.call("get_board_at_position", machine_name, x, y, z,
                         timeout=timeout)

    _acceptable_kwargs_for_where_is = frozenset([
        frozenset("machine x y z".split()),
        frozenset("machine cabinet frame board".split()),
        frozenset("machine chip_x chip_y".split()),
        frozenset("job_id chip_x chip_y".split())])

    def where_is(self, timeout=None, **kwargs):
        # Test for whether sane arguments are passed.
        keywords = frozenset(kwargs)
        if keywords not in ProtocolClient._acceptable_kwargs_for_where_is:
            raise SpallocServerException(
                "Invalid arguments: {}".format(", ".join(keywords)))
        kwargs["timeout"] = timeout
        return self.call("where_is", **kwargs)
