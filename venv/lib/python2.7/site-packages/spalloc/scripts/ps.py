"""An administrative command-line process listing utility.

By default, the ``spalloc-ps`` command lists all running and queued jobs.  For
a real-time monitor of queued and running jobs, the ``--watch`` option may be
added.

.. image:: _static/spalloc_ps.png
    :alt: Jobs being listed by spalloc-ps

This list may be filtered by owner or machine with the ``--owner`` and
``--machine`` arguments.
"""

import argparse
import datetime
from pytz import utc
import sys
from tzlocal import get_localzone

from spalloc import __version__, JobState
from spalloc.term import Terminal, render_table
from .support import Script


def render_job_list(t, jobs, args):
    """Return a human-readable process listing.

    Parameters
    ----------
    t : :py:class:`spalloc.term.Terminal`
        The terminal to which the output will be sent.
    jobs : [{...}, ...]
        The list of jobs returned by the server.
    machine : str or None
        If not None, only list jobs on this machine.
    owner : str or None
        If not None, only list jobs with this owner.
    """
    table = []

    # Add headings
    table.append(((t.underscore_bright, "ID"),
                  (t.underscore_bright, "State"),
                  (t.underscore_bright, "Power"),
                  (t.underscore_bright, "Boards"),
                  (t.underscore_bright, "Machine"),
                  (t.underscore_bright, "Created at"),
                  (t.underscore_bright, "Keepalive"),
                  (t.underscore_bright, "Owner (Host)")))

    for job in jobs:
        # Filter jobs
        if args.machine is not None and \
                job["allocated_machine_name"] != args.machine:
            continue
        if args.owner is not None and job["owner"] != args.owner:
            continue

        # Colourise job states
        if job["state"] == JobState.queued:
            job_state = (t.blue, "queue")
        elif job["state"] == JobState.power:
            job_state = (t.yellow, "power")
        elif job["state"] == JobState.ready:
            job_state = (t.green, "ready")
        else:
            job_state = str(job["state"])

        # Colourise power states
        if job["power"] is not None:
            power_state = (t.green, "on") if job["power"] else (t.red, "off")
            if job["state"] == JobState.power:
                power_state = (t.yellow, power_state[1])
        else:
            power_state = ""

        num_boards = "" if job["boards"] is None else len(job["boards"])

        # Format start time
        utc_timestamp = datetime.datetime.fromtimestamp(
            job["start_time"], utc)
        local_timestamp = utc_timestamp.astimezone(get_localzone())
        timestamp = local_timestamp.strftime('%d/%m/%Y %H:%M:%S')

        if job["allocated_machine_name"] is not None:
            machine_name = job["allocated_machine_name"]
        else:
            machine_name = ""

        owner = job["owner"]
        if "keepalivehost" in job and job["keepalivehost"] is not None:
            owner += " (%s)" % job["keepalivehost"]

        table.append((
            job["job_id"],
            job_state,
            power_state,
            num_boards,
            machine_name,
            timestamp,
            str(job["keepalive"]),
            owner,
        ))
    return render_table(table)


class ProcessListScript(Script):
    def get_parser(self, cfg):  # @UnusedVariable
        parser = argparse.ArgumentParser(description="List all active jobs.")
        parser.add_argument(
            "--version", "-V", action="version", version=__version__)
        parser.add_argument(
            "--watch", "-w", action="store_true", default=False,
            help="watch the list of live jobs in real time")
        filter_args = parser.add_argument_group("filtering arguments")
        filter_args.add_argument(
            "--machine", "-m", help="list only jobs on the specified machine")
        filter_args.add_argument(
            "--owner", "-o",
            help="list only jobs belonging to a particular owner")
        return parser

    def one_shot(self, client, args):
        t = Terminal(stream=sys.stderr)
        jobs = client.list_jobs(timeout=args.timeout)
        print(render_job_list(t, jobs, args))

    def recurring(self, client, args):
        client.notify_job(timeout=args.timeout)
        t = Terminal(stream=sys.stderr)
        while True:
            jobs = client.list_jobs(timeout=args.timeout)
            # Clear the screen before reprinting the table
            sys.stdout.write(t.clear_screen())
            print(render_job_list(t, jobs, args))
            # Wait for state change
            try:
                client.wait_for_notification()
            except KeyboardInterrupt:
                # Gracefully exit
                return
            finally:
                print("")

    def body(self, client, args):
        if args.watch:
            self.recurring(client, args)
        else:
            self.one_shot(client, args)


main = ProcessListScript()
if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
