import os
import pandas
import locale
import datetime
import io
from reportlab.pdfbase import pdfmetrics
from PyPDF4 import PdfFileReader, PdfFileWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from num2words import num2words

from lab_1.lab1 import Telephony, SMS
from lab_2.lab2 import Internet

CHEQUE_FORM = "form.pdf"
CHEQUE_FILE = "bill.pdf"

class ServicesBill:
    def __init__(self, services_list):
        self.bill_form = self.initialize_bill_form()
        self.data_to_fill = self.create_new_page(services_list)
        self.services_list = services_list

        new_pdf = PdfFileReader(self.data_to_fill)
        self.bill_form.mergePage(new_pdf.getPage(0))
        output = PdfFileWriter()
        output.addPage(self.bill_form)

        outputStream = open(CHEQUE_FILE, "wb")
        output.write(outputStream)
        outputStream.close()

    @staticmethod
    def initialize_bill_form():
        form_file = open(CHEQUE_FORM, 'rb')
        pdf = PdfFileReader(form_file)
        page = pdf.getPage(0)

        return page

    @staticmethod
    def fill_service_data(my_canvas, y_pos, index, name, service_count, measure, rate, payment_amount):
        my_canvas.drawString(44, y_pos, index)
        my_canvas.drawString(85, y_pos, name)
        my_canvas.drawString(315, y_pos, service_count)
        my_canvas.drawString(350, y_pos, measure)
        my_canvas.drawString(379, y_pos, rate)
        my_canvas.drawString(466, y_pos, payment_amount)
        return

    def create_new_page(self, services_list):
        pdfmetrics.registerFont(TTFont("Arial", "Arial.ttf"))
        pdfmetrics.registerFont(TTFont("Arial-Bold", "Arial_Bold.ttf"))
        packet = io.BytesIO()

        # create a new PDF with Reportlab
        my_canvas = canvas.Canvas(packet, pagesize=letter)
        my_canvas.setFont("Arial", 10)

        # Банк
        my_canvas.drawString(35, 780, "АО \"АЛЬФА-БАНК\" Г.МОСКВА")
        # Бик
        my_canvas.drawString(353, 792, "044525974")
        # Номер счета банка
        my_canvas.drawString(353, 778, "40817810700007591910")
        # ИНН
        my_canvas.drawString(58, 754, "7710140679")
        # КПП
        my_canvas.drawString(201, 754, "773401001")
        # Номер счета получателя
        my_canvas.drawString(353, 754, "30101810145250000974")
        # Получатель
        my_canvas.drawString(35, 730, "ПАО \"РОСТЕЛЕКОМ\"")

        my_canvas.setFont("Arial-Bold", 14)
        # Номер счета на оплату
        my_canvas.drawString(160, 688, "92")
        # Дата
        current_date = datetime.datetime.now()
        my_canvas.drawString(198, 688, str(current_date.day) + current_date.strftime("%b"))
        # Год
        my_canvas.drawString(254, 688, current_date.strftime("%y"))

        my_canvas.setFont("Arial", 10)
        # Поставщик
        my_canvas.drawString(100, 654, "Макрорегиональный филиал \"СЕВЕРО-ЗАПАД\" ПАО \"РОСТЕЛЕКОМ\",")
        my_canvas.drawString(100, 643, "Адрес: г.Санкт-Петербург, ИНН 7707049388, Р/С 40702810855000100555")
        # Получатель
        my_canvas.drawString(83, 609, "Игнатьева К.Е., Л/С 278012380547")
        # Основание
        my_canvas.drawString(85, 586, "№" + current_date.strftime("%y%m%d") + " от " + current_date.strftime("%d.%m.%Y"))

        my_canvas.setFont("Arial", 8)
        my_canvas.setLineWidth(0)
        rate = "н.:" + str(services_list[0].call_cost_night) + "/д.:" + str(services_list[0].call_cost_day) + " руб/мин"
        self.fill_service_data(my_canvas, 550, "1", "Телефония", str(services_list[0].call_duration), "мин.", rate,
                               str(services_list[0].billing))
        my_canvas.line(33, 545, 516, 545)
        rate = str(services_list[1].sms_cost) + "руб/шт"
        self.fill_service_data(my_canvas, 534, "2", "СМС", str(services_list[1].sms_number), "шт.", rate,
                               str(services_list[1].billing))
        my_canvas.line(33, 529, 516, 529)
        rate = str(services_list[2].internet_cost) + "руб/Мб"
        self.fill_service_data(my_canvas, 518, "3", "Интернет",
                               str(float('{:.2f}'.format(services_list[2].traffic_count))), "Мб", rate,
                               str(services_list[2].billing))

        my_canvas.setFont("Arial-Bold", 9)
        total_bill = services_list[0].billing + services_list[1].billing + services_list[2].billing
        # Итог
        my_canvas.drawString(450, 496, str(total_bill))
        # НДС
        my_canvas.drawString(450, 484, str(float('{:.2f}'.format(total_bill*0.2))))
        # Всего к оплате
        my_canvas.drawString(450, 471, str(total_bill))
        # Сумма прописью
        number_str = num2words('{:.2f}'.format(total_bill), lang='ru').format().split('запятая')
        my_canvas.drawString(125, 445.5, '{} руб. {} коп.'.format(number_str[0], number_str[1]))

        # Всего наименований
        my_canvas.setFont("Arial", 9)
        my_canvas.drawString(130, 455.5, '{} на сумму {} руб.'.format(len(services_list), total_bill))

        # Руководитель
        my_canvas.drawString(125, 340, "Бадаев Л.Р.")
        #Бухгалтер
        my_canvas.drawString(400, 340, "Кряжникова В.Ю.")

        my_canvas.save()

        return packet


def main():
    locale.setlocale(locale.LC_ALL, 'Russian_Russia.1251')

    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_dir = "\\".join(current_dir.split("\\")[:-1])
    data = pandas.read_csv(current_dir + '\\lab_1\\data.csv')
    phone_number = 933156729
    xls_file = pandas.ExcelFile(current_dir + '\\lab_2\\dmp.xls')
    dmp_table = xls_file.parse("dmp")
    ip_address = '87.245.198.147'

    telephony = Telephony(data=data, phone_number=phone_number)
    sms = SMS(data=data, phone_number=phone_number)
    internet = Internet(dmp_table, ip_address)

    bill = ServicesBill(services_list=[telephony, sms, internet])

    return


if __name__ == "__main__":
    main()
