'''
4 port PNA calss
Phoenix 2020-03-26
类功能说明:
打开
关闭
查询网分型号
加载校准文件
存SNP文件
存PNG图片
计算指定带宽的中心频率
取出指定trace的S参数
'''
import pyvisa
import time
import matplotlib.pyplot as plt

class PNA:
    '需要传入IP地址'
    def __init__(self, ip, visaDLL=None, *args):
        '生成实例,列出可用网分'
        self.ip = ip
        self.visaDLL = 'c:/windows/system32/visa32.dll' if visaDLL is None else visaDLL
        self.address = 'TCPIP0::%s::inst0::INSTR' % self.ip
        self.resourceManager = pyvisa.ResourceManager(self.visaDLL)
        print(self.resourceManager.list_resources())


    def open(self):
        '打开指定IP的网分,无参'
        self.instance = self.resourceManager.open_resource(self.address)


    def close(self):
        '关闭网分连接,无参'
        if self.instance is not None:
            self.instance.close()
            self.instance = None


    def read_idn(self):
        '读网分型号,无参'
        idn = self.instance.query('*IDN?')
        print(idn)
        return idn


    def loadCSA(self,path = "D:\\", fileName = "8G.csa"):
        '加载校准文件, path(文件路径),fileName(文件名)'
        self.instance.write(':MMEMory:LOAD:CSARchive "{}{}"'.format(path,fileName))
        time.sleep(0.5)
        print("加载校准文件成功!")


    def getCF(self,trNum = "CH1_S12_2", bwLevel = -3.0, chNum = "1" ):
        '功能:取中心频率.trNum(trace名称), bwLevel(设置带宽Level), chNum(Channel号)'
        self.instance.write(':CALCulate{}:PARameter:SELect {}'.format(chNum,trNum)) # 选择tr2 ,"CH1_S12_2"
        time.sleep(0.02)
        # tcp_inst.write(':CALCulate1:MARKer:STATe %d' % (1)) # 打开mark1
        time.sleep(0.02)
        self.instance.write(':CALCulate1:MARKer:BWIDth {}'.format(bwLevel)) # 设置3dB带宽 (-3.0)
        time.sleep(0.02)
        # tcp_inst.write(':CALCulate1:MARKer:FUNCtion:TRACking %d' % (1)) # 打开追踪
        time.sleep(0.02)
        self.instance.write(':SENSe:SWEep:MODE %s' % ('HOLD'))
        time.sleep(0.02)
        BW = self.instance.query_ascii_values(':CALCulate{}:MARKer:BWIDth?'.format(chNum)) # 返回结果
        time.sleep(0.02)
        self.instance.write(':SENSe:SWEep:MODE %s' % ('CONTinuous'))
        print("{}的中心点{}".format(trNum,BW[1]))
        return BW


    def saveSNP(self,snpName = '1.s3p', nPort="1,2,3",snpPath = "D:\\"):
        '保存snp, snpName(文件名), n(数量), snpPath(文件路径)'
        self.instance.write("CALC:DATA:SNP:PORTs:Save '{}','{}{}'".format(nPort,snpPath,snpName))


    def savePNG(self,pngName = '1.png',pngPath = "D:\\"):
        '保存图片,pngName(文件名), pngPath(文件路径)'
        self.instance.write('HCOPy:FILE "{}{}"'.format(pngPath,pngName))


    def getS1p(self, trNum = "CH1_S12_2", chNum = "1", s1pFormat = "DB"):
        '取指定trace的S参数, trNum(trace), chNum(channel), s1pFormat(s参数格式)'
        # 选择trace
        self.instance.write(':CALCulate{}:PARameter:SELect {}'.format(chNum,trNum)) 
        time.sleep(0.02)
        # 设置传输数据格式
        self.instance.write(':FORMat:DATA %s,%d' % ('REAL', 64)) 
        time.sleep(0.02)
        # 设置S参数格式
        self.instance.write(':MMEMory:STORe:TRACe:FORMat:SNP "{}"'.format(s1pFormat)) 
        time.sleep(0.02)

        # 取当前S数据
        self.sdata = self.instance.query_binary_values(':CALCulate%s:DATA? %s' % (chNum,'FDATA'),datatype='d', is_big_endian=True)
        time.sleep(0.02)

        # 取当前频率数据
        self.xdata = self.instance.query_binary_values(':CALCulate%s:X:VALues?' % chNum,datatype='d', is_big_endian=True)
        time.sleep(0.02)

        # # 生成字典以备后续查询
        self.dictData = dict(zip(self.xdata,self.sdata))

        print(len(self.sdata))
        print(self.sdata[:10])
        print(len(self.xdata))
        print(self.xdata[:10])


if __name__ == '__main__':
    ip = '10.0.4.5'
    N5224A = PNA(ip)
    N5224A.open()
    N5224A.read_idn()
    # N5224A.loadCSA(path = "D:\\", fileName = "8G.csa")
    N5224A.getCF(trNum = "CH1_S12_2", bwLevel = -4.0, chNum = "1")
    N5224A.getCF(trNum = "CH1_S31_4", bwLevel = -4.0, chNum = "1")
    # N5224A.saveSNP(snpName = '1.s3p', nPort="1,2,3",snpPath = "D:\\test\\")
    # N5224A.savePNG(pngName = '1.png',pngPath = "D:\\test\\")
    N5224A.getS1p(trNum = "CH1_S12_2", chNum = "1", s1pFormat = "DB")
    plt.plot(N5224A.xdata,N5224A.sdata)
    N5224A.getS1p(trNum = "CH1_S31_4", chNum = "1", s1pFormat = "DB")
    plt.plot(N5224A.xdata,N5224A.sdata)
    N5224A.getS1p(trNum = "CH1_S11_1", chNum = "1", s1pFormat = "DB")
    plt.plot(N5224A.xdata,N5224A.sdata)
    # N5224A.getS1p(trNum = "CH2_S11_6", chNum = "2", s1pFormat = "DB")
    # plt.plot(N5224A.xdata,N5224A.sdata)
    plt.show()


    N5224A.close()