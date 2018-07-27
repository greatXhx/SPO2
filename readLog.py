def readLog(path):
    import re

    line = []
    f = open(path)  # 返回一个文件对象
    lines = f.readlines()#读取全部内容
    reg = r'SPO2DeviceStream2: (.{12})'#只取SessionId=字符后面32位字符串
    wordreg = re.compile(reg)
    wordreglist = []
    aun_ir_buffer = []
    aun_red_buffer = []
    for line in lines:
        if re.findall(wordreg, line):
            wordreglist.append(re.findall(wordreg, line))
            aun_red_buffer.append(int(re.findall(wordreg, line)[0][:5]))
            aun_ir_buffer.append(int(re.findall(wordreg, line)[0][6:]))

    return aun_red_buffer, aun_ir_buffer
