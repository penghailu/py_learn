import pyvisa
import matplotlib.pyplot as plt
import openpyxl as xl
import time

wb = xl.load_workbook('PNA_config.xlsx') # 打开配置文件
sheet = wb.active # 激活工作表
tcp_addr = 'TCPIP0::{IP}::inst0::INSTR'.format(IP=sheet.cell(row=1,column=2).value) # 设置网分地址

# 打开网分
rm = pyvisa.ResourceManager()
rm.list_resources()
try:
    tcp_inst = rm.open_resource(tcp_addr)
    print(tcp_inst.query("*IDN?"))
    time.sleep(0.01)
    tcp_inst.timeout = 1000
except:
    print("打开网分错误, 请检查配置文件IP地址!!")

# 加载配置文件
""" try:
    tcp_inst.write(':MMEMory:LOAD:CSARchive "D:\\8G.csa"')
    time.sleep(0.5)
    print("加载校准文件成功!")
except:
    print("校准文件不存在!") """

# 查询tr2, s12中心频点
""" time.sleep(0.02)
tcp_inst.write(':CALCulate:PARameter:SELect "CH1_S12_2"') # 选择tr2, s12
time.sleep(0.02)
# tcp_inst.write(':CALCulate1:MARKer:STATe %d' % (1)) # 打开mark1
time.sleep(0.02)
tcp_inst.write(':CALCulate1:MARKer:BWIDth %G' % (-3.0)) # 设置3dB带宽
time.sleep(0.02)
# tcp_inst.write(':CALCulate1:MARKer:FUNCtion:TRACking %d' % (1)) # 打开追踪
time.sleep(0.02)
tcp_inst.write(':SENSe:SWEep:MODE %s' % ('HOLD'))
time.sleep(0.02)
BW_S12 = tcp_inst.query_ascii_values(':CALCulate1:MARKer:BWIDth?') # 返回结果
time.sleep(0.02)
tcp_inst.write(':SENSe:SWEep:MODE %s' % ('CONTinuous'))

bandwidth_S12 = BW_S12[0]
centerFrequency_S12 = BW_S12[1]
q_S12 = BW_S12[2]
loss_S12 = BW_S12[3]

print("S12中心点:",BW_S12[1])

# 查询tr4, s31中心频点
time.sleep(0.02)
tcp_inst.write(':CALCulate:PARameter:SELect "CH1_S31_4"') # 选择tr2, s12
time.sleep(0.02)
# tcp_inst.write(':CALCulate1:MARKer:STATe %d' % (1)) # 打开mark1
time.sleep(0.02)
tcp_inst.write(':CALCulate1:MARKer:BWIDth %G' % (-3.0)) # 设置3dB带宽
time.sleep(0.02)
# tcp_inst.write(':CALCulate1:MARKer:FUNCtion:TRACking %d' % (1)) # 打开追踪
time.sleep(0.02)
tcp_inst.write(':SENSe:SWEep:MODE %s' % ('HOLD'))
time.sleep(0.02)
BW_S31 = tcp_inst.query_ascii_values(':CALCulate1:MARKer:BWIDth?') # 返回结果
time.sleep(0.02)
tcp_inst.write(':SENSe:SWEep:MODE %s' % ('CONTinuous'))

print("S31中心点:",BW_S31[1]) """



tcp_inst.close()