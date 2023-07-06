from flask import Blueprint, render_template, request, redirect, url_for
from models import PriceList, Order
from exts import db
import os
import csv
import shutil
from datetime import datetime
import pandas

bp = Blueprint('shopping', __name__, url_prefix='/shopping')


@bp.route('/active_work_order')
def active_work_order():

    work_order = Order.query.order_by(Order.id.desc()).limit(10).all()
    return render_template('active_work_order.html', work_order=work_order)

@bp.route('/order', methods=['GET', 'POST'])
def order():

    # work_order = Order.query.order_by(Order.id.desc()).limit(5).all()
    laser_scanner_list = ['RulerX 10', 'RulerX 20', 'RulerX 70', 'RulerXC 10', 'RulerXC 20', 'RulerXC 70', ]
    prepared_by_list = ['John', 'Ben', 'Linda']
    approved_by_list = ['John1', 'Ben1', 'Linda1']

    if request.method == 'GET':
        return render_template('order.html', laser_scanner_list=laser_scanner_list,
                               prepared_by_list=prepared_by_list, approved_by_list=approved_by_list)

    else:
        sale_order_id = request.form.get('sale_order_id')
        part_number_id = request.form.get('part_number_id')
        part_id = request.form.get('part_id')
        item1 = request.form.get('item1')
        laser_scanner1 = request.form.get('scanner1')
        prepared_by = request.form.get('prepared_by')
        approved_by = request.form.get('approved_by')
        status1 = 'sentencing'
        date_time = datetime.now()
        sentencing_time1 = date_time.strftime("%Y-%m-%d %H:%M:%S")

        w_order = Order(sale_order_id=sale_order_id, part_number_id=part_number_id, part_id=part_id, item1=item1,
                        status1=status1, sentencing_time1=sentencing_time1, laser_scanner1=laser_scanner1,
                        prepared_by=prepared_by, approved_by=approved_by)
        db.session.add(w_order)
        db.session.commit()

        return redirect(url_for('shopping.pay'))


@bp.route('/pay', methods=['GET', 'POST'])
def pay():
    work_order = Order.query.order_by(Order.id.desc()).first()
    order_id = work_order.id
    item1 = work_order.item1
    status1 = work_order.status1
    part_id = work_order.part_id

    sentencing_time1 = work_order.sentencing_time1

    laser_scanner1 = work_order.laser_scanner1
    if request.method == 'GET':
        return render_template('pay.html', order_id=order_id, part_id=part_id, item1=item1, status1=status1,
                               sentencing_time1=sentencing_time1, laser_scanner1=laser_scanner1)
    else:
        date_time = datetime.now()
        verify_time1 = date_time.strftime("%Y-%m-%d %H:%M:%S")
        work_order.verify_time1 = verify_time1
        work_order.status1 = 'verified'
        db.session.commit()

        return redirect(url_for("shopping.invoice"))


