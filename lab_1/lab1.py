import os
import math
import pandas
import datetime


class Telephony:
    def __init__(self, data, phone_number):
        self.call_cost_night = 4
        self.call_cost_day = 2
        self.call_duration = 0
        self.incomming_call_cost = self.calculate_call_cost(data=data, msisdn_type='msisdn_origin', phone_number=phone_number)
        self.outcoming_call_cost = self.calculate_call_cost(data=data, msisdn_type='msisdn_dest', phone_number=phone_number)
        self.billing = self.incomming_call_cost + self.outcoming_call_cost

    def calculate_call_cost(self, data, msisdn_type, phone_number):

        call_cost = 0

        for i in range(data.shape[0]):
            if data[msisdn_type][i] == phone_number:
                call_time = datetime.datetime.strptime(data['timestamp'][i], '%Y-%m-%d %H:%M:%S')
                time_border = call_time.replace(hour=0, minute=30, second=0)
                if time_border <= call_time:
                    call_duration = math.ceil(data['call_duration'][i])
                    self.call_duration += call_duration
                    call_cost += call_duration * self.call_cost_day
                else:
                    time_delta = time_border - call_time
                    time_delta = time_delta.seconds / 60
                    call_duration = math.ceil(data['call_duration'][i])
                    self.call_duration += call_duration
                    above_tariff = call_duration-time_delta
                    if above_tariff > 0:
                        call_cost += above_tariff * self.call_cost_day
                        call_cost += (call_duration - above_tariff) * self.call_cost_night
                    else:
                        call_cost += call_duration * self.call_cost_night

        return call_cost


class SMS:
    def __init__(self, data, phone_number):
        self.sms_cost = 1.5
        self.sms_number = 0
        self.billing = self.calculate_sms_cost(data, phone_number)

    def calculate_sms_cost(self, data, phone_number):
        cost = 0
        for i in range(data.shape[0]):
            if data['msisdn_origin'][i] == phone_number:
                self.sms_number += data['sms_number'][i]
                cost += data['sms_number'][i] * self.sms_cost

        return cost

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data = pandas.read_csv(current_dir + '\\data.csv')
    phone_number = 933156729

    telephony = Telephony(data=data, phone_number=phone_number)
    sms = SMS(data=data, phone_number=phone_number)

    print("Telephony billing: " + str(telephony.billing))
    print("SMS billing: " + str(sms.billing))

    return


if __name__ == "__main__":
    main()