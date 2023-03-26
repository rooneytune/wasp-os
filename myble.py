
import wasp
import widgets

import ble
from ubluepy import Service, Characteristic, UUID, Peripheral, constants

# from ubluepy import UUID
# from ubluepy import Service
# from ubluepy import Peripheral
# from ubluepy import Characteristic



class MyBleApp():
    """A hello ROONEY application for wasp-os."""
    """Name must be 7 chars MAX. Errors occur if longer"""
    NAME = "BLE"
    FILEVERSION = "1.26"

    def __init__(self,msg="BLE App" ):

        self.msg = msg + " v{}".format(FILEVERSION)
        self._button = widgets.Button(10,10,80,40,"Start")
        
        self._bleCheckbox = widgets.Checkbox(10,60,"BLE")
        self._bleName="RoonTime"
        self._bleInfo="NotSet"
        
       # self._button = widgets.Button(10,10,80,30,"Start")
       # self._bleToggleButton = wasp.widgets.ToggleButton(bleButtonTemp)
        self._buttonPressCount = 0
        self._checkboxState = True
        self._touchCount =0 
        

    def _updateLabels(self):
        draw = wasp.watch.drawable
        #draw.set_font(wasp. sans18)
        draw.set_color(wasp.system.theme('mid'))

        checkboxInfo = "Checkbox: {}".format(self._checkboxState)
        draw.string(checkboxInfo, 0, 140, width=240)
        
        progressInfo = "BleInfo: {}".format(self._bleInfo)
        draw.string(progressInfo, 0, 180, width=240)

        touchInfo = "Touch Count: {}".format(self._touchCount)
        draw.string(touchInfo, 0, 200, width=240)

    def foreground(self):
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH |
                    wasp.EventMask.BUTTON |
                wasp.EventMask.NEXT)

    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()
        #Print app name
        draw.string(self.msg, 0, 108, width=240)
        #Draw UI
        self._button.draw()
        self._bleCheckbox.draw()
    
        #self._bleToggleButton.draw()
      


    def press(self, button, state):
       # print("press event detected")
        self._buttonPressCount =self._buttonPressCount+1

        # if self.test == 'Alarm':
        #     self._test_alarm()
        # elif self.test == 'Button':
        #     draw.string('{}: {}'.format(button, state), 0, 108, width=240)
        # elif self.test == 'Crash':
        #     self.crash()
        # elif self.test == 'String':
        #     self._benchmark_string()
        # elif self.test == 'Touch':
        #     draw.string('Button', 0, 108, width=240)
        self._update()

    def touch(self, event):
       # print("touch event detected")
        
        if self._bleCheckbox.touch(event):
            self._checkboxState = not self._checkboxState
            print('ble checkbox toggled: {}'.format(self._checkboxState))
            if self._checkboxState==True:
                #ble.enable()
                self._setupBleService()
            else:
                #ble.disable()
                print("ble check off")

        elif self._button.touch(event):
            self._touchCount+=1
            #ble.disable()
            self._updateBleInfo("ble-Disabled")
            

        self._update()

    def _update(self):
        self._updateLabels()

    def _updateBleInfo(self, msg="Default"):
        self._bleInfo = msg
        self._updateLabels()        

    def _setupBleService(self):

        ble.disable()
        
        uuid_env_sense = UUID("0x181A")  # Environmental Sensing service
        uuid_temp = UUID("0x2A6E")  # Temperature characteristic
        self._updateBleInfo("Uid Set")

        serv_env_sense = Service(uuid_env_sense)
        self._updateBleInfo("Svc Set")       

        temp_props = Characteristic.PROP_NOTIFY | Characteristic.PROP_READ
        temp_attrs = Characteristic.ATTR_CCCD
        char_temp = Characteristic(uuid_temp, props=temp_props, attrs=temp_attrs)
        self._updateBleInfo("Chars Set")

        serv_env_sense.addCharacteristic(char_temp)
        self._updateBleInfo("Chars Add")

        periph = Peripheral()
        self._updateBleInfo("Perif. 1")
        periph.addService(serv_env_sense)
        self._updateBleInfo("Perif. 2")
       # periph.setConnectionHandler(self.event_handler)
        periph.advertise(device_name="Roon_Time", services=[serv_env_sense])
        self._updateBleInfo("Advertising")

    def event_handler(id, handle, data):
        pass