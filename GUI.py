import PySimpleGUI as sg
import threading
import winsound
#import psgtray
from psgtray import SystemTray

import keypadProfile
import layouts.mainMenu as mainMenuLayout

# TODO LIST :
#   --------------------------------------------------------------------------------------------------------------------
#   - Implement AUTO mode, probable use of threading to not freeze the app ?
#       - Refresh processes list every 5 seconds, but don't refresh the table.
#   - Capitalize or lowercase all processes' modes, everywhere.
#   - Sanitizing User Input in both backend and frontend.
#   - Display all COM ports in a dropdown menu.
#   - Refactoring all strings with the f-strings syntax for consistency.
#   - Refactoring bits of code into functions for easier maintaining and re-usability, especially in event handlers
#   - Refactoring (getting rid of the manual editing of processes.ini in favour of the 'INPUT_CUSTOM' way ?)
#   ----- New Button to add a process and its mode without editing processes.ini ?
#   ----- Delete Button to remove a process and its mode without editing processes.ini ?
#   - Using cprint in the multiline output box to outline processes name and modes as well as COM port.
#   - FIX : Fix the empty space after clicking on the custom tab and then away from it. (would be a non issue with
#           the above refactoring)
#   - FIX : Find a way to speed up the binding of keys.
#   - B4-RELEASE : Remove the print statements and replace them with logging or remove them altogether.
#   - B4-RELEASE : Modify functions that need threading in the backend rather than in the frontend.
#   - B4-RELEASE : Find a way to add 'ARROW' mode to processes.
#   - B4-RELEASE : Add a 'About' window with the version number and a link to the GitHub repo.
#    (cf. bind_thread)
#   --------------------------------------------------------------------------------------------------------------------


def bind_thread(com_port, selected_mode):
    """Threaded function to call the key binding function from the backend.

    Args:
        com_port (str): COM port of the keypad
        selected_mode (str): mode to bind the keys to
    """
    print(f"Binding keys for {selected_mode} mode over {com_port}...")
    keypadProfile.set_keys(com_port, selected_mode)
    winsound.PlaySound('SystemAsterisk', winsound.SND_ASYNC)
    window['-BUTTON_BIND-'].update(disabled=False)


def get_processes_list() -> list[list]:
    """Reads processes.ini from the backend to get a fresh list of processes, then formats it to be
    displayed in a table and returns it.

    Returns:
        List[List]: list of all processes and their modes, ready to be displayed in a table.
    """
    processes = {"Auto": "N/A", "Custom": "N/A"}
    processes.update(keypadProfile.get_processes())
    processes = list(map(list, processes.items()))
    return processes


VERSION = '0.2.0'
NAME = 'KeypadProfile v' + VERSION
layout = mainMenuLayout.mainMenuLayout
window = sg.Window(title=NAME, layout=layout, icon='./favicon.ico')

menu = ['', ['Show Window', 'Hide Window', '---', 'Exit']]
tooltip = NAME + '\n' + 'Double click to show/hide window.' + '\n' + 'Right click for menu.'
tray = SystemTray(menu, single_click_events=False, window=window, tooltip=tooltip, icon='./favicon.ico')
tray.show_message('KeypadProfile', 'KeypadProfile is now in the system tray.')


processes = get_processes_list()
t = threading.Thread()

while True:
    event, values = window.read()
    # print(event, values)  # DEBUG

    if event == tray.key:
        event = values[event]  # use the System Tray's event as if was from the window

    if event in ('Exit', sg.WIN_CLOSED):
        break

    if event == '-BUTTON_TRAY-':
        window.hide()
        tray.show_icon()

    if event == sg.EVENT_SYSTEM_TRAY_ICON_DOUBLE_CLICKED:
        if window.TKroot.state() == 'withdrawn':
            window.un_hide()
            window.bring_to_front()
        else:
            window.hide()
            tray.show_icon()
    elif event == 'Show Window':
        window.un_hide()
        window.bring_to_front()
    elif event in ('Hide Window', sg.WIN_CLOSE_ATTEMPTED_EVENT):
        window.hide()
        tray.show_icon()  # if hiding window, better make sure the icon is visible

    if event == '-BUTTON_BIND-':
        if values['-TABLE-']:
            selected_row_data = processes[values['-TABLE-'][0]]  # Retrieve the row data from the processes list
            print(f"Selected Process: {selected_row_data[0]}  |  Selected Mode: {selected_row_data[1]}")
            selected_process = selected_row_data[0]
            selected_mode = selected_row_data[1]
            com_port = keypadProfile.get_com_port()
            if selected_process == "Auto":
                print("Auto mode is not implemented yet.")
            elif selected_process == "Custom" and selected_mode == "N/A":
                print("Please enter a mode for the custom process.")
            else:
                t = threading.Thread(target=bind_thread, args=(com_port, selected_mode))
                t.start()
                window['-BUTTON_BIND-'].update(disabled=True)
        else:
            print("Please select a row in the table.")

    if event == '-TABLE-':
        if values['-TABLE-']:
            selected_row_data = processes[values['-TABLE-'][0]]
            if selected_row_data[0] == "Custom":
                window['-TEXT_CUSTOM-'].update(visible=True)
                window['-INPUT_CUSTOM-'].update(disabled=False)
                window['-COLUMN_CUSTOM-'].update(visible=True)
            else:
                window['-TEXT_CUSTOM-'].update(visible=False)
                window['-INPUT_CUSTOM-'].update(disabled=True)
                window['-COLUMN_CUSTOM-'].update(visible=False)

    if event == '-INPUT_CUSTOM-':
        user_input = values['-INPUT_CUSTOM-']
        if len(user_input) > 4:     # Limits the number of characters to 4 in the Custom Input
            window['-INPUT_CUSTOM-'].update(user_input[:-1])

    if event == '-BUTTON_CUSTOM-':
        user_input = values['-INPUT_CUSTOM-']
        if user_input and len(user_input) == 4:
            if values['-TABLE-']:   # Check if the table is initialized and not empty
                selected_row_index = values['-TABLE-'][0]
                processes[selected_row_index][1] = user_input
                window['-TABLE-'].update(values=processes, select_rows=[selected_row_index])
                print("Custom mode set to:", user_input)
        else:
            print("Please enter a valid mode for the custom process.")

    if event == '-BUTTON_RESCAN-':
        processes = get_processes_list()
        window['-TABLE-'].update(values=processes)  # Updating Table
        window['-TEXT_CUSTOM-'].update(visible=False)   # Hiding 'CUSTOM' widgets
        window['-INPUT_CUSTOM-'].update(disabled=True)
        window['-COLUMN_CUSTOM-'].update(visible=False)

if t.is_alive():
    t.join()
tray.close()
window.close()
