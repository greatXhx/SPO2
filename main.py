if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import algorithm as al
    aun_ir_buffer = [int(l.split()[1]) for l in open("D:\project\XHX\血氧\wm0717-17-2.txt")]
    aun_red_buffer = [l.split()[0] for l in open("D:\project\XHX\血氧\wm0717-17-2.txt")]
    pn_heart_rate = 0
    pch_hr_valid = -1
    al.maxim_heart_rate_and_oxygen_saturation(aun_ir_buffer[0:500], 500, aun_red_buffer[0:500])
    plt.show()

