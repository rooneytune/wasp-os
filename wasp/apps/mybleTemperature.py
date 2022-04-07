
import time
import wasp
import widgets
from machine import RTCounter

import ble
from ubluepy import Service, Characteristic, UUID, Peripheral, constants
from apps.chrono import ChronoApp

bleEventMessage = "NotSet"

class MyBleApp():
    """A hello ROONEY application for wasp-os."""
    """Name must be 7 chars MAX. Errors occur if longer"""
    NAME = "BLE"
    

    @staticmethod 
    def getAppVersion():
        appVersion = "2.69"   
        return appVersion

    def __init__(self,msg="BLE App" ):
        self.firstDrawComplete = False
        self._msg = "NotSet"
        self._button = widgets.Button(10,10,150,50,"Status")
        
        self._bleCheckbox = widgets.Checkbox(10,70,"BLE")
        self._bleName="RoonTime"
        self._bleInfo="NotSet"
        
       # self._button = widgets.Button(10,10,80,30,"Start")
       # self._bleToggleButton = wasp.widgets.ToggleButton(bleButtonTemp)
        self._buttonPressCount = 0
        self._checkboxState = False
        self._touchCount =0 
        self._bleUpdateCount = 0
        self._notifEnabled = False

        

    def _updateLabels(self):

        global bleEventMessage
        draw = wasp.watch.drawable
        #draw.set_font(wasp. sans18)
        draw.set_color(wasp.system.theme('mid'))

        progressInfo = "BleInf: {}".format(self._bleInfo)
        draw.string(progressInfo, 0, 120, width=240)

        bleEventInfo = "BleEvt: {}".format(bleEventMessage)
        draw.string(bleEventInfo, 0, 150, width=240)
        

        # touchInfo = "Touch Count: {}".format(self._touchCount)
        # draw.string(touchInfo, 0, 200, width=240)

    def foreground(self):                
        
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH |
                    wasp.EventMask.BUTTON |
                wasp.EventMask.NEXT)
        wasp.system.request_tick(2000)


    def _draw(self):
        draw = wasp.watch.drawable
        draw.fill()

        if not self.firstDrawComplete:
            #Draw static Ui elements
            self.msg = " v{}".format(self.getAppVersion())
            #Print app name
            draw.string(self.msg, 160, 5, width=80)
            self._button.draw()

        self._bleCheckbox.draw()
    
        #self._bleToggleButton.draw()
      
        self.firstDrawComplete= True

    def press(self, button, state):
       # print("press event detected")
        self._buttonPressCount =self._buttonPressCount+1
        #wasp.system.switch(clock)
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
        #wasp.system.switch(wasp.system.quick_ring[0])
        wasp.system.switch(ChronoApp())

    #def background(self):
        
        #super().background()


    def touch(self, event):
       # print("touch event detected")
        global bleEventMessage
        if self._bleCheckbox.touch(event):
            
            self._checkboxState = self._bleCheckbox.state
        #     print('ble checkbox toggled: {}'.format(self._checkboxState))
            if self._checkboxState==True:
                self._setupBleService()
            else:  
                ble.disable()
        elif self._button.touch(event):
            self._touchCount+=1
            
            self._updateBleInfo(bleEventMessage)
            

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

        global serv_env_sense
        serv_env_sense = Service(uuid_env_sense)
        self._updateBleInfo("Svc Set")       

        temp_props = Characteristic.PROP_NOTIFY | Characteristic.PROP_READ | Characteristic.PROP_WRITE
        #temp_props = Characteristic.PROP_READ
        temp_attrs = Characteristic.ATTR_CCCD
        global char_temp
        char_temp = Characteristic(uuid_temp, props=temp_props, attrs=temp_attrs)

        self._updateBleInfo("Chars Set")

        serv_env_sense.addCharacteristic(char_temp)
        self._updateBleInfo("Chars Add")

        global periph
        periph = Peripheral()
        periph.addService(serv_env_sense)
        periph.setConnectionHandler(event_handler)
        self._updateBleInfo("Set handler")
        
        periph.advertise(device_name="Roon_Time", services=[serv_env_sense])
        self._updateBleInfo("Advertising")


        # use RTC1 as RTC0 is used by bluetooth stack
        # set up RTC callback every 5 second
        #rtc = RTCounter(1, period=50, mode=RTCounter.PERIODIC, callback=self.rtcTimerTick(self=self))


    def tick(self, ticks):
        """Periodic callback to update the display."""
       
        
        global bleEventMessage
        
        # if self._notifEnabled:
            
        #     global char_temp
            

            #char_temp.write(bytearray([temp & 0xFF, temp >> 8]))
            #char_temp.write(bytearray([self._bleUpdateCount & 0xFF, self._bleUpdateCount >> 8]))
            # char_temp.write(bytearray(updateText,'utf-8'))
        
        if self._checkboxState == True:
            self._bleUpdateCount+=1
            updateText = "{} updates".format(self._bleUpdateCount)
            wasp.system.keep_awake()
            self._updateBleInfo(updateText)
            self._updateLabels()
        

    def rtcTimerTick(timer_id,self):
        
        global char_temp
        global bleEventMessage
        if self._notifEnabled:
            # measure chip temperature
            temp = 25
            temp = temp * 100
            #char_temp.write(bytearray([temp & 0xFF, temp >> 8]))
            #char_temp.write(bytearray('Hello roon','utf-8'))
            bleEventMessage= "set bytearray"
        else:
            bleEventMessage= "notif false"
    


def event_handler(id, handle, data):

    global periph
    global serv_env_sense
    global bleEventMessage

    if id == constants.EVT_GAP_CONNECTED:
        # indicated 'connected'
        
        bleEventMessage= "conn"
        

    elif id == constants.EVT_GAP_DISCONNECTED:
        # stop low power timer
        bleEventMessage="discon"
        # restart advertisment
        periph.advertise(device_name="Roon_Time2", services=[serv_env_sense])

    elif id == constants.EVT_GATTS_WRITE:
        global char_temp
        temp = 25
        char_temp.write(bytearray([temp & 0xFF, temp >> 8]))
        bleEventMessage="gattWrite"
    elif id == constants.EVENT_READ:
        # write to this Characteristic is to CCCD
        bleEventMessage="gattRead"
        #if int(data[0]) == 1:
        #   bleEventMessage="write-Start"
        # else:
        #     notif_enabled = False
        #     # stop low power timer
        #     bleEventMessage="write-stop"