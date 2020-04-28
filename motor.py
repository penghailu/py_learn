'''
2020-04-02


'''
import time
import pyvisa


class Motor():
    '传入agilent IO的com地址， 波特率等设置转到agilent IO设置'
    def __init__(self, com):
        '生成串口实例，列出可用端口'
        self.com = com
        self.rm = pyvisa.ResourceManager()
        print(self.rm.list_resources())

    def open(self):
        '打开串口，无参'
        self.motor = self.rm.open_resource(self.com)
        self.motor.read_termination = '\r\n'
        self.motor.timeout = 5000

    def close(self):
        '关闭串口'
        self.rm.close()

    def returnZero(self, ch):
        '电机下归零，ch为通道号，0表示Rx，1表示Tx；'
        self.motor.write('SetReturnZero %d' % ch)
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                if ch == 1:
                    print("TX电机归零成功！\n")
                else:
                    print("RX电机归零成功！\n")
                break

    def setMotorPos(self, ch, postion):
        '设置电机位置，归零之后才可用，ch为通道号，0表示Rx，1表示Tx；postion步长'
        self.motor.write("SetMotorPos %d %d" % (ch, postion))
        time.sleep(1)
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                if ch == 1:
                    print("TX电机到达%d！\n" % postion)
                else:
                    print("RX电机到达%d！\n" % postion)
                break

    def showMotorInfo(self, ch):
        '显示电机详细信息,ch为通道号，0表示Rx，1表示Tx；'
        self.motor.write('ShowMotorDeteInfo %d' % ch)
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                if ch == 1:
                    print("TX电机显示完成\n")
                else:
                    print("RX电机显示完成！\n")
                break

    def saveBarCode(self, flag, codeValue):
        '写入标签数据，[flag]为标志位。0：接口电机组件电子标签，1：发射电机组件电子标签，2：滤波器电子标签'
        self.motor.write('SaveBarCode %d %s' % (flag, codeValue))
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                if flag == 0:
                    print("RX电机条码写完成\n")
                elif flag == 1:
                    print("TX电机条码写完成\n")
                elif flag == 2:
                    print("滤波器条码写完成\n")
                else:
                    print("条码写入错误")
                break

    def helpMotor(self):
        "显示电机控制器帮助文件"
        self.motor.write('help')
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                print('帮忙文件显示完成！')
                break

    def showBarCode(self, ch):
        '显示条码，ch为标志位。0：接口电机组件电子标签，1：发射电机组件电子标签，2：滤波器电子标签'
        self.motor.write('ShowBarCode %d' % ch)
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                print('BarCode显示完成！')
                break

    def saveFrelist(self, freDict, ch):
        '写表，freDict表字典，ch为通道号，0表示Rx，1表示Tx；'
        freDict = dict(freDict)
        self.motor.write('SaveFreqPosTab 0 0 0 0')
        for each in freDict:
            self.motor.write('SaveFreqPosTab %d %d %d 1' % (each[0], each[1], ch))
        self.motor.write('SaveFreqPosTab 0 0 0 2')
        while True:
            end = self.motor.read()
            print(end)
            if end == 'shell end.':
                print('写EEPROM完成！')
                break


if __name__ == '__main__':
    com = 'ASRL4::INSTR'
    motor = Motor(com)
    motor.open()
    # motor.returnZero(0)
    # motor.returnZero(1)
    motor.setMotorPos(0, 100)
    motor.setMotorPos(0, 200)
    motor.setMotorPos(0, 300)
    motor.setMotorPos(0, 400)
    motor.setMotorPos(0, 500)
    # motor.setMotorPos(1, 3000)
    # motor.showMotorInfo(1)
    motor.showMotorInfo(0)
    motor.returnZero(0)
    motor.showMotorInfo(0)
    # motor.saveBarCode(1, '000003881502164700095')
    # motor.helpMotor()
    # motor.showBarCode(2)
    motor.close()



