import pandas
import math
import matplotlib.dates as mdates, datetime
from pandas.plotting import register_matplotlib_converters

import datetime
import matplotlib.pyplot as plt

DUMP_FILE = 'dmp.xls'

class Internet:
    def __init__(self, dmp_table, ip_address):
        self.internet_cost = 2
        self.session_time_list = []
        self.traffic_bytes_list = []
        self.traffic_count = self.calculate_internet_traffic(dmp_table, ip_address) / (1024 ** 2)
        self.billing = math.ceil(self.traffic_count) * self.internet_cost

    def calculate_internet_traffic(self, dmp_table, ip_address):
        traffic_count = 0
        for i in range(dmp_table.shape[0]):
            if dmp_table['Src IP Addr:Port'][i].find(ip_address) != -1:
                traffic_count += dmp_table['In Byte'][i]
                tmp_time = datetime.datetime.fromtimestamp(dmp_table['Date first seen'][i].timestamp())
                self.session_time_list.append(tmp_time)
                self.traffic_bytes_list.append(dmp_table['In Byte'][i])


        return traffic_count


def main():
    register_matplotlib_converters()

    xls_file = pandas.ExcelFile(DUMP_FILE)
    dmp_table = xls_file.parse("dmp")
    ip_address = '87.245.198.147'

    print('Src IP Addr: ' + ip_address)
    internet = Internet(dmp_table, ip_address)

    for i in range(len(internet.session_time_list)):
        print("Date seen: " + str(internet.session_time_list[i]) + ' - In Byte: ' + str(internet.traffic_bytes_list[i]))

    print("Total traffic (bytes): " + str(internet.traffic_count))
    print("Total traffic (Kb): " + str(internet.traffic_count / 1024))
    print("Total traffic (Mb): " + str(internet.traffic_count / (1024 ** 2)))
    print("Total cost (Rub/Mb): " + str(internet.billing))

    fig, ax = plt.subplots()
    ax.plot(internet.session_time_list, internet.traffic_bytes_list)

    # format the ticks
    ax.xaxis.set_major_locator(mdates.MinuteLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(mdates.MinuteLocator())

    ax.set_title("График зависимости трафик от времени")
    ax.set_xlabel("Time", fontsize=1)
    ax.set_ylabel("Traffic", fontsize=14)
    ax.set_xlim(internet.session_time_list[0], internet.session_time_list[len(internet.session_time_list)-1])
    ax.minorticks_on()

    plt.show()

    return

if __name__ == '__main__':
    main()