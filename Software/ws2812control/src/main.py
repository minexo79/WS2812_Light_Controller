import flet as ft
from parse_tool import parseJson
import os
from serial_light import ws2812ser

ser = ws2812ser("COM7", 115200)

class SerialControl(ft.UserControl):
    textStatus = ft.Text(value="Status: Not Connected.")

    def connect_serial(self, e: ft.Control):
        global ser
        ser.connect()

        self.textStatus.value = "Status: Connected."
        self.textStatus.update()

        print("> Connected to {}.".format(ser.comport))

    def disconnect_serial(self, e: ft.Control):
        global ser 
        ser.disconnect()

        self.textStatus.value = "Status: Not Connected."
        self.textStatus.update()

        print("> Disconnected from {}.".format(ser.comport))

    def build(self):
        column = ft.Column([
            ft.Row([
                ft.ElevatedButton(text="Connect",
                                bgcolor=ft.colors.YELLOW_900,
                                color=ft.colors.WHITE,
                                width=150,
                                on_click=self.connect_serial),
                ft.ElevatedButton(text="Disconnect",
                                bgcolor=ft.colors.WHITE10,
                                color=ft.colors.WHITE,
                                width=150,
                                on_click=self.disconnect_serial),
            ], 
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20),
            self.textStatus
        ])

        container = ft.Container(
            content=column,
            padding = 10,
            bgcolor = ft.colors.BLACK54,
            border_radius=10
        )

        return container

class SlideControl(ft.UserControl):
    wsval       = [0, 0, 0]

    rslider = ft.Slider(min=0, max=255, divisions=255, label="{value}")
    gslider = ft.Slider(min=0, max=255, divisions=255, label="{value}")
    bslider = ft.Slider(min=0, max=255, divisions=255, label="{value}")

    textValue   = ft.Text(value="LED Value", size=16)

    def slide_changed(self, e: ft.Control):
        self.wsval[0] = self.rslider.value or 0
        self.wsval[1] = self.gslider.value or 0
        self.wsval[2] = self.bslider.value or 0

        ser.sendSerial(mode = 'custom', wsval = self.wsval)    

        self.textValue.value = "LED Value: {} {} {}".format(self.wsval[0], self.wsval[1], self.wsval[2])
        self.textValue.update()

    def build(self):
        self.rslider.on_change = self.slide_changed
        self.gslider.on_change = self.slide_changed
        self.bslider.on_change = self.slide_changed

        return ft.ResponsiveRow([        
            ft.Text('Color R', size=16, weight=ft.FontWeight.BOLD),
            self.rslider,
            ft.Text('Color G', size=16, weight=ft.FontWeight.BOLD),
            self.gslider,
            ft.Text('Color B', size=16, weight=ft.FontWeight.BOLD),
            self.bslider,
            self.textValue,
            ft.ElevatedButton(text='Add To Record', icon='add')
        ])

class QuickControl(ft.UserControl):
    
    dropdown = ft.Dropdown(width=100, col=10, text_size=16, color=ft.colors.BLACK)

    def quick_change_state(self, e: ft.UserControl):
        global ser
        ser.sendSerial(mode = e.control.data)
        pass

    def parse_with_file(self, e: ft.UserControl):
        global ser
        parse = parseJson()
        parse.parseToStructure("./data/" + self.dropdown.value)

        ser.sendSerialWithTiming(parse.parsedata)


    def build(self):
        control = [
            ft.ElevatedButton(text="Set RED",
                            bgcolor=ft.colors.RED,
                            color=ft.colors.WHITE,
                            on_click=self.quick_change_state,
                            data='r',
                            col=4),
            ft.ElevatedButton(text="Set GREEN", 
                            bgcolor=ft.colors.GREEN,
                            color=ft.colors.WHITE,
                            on_click=self.quick_change_state,
                            data='g',
                            col=4),
            ft.ElevatedButton(text="Set BLUE", 
                            bgcolor=ft.colors.BLUE, 
                            color=ft.colors.WHITE,
                            on_click=self.quick_change_state,
                            data='b',
                            col=4),
            ft.ElevatedButton(text="Turn Off LED", 
                            bgcolor=ft.colors.BLUE_GREY_900, 
                            color=ft.colors.WHITE,
                            on_click=self.quick_change_state,
                            data='close',
                            col=12)]

        datadir = os.listdir("data/")
        selection = []
        
        for file in datadir:
            selection.append(ft.dropdown.Option(file))

        self.dropdown.options=selection

        control.append(ft.Divider())
        control.append(self.dropdown)
        control.append(
            ft.IconButton(
                icon=ft.icons.SEND,
                bgcolor=ft.colors.WHITE70,
                icon_color=ft.colors.RED,
                on_click=self.parse_with_file,
                col=2
            )
        )

        viewcontrol = ft.ResponsiveRow(control)

        container = ft.Container(
            content = viewcontrol,
            padding = 10,
            bgcolor = ft.colors.WHITE,
            border_radius=10
        )

        return container

def main(page: ft.page):

    serialControl   = SerialControl()
    slideControl    = SlideControl()
    quickControl    = QuickControl()

    page.title      = "WS2812 Light Effect Controller"
    page.theme_mode = ft.ThemeMode.DARK
    page.on_close   = serialControl.disconnect_serial

    page.window_width       = 400
    page.window_min_width   = 400
    page.window_height      = 800
    page.window_min_height  = 800

    page.appbar = ft.AppBar(
        title = ft.Text("WS2812 Light Effect Controller"),
        actions = [
            ft.IconButton(ft.icons.ARROW_RIGHT)
        ]
    )
    
    page.add(
        # Serial Control
        serialControl,
        # Maunal Control
        slideControl,
        # Quick Control
        quickControl
    )    

if __name__ == "__main__":
    ft.app(target = main, assets_dir="img")