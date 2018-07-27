if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import algorithm as al
    import readLog as rl

    BUFFERLENGHT = 500
    # aun_ir_buffer = [int(l.split()[1]) for l in open("D:\project\XHX\血氧\wm0717-17-2.txt")]
    # aun_red_buffer = [l.split()[0] for l in open("D:\project\XHX\血氧\wm0717-17-2.txt")]

    logPath = "F:\新建文件夹\血氧\logSpo2.txt"
    aun_red_buffer, aun_ir_buffer = rl.readLog(logPath)
    # plt.figure()
    # plt.plot(aun_ir_buffer)
    # plt.figure()
    # plt.plot(aun_red_buffer)
    pn_heart_rate = []
    pch_hr_valid = []
    pn_spo2 = []
    pch_spo2_valid = []

    for i in range(int(len(aun_ir_buffer)/100 - BUFFERLENGHT/100)):
        al.maxim_heart_rate_and_oxygen_saturation(aun_ir_buffer[100*i:100*i+BUFFERLENGHT], 500, aun_red_buffer[100*i:100*i+BUFFERLENGHT], pn_heart_rate, pch_hr_valid, pn_spo2, pch_spo2_valid)
    print("心率： ", pn_heart_rate, " length:", len(pn_heart_rate))
    print("心率是否有效", pch_hr_valid, " length:", len(pch_hr_valid))
    print("血氧： ", pn_spo2, "length: ", len(pn_spo2))
    print("血氧是否有效： ", pch_spo2_valid, " length:", len(pch_spo2_valid))



    startIndex = 500
    pn_heart_rate1 = []
    pch_hr_valid1 = []
    pn_spo21 = []
    pch_spo2_valid1 = []

    al.maxim_heart_rate_and_oxygen_saturation(aun_ir_buffer[startIndex:startIndex + BUFFERLENGHT], 500,
                                              aun_red_buffer[startIndex :startIndex + BUFFERLENGHT], pn_heart_rate1, pch_hr_valid1, pn_spo21, pch_spo2_valid1, 1)
    print(pn_heart_rate1)
    plt.show()


