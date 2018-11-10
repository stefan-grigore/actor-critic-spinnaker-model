"""Command-line administrative machine management interface.

When called with no arguments the ``spalloc-machine`` command lists all
available machines and a summary of their current load.

If a specific machine is given as an argument, the current allocation of jobs
to machines is displayed:

.. image:: _static/spalloc_machine.png
    :alt: spalloc-machine showing jobs allocated on a machine.

Adding the ``--detailed`` option displays additional information about jobs
running on a machine.

If the ``--watch`` option is given, the information displayed is updated in
real-time.
"""
import argparse
from collections import defaultdict, OrderedDict
from six import next
import sys

from spalloc import __version__
from spalloc.term import \
    Terminal, render_table, render_definitions, render_boards, render_cells, \
    DEFAULT_BOARD_EDGES
from .support import Terminate, Script


# The acceptable range of server version numbers
VERSION_RANGE_START = (0, 1, 0)
VERSION_RANGE_STOP = (2, 0, 0)


def generate_keys(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    """Generate ascending values in spreadsheet-column-name style.

    For example, A, B, C, ..., Y, Z, AA, AB, AC...
    """
    for symbol in alphabet:
        yield symbol

    for prefix in generate_keys(alphabet):
        for symbol in alphabet:
            yield prefix + symbol


def list_machines(t, machines, jobs):
    """Display a table summarising the available machines and their load.

    Parameters
    ----------
    t : :py:class:`.Terminal`
        An output styling object for stdout.
    machines : [{...}, ...]
        The list of machines and their properties returned from the server.
    jobs : [{...}, ...]
        The list of jobs and their properties returned from the server.

    Returns
    -------
        An error code: 0 on success.
    """
    machine_jobs = defaultdict(list)
    for job in jobs:
        machine_jobs[job["allocated_machine_name"]].append(job)

    table = [[
        (t.underscore_bright, "Name"),
        (t.underscore_bright, "Num boards"),
        (t.underscore_bright, "In-use"),
        (t.underscore_bright, "Jobs"),
        (t.underscore_bright, "Tags"),
    ]]

    for machine in machines:
        table.append([
            machine["name"],
            ((machine["width"] * machine["height"] * 3) -
             len(machine["dead_boards"])),
            sum(len(job["boards"]) for job in machine_jobs[machine["name"]]),
            len(machine_jobs[machine["name"]]),
            ", ".join(machine["tags"]),
        ])

    print(render_table(table))


def show_machine(t, machines, jobs, machine_name, compact=False):
    """Display a more detailed overview of an individual machine.

    Parameters
    ----------
    t : :py:class:`.Terminal`
        An output styling object for stdout.
    machines : [{...}, ...]
        The list of machines and their properties returned from the server.
    jobs : [{...}, ...]
        The list of jobs and their properties returned from the server.
    machine_name : str
        The machine of interest.
    compact : bool
        If True, display the listing of jobs on the machine in a more compact
        format.

    Returns
    -------
        An error code: 0 on success.
    """
    # Find the machine requested
    for machine in machines:
        if machine["name"] == machine_name:
            break
    else:
        # No matching machine
        raise Terminate(6, "No machine '{}' was found", machine_name)

    # Extract list of jobs running on the machine
    displayed_jobs = []
    job_key_generator = iter(generate_keys())
    job_colours = [
        t.green, t.blue, t.magenta, t.yellow, t.cyan,
        t.dim_green, t.dim_blue, t.dim_magenta, t.dim_yellow, t.dim_cyan,
        t.bright_green, t.bright_blue, t.bright_magenta, t.bright_yellow,
        t.bright_cyan,
    ]
    for job in jobs:
        if job["allocated_machine_name"] == machine_name:
            displayed_jobs.append(job)
            job["key"] = next(job_key_generator)
            job["colour"] = job_colours[job["job_id"] % len(job_colours)]

    # Calculate machine stats
    num_boards = ((machine["width"] * machine["height"] * 3) -
                  len(machine["dead_boards"]))
    num_in_use = sum(map(len, (job["boards"] for job in displayed_jobs)))

    # Show general machine information
    info = OrderedDict()
    info["Name"] = machine["name"]
    info["Tags"] = ", ".join(machine["tags"])
    info["In-use"] = "{} of {}".format(num_in_use, num_boards)
    info["Jobs"] = len(displayed_jobs)
    print(render_definitions(info))

    # Draw diagram of machine
    dead_boards = set((x, y, z) for x, y, z in machine["dead_boards"])
    board_groups = [(set([(x, y, z)
                          for x in range(machine["width"])
                          for y in range(machine["height"])
                          for z in range(3)
                          if (x, y, z) not in dead_boards]),
                     t.dim(" . "),  # Label
                     tuple(map(t.dim, DEFAULT_BOARD_EDGES)),  # Inner
                     tuple(map(t.dim, DEFAULT_BOARD_EDGES)))]  # Outer
    for job in displayed_jobs:
        board_groups.append((
            job["boards"],
            job["colour"](job["key"].center(3)),  # Label
            tuple(map(job["colour"], DEFAULT_BOARD_EDGES)),  # Inner
            tuple(map(t.bright, DEFAULT_BOARD_EDGES))  # Outer
        ))
    print("")
    print(render_boards(board_groups, machine["dead_links"],
                        tuple(map(t.red, DEFAULT_BOARD_EDGES))))

    # Produce table showing jobs on machine
    if compact:
        # In compact mode, produce column-aligned cells
        cells = []
        for job in displayed_jobs:
            key = job["key"]
            job_id = str(job["job_id"])
            cells.append((len(key) + len(job_id) + 1,
                         "{}:{}".format(job["colour"](key), job_id)))
        print("")
        print(render_cells(cells))
    else:
        # In non-compact mode, produce a full table of job information
        job_table = [[
            (t.underscore_bright, "Key"),
            (t.underscore_bright, "Job ID"),
            (t.underscore_bright, "Num boards"),
            (t.underscore_bright, "Owner (Host)"),
        ]]
        for job in displayed_jobs:
            owner = job["owner"]
            if "keepalivehost" in job and job["keepalivehost"] is not None:
                owner += " (%s)" % job["keepalivehost"]
            job_table.append([
                (job["colour"], job["key"]),
                job["job_id"],
                len(job["boards"]),
                owner,
            ])
        print("")
        print(render_table(job_table))


class ListMachinesScript(Script):
    def get_and_display_machine_info(self, client, args, t):
        # Get all information
        machines = client.list_machines(timeout=args.timeout)
        jobs = client.list_jobs(timeout=args.timeout)

        # Display accordingly
        if args.machine is None:
            list_machines(t, machines, jobs)
        else:
            show_machine(t, machines, jobs, args.machine, not args.detailed)

    def get_parser(self, cfg):  # @UnusedVariable
        parser = argparse.ArgumentParser(
            description="Get the state of individual machines.")
        parser.add_argument(
            "--version", "-V", action="version", version=__version__)
        parser.add_argument(
            "machine", nargs="?",
            help="if given, specifies the machine to inspect")
        parser.add_argument(
            "--watch", "-w", action="store_true", default=False,
            help="update the output when things change.")
        parser.add_argument(
            "--detailed", "-d", action="store_true", default=False,
            help="list detailed job information")
        self.parser = parser
        return parser

    def verify_arguments(self, args):
        # Fail if --detailed used without specifying machine
        if args.machine is None and args.detailed:
            self.parser.error(
                "--detailed only works when a specific machine is specified")

    def one_shot(self, client, args):
        t = Terminal()
        # Get all information and display accordingly
        self.get_and_display_machine_info(client, args, t)

    def recurring(self, client, args):
        t = Terminal()
        while True:
            client.notify_machine(args.machine, timeout=args.timeout)
            t.stream.write(t.clear_screen())
            # Prevent errors on stderr being cleared away due to clear being
            # buffered
            t.stream.flush()

            # Get all information and display accordingly
            self.get_and_display_machine_info(client, args, t)

            # Wait for changes
            try:
                client.wait_for_notification()
            except KeyboardInterrupt:
                return
            finally:
                print("")

    def body(self, client, args):
        if args.watch:
            self.recurring(client, args)
        else:
            self.one_shot(client, args)
        return 0


main = ListMachinesScript()
if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