@bp.route('/invoice', methods=['GET', 'POST'])
def invoice():
    # 处理数据
    work_order = Order.query.order_by(Order.id.desc()).first()
    order_id = work_order.id
    sale_order_id = work_order.sale_order_id
    part_number_id = work_order.part_number_id
    part_id = work_order.part_id
    item1 = work_order.item1
    prepared_by = work_order.prepared_by
    approved_by = work_order.approved_by
    status1 = work_order.status1
    sentencing_time1 = work_order.sentencing_time1
    laser_scanner1 = work_order.laser_scanner1
    verify_time1 = work_order.verify_time1

    if request.method == 'GET':
        factor = 1
        return render_template('invoice_csv.html', order_id=order_id, part_id=part_id, item1=item1, status1=status1,
                               sentencing_time1=sentencing_time1, verify_time1=verify_time1,
                               laser_scanner1=laser_scanner1, factor=factor)
    else:
        factor = 2
        date_time = datetime.now()
        final_time1 = date_time.strftime("%Y-%m-%d %H:%M:%S")
        work_order.final_time1 = final_time1
        work_order.status1 = 'final_inspection'
        db.session.commit()

        # to generate csv file
        invoice_template_folder = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice_template'  # csv1 文件夹的路径
        invoice_folder = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice'  # 新的文件夹路径
        csv1_folder = invoice_template_folder
        csv2_folder = invoice_folder

        if not os.path.exists(csv2_folder):
            os.makedirs(csv2_folder)

        invoice_template_path = f'{csv1_folder}/work_order_template.csv'  # csv1 文件的路径
        csv1_path = invoice_template_path

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        invoice_path = f'{csv2_folder}/{order_id}_csv{timestamp}.csv'
        invoice_file = f'{order_id}_csv{timestamp}.csv'
        csv2_path = invoice_path

        shutil.copyfile(csv1_path, csv2_path)  # 复制 csv1 文件到新的文件夹作为 csv2

        with open(csv2_path, 'r', newline='') as file:
            reader = csv.reader(file)
            data1 = list(reader)
            data1 = data1[0]

        data = []
        data.append(data1)
        data.append(
            [order_id, sale_order_id, part_number_id, part_id, item1, prepared_by, approved_by, status1, laser_scanner1,
             sentencing_time1, verify_time1, final_time1])
        # if quantity1 != 0:
        #     data.append([order_id, item1, price1, quantity1, sub1])
        # if quantity2 != 0:
        #     data.append([order_id, item2, price2, quantity2, sub2])
        # if quantity3 != 0:
        #     data.append([order_id, item3, price3, quantity3, sub3])
        # data[1].append(total)

        # 4. 将数据填充到生成的 CSV 文件中

        with open(csv2_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for i, row in enumerate(data):
                writer.writerow(row)

        invoice_file = url_for('static', filename='csv/invoice/' + invoice_file)

        return render_template('invoice_csv.html', invoice_file=invoice_file, factor=factor)



@bp.route('/overwrite_invoice', methods=['GET', 'POST'])
def overwrite_invoice():
    laser_scanner_list = ['RulerX 10', 'RulerX 20', 'RulerX 70', 'RulerXC 10', 'RulerXC 20', 'RulerXC 70', ]
    if request.method == "POST":
        order_id = request.form.get('order_id')
        new_scanner = str(request.form.get('new_scanner'))
        # # 使用 try-except 验证输入数据类型是否为int
        # try:
        #     new_quantity = int(new_quantity)
        #     # 在这里处理验证通过的数据
        #     # new_quantity 确保是一个整数
        # except ValueError:
        #     error_message = 'Invalid input. Quantity must be an integer.'
        #     return render_template('overwrite_invoice.html', error_message=error_message)

        # item = request.form.get('item')
        folder_path = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice'

        for filename in os.listdir(folder_path):
            file_id = filename.split('_')[0]
            if file_id == order_id:
                invoice_path = f'{folder_path}/{filename}'
                print('i am here')
                print(filename)
                with open(invoice_path, 'r', newline='') as file:
                    reader = csv.reader(file)
                    original_data = list(reader)
                    original_data[1][3] = new_scanner

                    # length = len(original_data)

                    # for i in range(1, length):
                    #     if original_data[i][1] == item:
                    #         original_quantity = int(original_data[i][3])
                    #         original_data[i][3] = int(new_quantity)
                    #         quantity_gap = original_data[i][3] - original_quantity
                    #
                    #         original_data[i][4] = int(new_quantity) * float(original_data[i][2])
                    #         original_data[1][5] = float(original_data[1][5]) + float(original_data[i][2]) * quantity_gap
                    #         break
                    # elif original_data[2][1] == item:
                    #     original_data[2][3] = int(new_quantity)
                    #     original_data[2][4] = int(new_quantity)*float(original_data[2][2])
                    #     original_data[1][5] = float(original_data[1][4]) + float(original_data[2][4]) + float(original_data[3][4])
                    #
                    # elif original_data[3][1] == item:
                    #     original_data[3][3] = int(new_quantity)
                    #     original_data[3][4] = int(new_quantity)*float(original_data[3][2])
                    #     original_data[1][5] = float(original_data[1][4]) + float(original_data[2][4]) + float(original_data[3][4])

                    # else:
                    #     error_message = 'Select a scanner please!'
                    #     file_id_list = get_file_id_list()
                    #
                    #     return render_template('overwrite_invoice.html', file_id_list=file_id_list,
                    #                            error_message=error_message)

                    new_data = original_data
                with open(invoice_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(new_data)
                # return 'Invoice has been overwrited.'

                return render_template('send_email.html')
                break
        else:
            error_message = 'Select a order ID please!'
            file_id_list = get_file_id_list()

            return render_template('overwrite_invoice.html', file_id_list=file_id_list,
                                   laser_scanner_list=laser_scanner_list,
                                   error_message=error_message)

    else:

        file_id_list = get_file_id_list()
        return render_template('overwrite_invoice.html', file_id_list=file_id_list,
                               laser_scanner_list=laser_scanner_list)


def get_file_id_list():
    folder_path = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice'
    file_id_list = []

    for filename in os.listdir(folder_path):
        file_id = filename.split('_')[0]
        file_id_list.append(file_id)
    return file_id_list
