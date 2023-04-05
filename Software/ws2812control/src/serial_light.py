import serial
import time

class ws2812ser:
    def __init__(self,
                comport: str,
                baud: int = 115200, 
                timeout: int = 1000):
        
        self.ser        = None
        self.comport    = comport
        self.baud       = baud
        self.timeout    = timeout
        self._isoperate = False

    def connect(self):
        
        if (self.ser is None) or (self.ser.is_open == False):
            self.ser = serial.Serial(port       = self.comport,
                                     baudrate   = self.baud, 
                                     timeout    = self.timeout)

            while(self.ser.is_open == False):
                pass 

    def disconnect(self):
        if (self.ser is not None) and (self.ser.is_open == True):
            self.ser.close()

            while(self.ser.is_open == True):
                pass

    def sendSerial(self,
                   mode: str,
                   wsval: list = [0, 0, 0]):
        
        if (self.ser is not None) and (self.ser.is_open == True) and (self._isoperate == False):
            self._isoperate = True
            srcarray = []

            if (mode == 'r'):
                srcarray = [0x01, 0x00, 0x00, 0x00, 0x00, 0x79]
            elif (mode == 'g'):
                srcarray = [0x01, 0x01, 0x00, 0x00, 0x00, 0x79]
            elif (mode == 'b'):
                srcarray = [0x01, 0x02, 0x00, 0x00, 0x00, 0x79]
            elif (mode == 'custom'):
                srcarray = [0x01, 0x03, int(wsval[0]), int(wsval[1]), int(wsval[2]), 0x79]
            elif (mode == 'close'):
                srcarray = [0x00, 0x00, 0x00, 0x00, 0xFF, 0x79]
            else:
                pass 

            print("> Run Command: {}".format(srcarray))

            barray = bytearray(srcarray)
            self.ser.write(barray)

            while (self.ser.writable() == False): 
                pass
                
            self._isoperate = False

    def sendSerialWithTiming(self, 
                             parseData: dict):
        
        if (self.ser is not None) and (self.ser.is_open == True) and (self._isoperate == False):
            
            self._isoperate = True
            start = time.time()

            for li in parseData:
                while True and li["time"] > 0:
                    end = time.time()
                    if round(end - start, 3) >= float(li["time"]):
                        break
                
                barray = bytearray(li["light"])
                self.ser.write(barray)

                print("> Run Command: {}s\t{}".format(li["time"], li["light"]))

                while (self.ser.writable() == False): 
                    pass
            
            print("> Complete!")

            self._isoperate = False