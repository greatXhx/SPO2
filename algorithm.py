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
    while i<n_size-1:
        if pn_x[i] > n_min_height and pn_x[i] > pn_x[i-1]:
            n_width = 1
            while i+n_width < n_size and pn_x[i] == pn_x[i+n_width]:
                n_width += 1
            if pn_x[i] > pn_x[i+n_width] and pn_npks < 15:
                pn_locs[pn_npks] = i
                pn_npks += 1
                i += n_width +1
            else:
                i += n_width
        else:
            i += 1

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
        n_old_npks = i+1
        for j in range(i+1, n_old_npks):
            n_dist = pn_locs[j] - [-1 if i==-1 else pn_locs[i]]
            if n_dist>n_min_distance or n_dist < -n_min_distance:
                pn_locs[pn_npks] = pn_locs
                pn_npks += 1

    maxim_sort_ascend(pn_locs, pn_npks);

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
            if pn_x[n_temp] > pn_x[pn_index[j-1]]:
                pn_index[j] = pn_index[j-1]
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
        for j in range(i , 0, -1):
            if n_temp < pn_x[j-1]:
                pn_x[j] = pn_x[j-1]
        pn_x = n_temp


def maxim_find_peaks(pn_locs, pn_npks, pn_x, n_size, n_min_height, n_min_distance, n_max_num):
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
    maxim_peaks_above_min_height(pn_locs, pn_npks, pn_x, n_size, n_min_height )
    maxim_remove_close_peaks(pn_locs, pn_npks, pn_x, n_min_distance )
    pn_npks = min(pn_npks, n_max_num )






# def maxim_heart_rate_and_oxygen_saturation(pun_ir_buffer, n_ir_buffer_length, pun_red_buffer, pn_spo2, pch_spo2_valid, pn_heart_rate, pch_hr_valid):
def maxim_heart_rate_and_oxygen_saturation(pun_ir_buffer, n_ir_buffer_length, pn_heart_rate, pch_hr_valid):
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

    MA4_SIZE = 4    #均值滤波长度
    HAMMING_SIZE = 5
    auw_hamm = [41, 276, 512, 276, 41]

    an_x = []
    an_dx = []
    un_ir_mean = 0
    for k in range(n_ir_buffer_length):
       un_ir_mean += pun_ir_buffer[k]
    un_ir_mean = un_ir_mean/n_ir_buffer_length

    for k  in range(n_ir_buffer_length):
       an_x.append(pun_ir_buffer[k] - un_ir_mean)

    # 4 pt Moving Average
    plt.figure()
    plt.plot(an_x)
    for k in range(n_ir_buffer_length-MA4_SIZE):
        n_denom = an_x[k] + an_x[k+1] + an_x[k+2] + an_x[k+3]
        an_x[k] = n_denom/4

    plt.plot(an_x)

    # get different of smoothed IR signal  查分会去直流，周期信息仍然存在
    for k in range(n_ir_buffer_length - MA4_SIZE - 1):
        an_dx.append(an_x[k+1] - an_x[k])

    # 2-pt Moving Average to an_dx
    for k in range(n_ir_buffer_length - MA4_SIZE - 2):
        an_dx[k] = (an_dx[k] + an_dx[k+1])/2


    plt.figure()
    plt.plot(an_dx)
    # hamming window
    # flip wave from so that we can detect valley with peak detector
    for i in range(n_ir_buffer_length - HAMMING_SIZE - MA4_SIZE - 2):
        s=0
        for k in range(i, i+HAMMING_SIZE):
            s -= an_dx[k]*auw_hamm[k-i]

        an_dx[i] = s/1146   # divide by sum of auw_hamm

    plt.plot(an_dx, color = 'black')

    n_th1 = 0
    for k in range(n_ir_buffer_length - HAMMING_SIZE):
        n_th1 += an_dx[k] if an_dx[k]>0 else 0-an_dx[k]
    n_th1 = n_th1/(n_ir_buffer_length - HAMMING_SIZE)

    n_npks = 0    #峰值数目
    an_dx_peak_locs = [0]*15
    #peak location is acutally index for sharpest location of raw signal since we flipped the signal
    maxim_find_peaks(an_dx_peak_locs, n_npks, an_dx, n_ir_buffer_length - HAMMING_SIZE, n_th1, 8, 5)

    n_peak_interval_sum = 0

    if n_npks>=2:
        for k in range(1, n_npks):
            n_peak_interval_sum += an_dx_peak_locs[k] - an_dx_peak_locs[k-1]
        n_peak_interval_sum = n_peak_interval_sum/(n_npks-1)
        pn_heart_rate = 6000/n_peak_interval_sum
        pch_hr_valid = 1

    print(an_dx_peak_locs)
    print(n_npks)






