from spalloc.version import __version__  # noqa

# Alias useful objects
from spalloc.protocol_client import ProtocolClient, ProtocolError  # noqa
from spalloc.protocol_client import ProtocolTimeoutError  # noqa
from spalloc.protocol_client import SpallocServerException  # noqa
from spalloc.job import Job, JobDestroyedError, StateChangeTimeoutError  # noqa
from spalloc.states import JobState  # noqa
