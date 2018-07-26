def maxim_peaks_above_min_height(pn_locs, pn_npks, pn_x, n_size, n_min_height):
    """
    Find all peaks above MIN_HEIGHT
    :param pn_locs:
    :param pn_npks:
    :param pn_x:
    :param n_size:
    :param n_min_height:
    :return:
    """
    i = 1
    # pn_npks = 0
    while i < n_size - 1:
        if pn_x[i] > n_min_height and pn_x[i] > pn_x[i - 1]:
            n_width = 1
            while i + n_width < n_size and pn_x[i] == pn_x[i + n_width]:
                n_width += 1
            if pn_x[i] > pn_x[i + n_width] and pn_npks < 15:
                pn_locs[pn_npks] = i
                pn_npks += 1
                i += n_width + 1
            else:
                i += n_width
        else:
            i += 1
    return pn_npks


def maxim_remove_close_peaks(pn_locs, pn_npks, pn_x, n_min_distance):
    """
    Remove peaks separated by less than MIN_DISTANCE

    :param n_locs:
    :param pn_npks:
    :param pn_x:
    :param n_min_distance:
    :return:
    """
    i = 0
    j = 0
    n_old_npks = 0
    n_dist = 0

    maxim_sort_indices_descend(pn_x, pn_locs, pn_npks)

    for i in range(-1, pn_npks):
        n_old_npks = i + 1
        for j in range(i + 1, n_old_npks):
            n_dist = pn_locs[j] - [-1 if i == -1 else pn_locs[i]]
            if n_dist > n_min_distance or n_dist < -n_min_distance:
                pn_locs[pn_npks] = pn_locs[j]
                pn_npks += 1

    maxim_sort_ascend(pn_locs, pn_npks)

    return pn_npks


def maxim_sort_indices_descend(pn_x, pn_index, n_size):
    """
    Sort indices according to descending order (insertion sort algorithm)

    :param pn_x:
    :param pn_index:
    :param n_size:
    :return:
    """
    i = 0
    j = 0
    n_temp = 0
    for i in range(n_size):
        n_temp = pn_index[i]
        for j in range(i, 0, -1):
            if pn_x[n_temp] > pn_x[pn_index[j - 1]]:
                pn_index[j] = pn_index[j - 1]
        pn_index[j] = n_temp


def maxim_sort_ascend(pn_x, n_size):
    """
    Sort array in ascending order (insertion sort algorithm)
    :param pn_x:
    :param n_size:
    :return:
    """
    i = 0
    j = 0
    n_temp = 0
    for i in range(n_size):
        for j in range(i, 0, -1):
            if n_temp < pn_x[j - 1]:
                pn_x[j] = pn_x[j - 1]
        pn_x[j] = n_temp


def maxim_find_peaks(
        pn_locs,
        pn_npks,
        pn_x,
        n_size,
        n_min_height,
        n_min_distance,
        n_max_num):
    """
    Find peaks
    Find at most MAX_NUM peaks above MIN_HEIGHT separated by an least MIN_DISTANCE

    :param pn_locs: peaks location
    :param pn_npks: the numbers of peaks
    :param pn_x:    input
    :param n_size:  the length of input
    :param n_min_height:   threshold
    :param n_min_distance:  8
    :param n_max_num:       5
    :return:
    """
    pn_npks = maxim_peaks_above_min_height(
        pn_locs, pn_npks, pn_x, n_size, n_min_height)
    # print(pn_npks)
    # pn_npks = maxim_remove_close_peaks(pn_locs, pn_npks, pn_x, n_min_distance )
    # print(pn_npks)
    pn_npks = min(pn_npks, n_max_num)

    return pn_npks


