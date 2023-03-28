import PySimpleGUI as sg
import keypadProfile

sg.theme('DarkAmber')

processes = {"Auto": "N/A", "Custom": "N/A"}
processes.update(keypadProfile.get_processes())
processes = list(map(list, processes.items()))

mainMenuLayout = [
    [sg.Column([
        [sg.Text('Console Output :')],
        [sg.Multiline(
            key='-ML_CONSOLE_OUTPUT-',
            size=(60, 10),
            autoscroll=True,
            disabled=True,
            reroute_stdout=True,
            no_scrollbar=True)],
        [sg.HorizontalSeparator(pad=(0, 10))],
        [sg.Table(
            key="-TABLE-",
            values=processes,
            headings=["Process", "Mode"],
            auto_size_columns=False,
            justification='center',
            num_rows=6,
            def_col_width=20,
            col_widths=[20, 20],
            font=('Consolas', 12),
            vertical_scroll_only=True,
            display_row_numbers=False,
            enable_events=True,
            bind_return_key=True)],
        [sg.Text("Custom Mode :", visible=False, key="-TEXT_CUSTOM-")],
        [sg.Column(visible=False, key="-COLUMN_CUSTOM-", layout=[
            [sg.Input(size=20, enable_events=True, disabled=True, key="-INPUT_CUSTOM-"),
             sg.Button('OK', key="-BUTTON_CUSTOM-")
             ]]
        )],
        [sg.Button('Bind', key='-BUTTON_BIND-'),
         sg.Button('Rescan', key='-BUTTON_RESCAN-'),
         sg.Button('Tray', key='-BUTTON_TRAY-'),
         sg.Button('Exit')]
    ], justification='center', element_justification='center')]
]
