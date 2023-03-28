import serial.tools.list_ports
import serial
import psutil
import serial.tools.list_ports
import time


def get_com_port():
    """
    Scans all COM ports and sets default port to the first COM port which is not COM1, \
    or COM1 if none is found.

    Returns:
        String: User String of the COM port to use, unsafe.
    """
    default_port = ''
    for p in serial.tools.list_ports.comports():
        if p.name != 'COM1':
            default_port = p.name
            break
    if default_port is None or default_port == '':
        default_port = 'COM1'
    # print('Current default port is :', default_port) # DEBUG
    # r = input("Type the name of the COM port you want to use, or 'y' to continue : ")
    # if r == 'y':
    #     print('Now using', default_port)
    #     return default_port
    # else:
    #     print('Now using', r)
    #     return r
    return default_port


def get_processes():
    """
    Reads processes from processes.ini file and returns it.

    Returns:
        Dict: Dict of the processes found.
    """
    processes = {}
    try:
        with open("processes.ini") as f:
            for line in f:
                (key, val) = line.strip('\n').split(':')
                processes[key] = val
    except FileNotFoundError:
        print("File 'processes.ini' missing or corrupted.")
    return processes


def is_active_process(process):
    """
    Checks if the passed string is a valid, active process on the system.

    Args:
        process (String): The process to look for in active processes.

    Returns:
        Boolean: True if the process is found and active, False if not.
    """
    if process in (p.name() for p in psutil.process_iter()):
        return True
    else:
        return False


def set_keys(com_port, mode):
    """
    Sets the keypad's keys over the provided COM port and based on the passed 'mode' string.

    Args:
        com_port (String): Unsafe, should indicate the name of the COM port the keypad is plugged
        into.
        mode (String): Unsafe, list of 4 characters to map to the keypad. Can also contain 'ARROWS'.
    """
    ser = serial.Serial(com_port, 9600, timeout=1)
    if mode is None or mode == "":
        print("No active process to map")
        return
    ser.write(b'0')  # Open Remapper
    time.sleep(2)
    if mode == "ARROWS":
        ser.write(b":26")
        time.sleep(2)
        ser.write(b"xx")
        time.sleep(2)
        ser.write(b":25")
        time.sleep(2)
        ser.write(b"xx")
        time.sleep(2)
        ser.write(b":24")
        time.sleep(2)
        ser.write(b"xx")
        time.sleep(2)
        ser.write(b":27")
        time.sleep(2)
        ser.write(b"xx")
        time.sleep(2)
        print("Keys bound to ARROWS")
    else:
        ser.write(b"%b" % mode[0].encode("utf-8"))
        time.sleep(2)
        ser.write(b"%b" % mode[1].encode("utf-8"))
        time.sleep(2)
        ser.write(b"%b" % mode[2].encode("utf-8"))
        time.sleep(2)
        ser.write(b"%b" % mode[3].encode("utf-8"))
        time.sleep(2)
        print("Keys bound to " + mode)


def get_active_mode(processes):
    """
    Checks the passed dict for active processes and returns the mode of the first one found.

    Args:
        processes (Dict): The list of processes and their modes in which to look for active
        processes.

    Returns:
        String: The mode of the first active process found (e.g. 'WXCV' or 'ARROWS').
    """
    for x in processes:
        if is_active_process(x):
            return processes[x].upper()


if __name__ == "__main__":
    last_mode = None
    com_port = get_com_port()
    while True:
        processesList = get_processes()
        active_mode = get_active_mode(processesList)
        if last_mode != active_mode:                   # If mode changed since last loop
            last_mode = active_mode                    # This mode is now the last registered one
            set_keys(com_port, active_mode)            # Bind the keys for that specific mode
            print("Now using mode", active_mode)
        time.sleep(10)
