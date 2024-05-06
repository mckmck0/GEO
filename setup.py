"""This script installs CPLEX and DOcplex.

It accepts three commands: help, install or uninstall
Any subsequent argument is given to pip as is
"""
import glob
import os
import subprocess
import sys


# We want to call python from this script.
# So let's record which interpreter runs
python = sys.executable


def guess_cplex_path():
    python_version = "%s.%s" % (sys.version_info[0], sys.version_info[1])

    # record location of the script. We'll find the CPLEX wrappers from here
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # The script is in a subdir of the root. So dirname(root) is the root
    # of this COS installation
    root = os.path.dirname(script_dir)
    # CPLEX is in root/cplex
    # the python wrappers are in a subdir python/python_version/port
    # and port/ contains cplex (the wrappers themselves, not the engine)
    # and setup.py to install them.
    g = os.path.join(root, 'cplex', 'python', python_version)
    cplex_dir = glob.glob(os.path.join(g, '*', 'cplex'))
    setup_py = glob.glob(os.path.join(g, '*', 'setup.py'))

    if len(cplex_dir) > 1 or len(setup_py) > 1:
        # There is more than one port for the CPLEX wrappers. We don't know
        # which one to select
        print(f'ERROR: More than one port exists for the CPLEX python wrappers at {g}')
        exit(1)

    if len(cplex_dir) == 0 or len(setup_py) == 0:
        print(f'ERROR: No CPLEX python wrappers at {g}')
        exit(1)

    if os.path.isdir(cplex_dir[0]) and os.path.exists(setup_py[0]):
        return os.path.dirname(setup_py[0])
    return None


def usage():
    script_name = os.path.basename(sys.argv[0])
    print("IBM ILOG CPLEX Optimization Studio installation script for Python")
    print()
    print(f"Usage: {script_name} command [pip-options]")
    print()
    print("Command can be: install, uninstall, help")
    print("pip-options can be anything: that will be passed straight to the pip commands")


def install(args):
    cplex_path = guess_cplex_path()
    if cplex_path is None:
        print("ERROR: No CPLEX python wrappers found.")
        exit(1)

    # install cplex
    command = [python, '-m', 'pip', 'install'] + args + ['.']
    print("Invoking %s in %s" % (command, cplex_path))
    r = subprocess.call(command, cwd=cplex_path)
    if r != 0:
        print("Could not install CPLEX, code = %s" % r)
        exit(r)

    # install docplex
    command = [python, '-m', 'pip', 'install'] + args + ['docplex']
    print("Invoking %s" % command)
    r = subprocess.call(command)
    if r != 0:
        print("Could not install DOcplex, code = %s" % r)
        exit(r)


def uninstall(args):
    # uninstall cplex
    command = [python, '-m', 'pip', 'uninstall', '-y'] + args + ['cplex']
    print("Invoking %s" % command)
    r = subprocess.call(command)
    if r != 0:
        print("Could not uninstall CPLEX, code = %s" % r)
        exit(r)

    # uninstall docplex
    command = [python, '-m', 'pip', 'uninstall', '-y'] + args + ['docplex']
    print("Invoking %s" % command)
    r = subprocess.call(command)
    if r != 0:
        print("Could not uninstall DOcplex, code = %s" % r)
        exit(r)


def main(args):
    if 'help' == args[0]:
        usage()
        exit(0)

    if 'install' == args[0]:
        install(args[1:])
        exit(0)

    if 'uninstall' == args[0]:
        uninstall(args[1:])
        exit(0)

    print(f"ERROR: unknown command: {args}")
    exit(1)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        usage()
        exit(1)

    main(sys.argv[1:])
