import os
import math
import pandas
import datetime

def calculate_call_cost(data, msisdn_type, phone_number):

    call_cost = 0
    call_rate_before = 4
    call_rate_after = 2

    for i in range(data.shape[0]):
        if data[msisdn_type][i] == phone_number:
            call_time = datetime.datetime.strptime(data['timestamp'][i], '%Y-%m-%d %H:%M:%S')
            time_border = call_time.replace(hour=0, minute=30, second=0)
            if time_border <= call_time:
                call_duration = math.ceil(data['call_duration'][i])
                call_cost += call_duration * call_rate_after
            else:
                time_delta = time_border - call_time
                time_delta = time_delta.seconds / 60
                call_duration = math.ceil(data['call_duration'][i])
                above_tariff = call_duration-time_delta
                if above_tariff > 0:
                    call_cost += above_tariff * call_rate_after
                    call_cost += (call_duration - above_tariff) * call_rate_before
                else:
                    call_cost += call_duration * call_rate_before

    return call_cost


def calculate_sms_cost(data, phone_number):

    sms_cost = 0
    sms_rate = 1.5

    for i in range(data.shape[0]):
        if data['msisdn_origin'][i] == phone_number:
            sms_cost += data['sms_number'][i] * sms_rate

        if data['msisdn_dest'][i] == phone_number:
            sms_cost += data['sms_number'][i] * sms_rate

    return sms_cost

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    data = pandas.read_csv(current_dir + '\\data.csv')

    outcoming_call_cost = calculate_call_cost(data=data, msisdn_type='msisdn_origin', phone_number=933156729)
    incoming_call_cost = calculate_call_cost(data=data, msisdn_type='msisdn_dest', phone_number=933156729)
    telephony_billing = outcoming_call_cost + incoming_call_cost
    sms_billing = calculate_sms_cost(data=data, phone_number=933156729)

    print("Telephony billing: " + str(telephony_billing))
    print("SMS billing: " + str(sms_billing))

    return


if __name__ == "__main__":
    main()