# def maxim_heart_rate_and_oxygen_saturation(pun_ir_buffer,
# n_ir_buffer_length, pun_red_buffer, pn_spo2, pch_spo2_valid,
# pn_heart_rate, pch_hr_valid):
def maxim_heart_rate_and_oxygen_saturation(
        pun_ir_buffer,
        n_ir_buffer_length,
        pun_red_buffer):
    """
    Calculate the heart rate and SpO2 level
    By detecting  peaks of PPG cycle and corresponding AC/DC of red/infra-red signal, the ratio for the SPO2 is computed.Since this algorithm is aiming for Arm M0/M3. formaula for SPO2 did not achieve the accuracy due to register overflow.Thus, accurate SPO2 is precalculated and save longo uch_spo2_table[] per each ratio.

    :param pun_ir_buffer:   IR sensor data buffer
    :param n_ir_buffer:     IR sensor data buffer length
    :param pun_red_buffer:   Red sensor data buffer
    :param pn_spo2:          Calculated SpO2 value
    :param pch_spo2_valid:   1 if the calculated SpO2 value is valid
    :param pn_heart_rate:    Calculated heart rate value
    :param pch_hr_valid:     1 if the calculated heart rate value is valid
    :return:                 None
    """
    # remove DC of ir signal
    import matplotlib.pyplot as plt

    uch_spo2_table = [95, 95, 95, 96, 96, 96, 97, 97, 97, 97, 97, 98, 98, 98, 98, 98, 99, 99, 99, 99, 99, 99, 99, 99, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 99, 99, 99, 99, 99, 99, 99, 99, 98, 98, 98, 98, 98, 98, 97, 97, 97, 97, 96, 96, 96, 96, 95, 95, 95, 94, 94, 94, 93, 93, 93, 92, 92, 92, 91, 91, 90, 90, 89, 89, 89, 88, 88, 87, 87, 86, 86, 85, 85, 84, 84, 83, 82, 82, 81, 81, 80, 80, 79, 78, 78, 77, 76, 76, 75, 74, 74, 73, 72, 72, 71, 70, 69, 69, 68, 67, 66, 66, 65, 64, 63, 62, 62, 61, 60, 59, 58, 57, 56, 56, 55, 54, 53, 52, 51, 50, 49, 48, 47, 46, 45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 31, 30, 29, 28, 27, 26, 25, 23, 22, 21, 20, 19, 17, 16, 15, 14, 12, 11, 10, 9, 7, 6, 5, 3, 2, 1]

    MA4_SIZE = 4  # 均值滤波长度
    HAMMING_SIZE = 5
    auw_hamm = [41, 276, 512, 276, 41]

    an_x = []
    an_dx = []
    un_ir_mean = 0

    for k in range(n_ir_buffer_length):
        un_ir_mean += pun_ir_buffer[k]
    un_ir_mean = un_ir_mean / n_ir_buffer_length

    for k in range(n_ir_buffer_length):
        an_x.append(pun_ir_buffer[k] - un_ir_mean)

    # 4 pt Moving Average
    plt.figure()
    plt.plot(an_x)
    for k in range(n_ir_buffer_length - MA4_SIZE):
        n_denom = an_x[k] + an_x[k + 1] + an_x[k + 2] + an_x[k + 3]
        an_x[k] = n_denom / 4

    plt.plot(an_x)

    # get different of smoothed IR signal  查分会去直流，周期信息仍然存在
    for k in range(n_ir_buffer_length - MA4_SIZE - 1):
        an_dx.append(an_x[k + 1] - an_x[k])

    # 2-pt Moving Average to an_dx
    for k in range(n_ir_buffer_length - MA4_SIZE - 2):
        an_dx[k] = (an_dx[k] + an_dx[k + 1]) / 2

    plt.figure()
    plt.plot(an_dx)
    # hamming window
    # flip wave from so that we can detect valley with peak detector
    for i in range(n_ir_buffer_length - HAMMING_SIZE - MA4_SIZE - 2):
        s = 0
        for k in range(i, i + HAMMING_SIZE):
            s -= an_dx[k] * auw_hamm[k - i]

        an_dx[i] = s / 1146   # divide by sum of auw_hamm

    plt.plot(an_dx, color='black')

    n_th1 = 0
    for k in range(n_ir_buffer_length - HAMMING_SIZE):
        n_th1 += an_dx[k] if an_dx[k] > 0 else 0 - an_dx[k]
    n_th1 = n_th1 / (n_ir_buffer_length - HAMMING_SIZE)

    n_npks = 0  # 峰值数目
    an_dx_peak_locs = [0] * 15  # 差值的峰值坐标
    # peak location is acutally index for sharpest location of raw signal
    # since we flipped the signal
    n_npks = maxim_find_peaks(
        an_dx_peak_locs,
        n_npks,
        an_dx,
        n_ir_buffer_length -
        HAMMING_SIZE,
        n_th1,
        8,
        5)  # 这个5是限定了500个点中脉搏上升一定小于5次，但不影响结果

    n_peak_interval_sum = 0

    if n_npks >= 2:
        for k in range(1, n_npks):
            n_peak_interval_sum += an_dx_peak_locs[k] - an_dx_peak_locs[k - 1]
        n_peak_interval_sum = n_peak_interval_sum / (n_npks - 1)
        pn_heart_rate = 6000 / n_peak_interval_sum
        pch_hr_valid = 1
    else:  # 峰值少于两个，无效
        pn_heart_rate = -999
        pch_hr_valid = -1

    an_ir_valley_locs = [0] * 15  # 根据差值的峰值坐标预估的一个波谷的坐标，以半个汉明窗宽往前推
    for k in range(n_npks):
        an_ir_valley_locs[k] = an_dx_peak_locs[k] + int(HAMMING_SIZE / 2)

    # raw value : RED(=y) and IR(=X)
    # we need to assess DC and AC value of ir and red PPG.

    an_x = [0] * 500
    an_y = [0] * 500
    for k in range(n_ir_buffer_length):
        an_x[k] = pun_ir_buffer[k]
        an_y[k] = int(pun_red_buffer[k])

    # find precise min near an_ir_valley_locs
    n_exact_ir_valley_locs_count = 0
    an_exact_ir_valley_locs = [0] * 15
    an_exact_ir_valley = [0] * 15
    an_exact_ir_peak_locs = [0] * 15
    an_exact_ir_peak = [0] * 15

    for k in range(n_npks):
        un_only_once = 1
        m = an_ir_valley_locs[k]
        n_c_min = 16777216
        if m + 5 < n_ir_buffer_length - HAMMING_SIZE and m - 5 > 0:
            for i in range(m - 5, m + 5):
                if an_x[i] < n_c_min:
                    if un_only_once > 0:
                        un_only_once = 0
                    n_c_min = an_x[i]
                    an_exact_ir_valley_locs[k] = i

            if un_only_once == 0:
                n_exact_ir_valley_locs_count += 1

    if n_exact_ir_valley_locs_count < 2:
        pn_spo2 = -999  # do not use SPO2 since signal ratio is out of range
        pch_spo2_valid = 0
        return


    plt.figure()
    plt.plot(an_x)
    # 4 pt MA
    for k in range(n_ir_buffer_length - MA4_SIZE):
        an_temp = (an_x[k] + an_x[k + 1] + an_x[k + 2] + an_x[k + 3])
        an_x[k] = an_temp/4
        an_temp = (an_y[k] + an_y[k + 1] + an_y[k + 2] + an_y[k + 3])
        an_y[k] = an_temp/4

    plt.plot(an_x)

    # using an_exact_ir_valley_locs , find ir-red DC andir-red AC for SPO2 calibration ratio
    # finding AC/DC maximum of raw ir * red between two valley locations
    n_ratio_average = 0
    n_i_ratio_count = 0
    an_ratio = [0] * 15
    for k in range(n_exact_ir_valley_locs_count):
        if an_exact_ir_valley_locs[k] > n_ir_buffer_length:
            pn_spo2 = -999  # do not use SPO2 since valley loc is out of range
            pch_spo2_valid = 0
            return

    # find max between two valley locations
    # and use ratio betwen AC compoent of Ir & Red and DC compoent of Ir & Red
    # for SPO2

    for k in range(n_exact_ir_valley_locs_count - 1):
        n_y_dc_max = -16777216
        n_x_dc_max = -16777216
        n_x_dc_max_idx = 0
        n_y_dc_max_idx = 0
        if an_exact_ir_valley_locs[k + 1] - an_exact_ir_valley_locs[k] > 10:
            for i in range(
                    an_exact_ir_valley_locs[k], an_exact_ir_valley_locs[k + 1]):
                # 从一个波峰到另一份波峰找最大值dc_max
                if an_x[i] > n_x_dc_max:
                    n_x_dc_max = an_x[i]
                    n_x_dc_max_idx = i
                if an_y[i] > n_y_dc_max:
                    n_y_dc_max = an_y[i]
                    n_y_dc_max_idx = i

            n_y_ac = (an_y[an_exact_ir_valley_locs[k + 1]] - an_y[an_exact_ir_valley_locs[k]]
                      ) * (n_y_dc_max_idx - an_exact_ir_valley_locs[k])  # red
            n_y_ac = an_y[an_exact_ir_valley_locs[k]] + n_y_ac / \
                (an_exact_ir_valley_locs[k + 1] - an_exact_ir_valley_locs[k])
            # subracting linear DC compoenents from raw
            n_y_ac = an_y[n_y_dc_max_idx] - n_y_ac

            n_x_ac = (an_x[an_exact_ir_valley_locs[k + 1]] - an_x[an_exact_ir_valley_locs[k]]
                      ) * (n_x_dc_max_idx - an_exact_ir_valley_locs[k])  # ir
            n_x_ac = an_x[an_exact_ir_valley_locs[k]] + n_x_ac / \
                (an_exact_ir_valley_locs[k + 1] - an_exact_ir_valley_locs[k])
            # subracting linear DC compoenents from raw
            n_x_ac = an_x[n_x_dc_max_idx] - n_x_ac

            n_nume = (int(n_y_ac)*n_x_dc_max)   #>>7
            n_denom = (int(n_x_ac)*n_y_dc_max)   #>>7
            if n_denom>0 and n_i_ratio_count<5 and n_nume!=0:
                an_ratio[n_i_ratio_count] = (n_nume*100)/n_denom
                n_i_ratio_count += 1

    maxim_sort_ascend(an_ratio, n_i_ratio_count)
    n_middle_idx = int(n_i_ratio_count/2)

    if n_middle_idx>1:
        n_ratio_average = (an_ratio[n_middle_idx-1] + an_ratio[n_middle_idx])/2
    else:
        n_ratio_average = an_ratio[n_middle_idx]

    if n_ratio_average>2 and n_ratio_average<184:
        n_spo2_calc = uch_spo2_table[int(n_ratio_average)]
        pn_spo2 = n_spo2_calc
        pch_spo2_valid = 1
    else:
        pn_spo2 = -999
        pch_spo2_valid = 0


    print(an_dx_peak_locs)
    print(n_npks)
    print(pn_heart_rate)
    print(n_ratio_average)
    print(pn_spo2)
