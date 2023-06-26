from flask import Blueprint, render_template, request, redirect, url_for
from models import PriceList, Order
from exts import db
import os
import csv
import shutil
from datetime import datetime

bp = Blueprint('shopping', __name__, url_prefix='/shopping')


@bp.route('/order', methods=['GET','POST'])
def order():
    #add price list into db

    items=['tea','coffee','cocacola']
    prices=[1,2,3]

    price_list1 = PriceList(item=items[0], price=prices[0])
    price_list2 = PriceList(item=items[1], price=prices[1])
    price_list3 = PriceList(item=items[2], price=prices[2])

    db.session.add_all([price_list1, price_list2, price_list3])
    db.session.commit()

    #from db get price data
    price1 = PriceList.query.filter_by(item=items[0]).order_by(PriceList.id.desc()).first().price
    price2 = PriceList.query.filter_by(item=items[1]).order_by(PriceList.id.desc()).first().price
    price3 = PriceList.query.filter_by(item=items[2]).order_by(PriceList.id.desc()).first().price
    item1 = PriceList.query.filter_by(item=items[0]).first().item
    item2 = PriceList.query.filter_by(item=items[1]).first().item
    item3 = PriceList.query.filter_by(item=items[2]).first().item

    if request.method == 'GET':
        return render_template('order.html',item1=item1, price1=price1,item2=item2,price2=price2,item3=item3,price3=price3)

    else:
        item1 = request.form.get('item1')
        quantity1=int(request.form.get('quantity1'))
        price1=prices[0]
        item2 = request.form.get('item2')
        quantity2=int(request.form.get('quantity2'))
        price2=prices[1]
        item3 = request.form.get('item3')
        quantity3=int(request.form.get('quantity3'))
        price3=prices[2]

        total_price=price1*quantity1+price2*quantity2+price3*quantity3

        c_order = Order(item1=item1,item2=item2,item3=item3,price1=price1,price2=price2,price3=price3,
                        quantity1=quantity1,quantity2=quantity2,quantity3=quantity3,total_price=total_price)
        db.session.add(c_order)
        db.session.commit()

        return redirect(url_for('shopping.pay'))


@bp.route('/pay', methods=['GET','POST'])
def pay():
    if request.method == 'GET':
        pay_order = Order.query.order_by(Order.id.desc()).first()
        order_id = pay_order.id
        item1=pay_order.item1
        item2 = pay_order.item2
        item3 = pay_order.item3
        price1 = pay_order.price1
        price2 = pay_order.price2
        price3 = pay_order.price3
        quantity1 = pay_order.quantity1
        quantity2 = pay_order.quantity2
        quantity3 = pay_order.quantity3
        sub1=price1*quantity1
        sub2=price2*quantity2
        sub3=price3*quantity3
        total = pay_order.total_price

        return render_template('pay.html', item1=item1, item2=item2,item3=item3,price1=price1,price2=price2,price3=price3,
                               quantity1=quantity1,quantity2=quantity2,quantity3=quantity3,total=total,order_id=order_id,
                                sub1=sub1,sub2=sub2,sub3=sub3)
    else:
        return render_template('order.html')

@bp.route('/invoice', methods=['GET','POST'])
def invoice():

    # 处理数据
    pay_order = Order.query.order_by(Order.id.desc()).first()
    order_id = pay_order.id
    item1 = pay_order.item1
    item2 = pay_order.item2
    item3 = pay_order.item3
    price1 = pay_order.price1
    price2 = pay_order.price2
    price3 = pay_order.price3
    quantity1 = pay_order.quantity1
    quantity2 = pay_order.quantity2
    quantity3 = pay_order.quantity3
    sub1 = price1 * quantity1
    sub2 = price2 * quantity2
    sub3 = price3 * quantity3
    total = pay_order.total_price


    invoice_template_folder = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice_template'  # csv1 文件夹的路径
    invoice_folder = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice'  # 新的文件夹路径
    csv1_folder = invoice_template_folder
    csv2_folder = invoice_folder

    if not os.path.exists(csv2_folder):
        os.makedirs(csv2_folder)

    invoice_template_path = f'{csv1_folder}/invoice_template.csv'  # csv1 文件的路径
    csv1_path = invoice_template_path

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    invoice_path = f'{csv2_folder}/{order_id}_csv{timestamp}.csv'
    invoice_file = f'{order_id}_csv{timestamp}.csv'
    csv2_path = invoice_path

    shutil.copyfile(csv1_path, csv2_path) # 复制 csv1 文件到新的文件夹作为 csv2


    with open(csv2_path, 'r', newline='') as file:
        reader = csv.reader(file)
        data1 = list(reader)
        data1 = data1[0]


    data = []
    data.append(data1)
    if quantity1 != 0:
        data.append([order_id,item1,price1,quantity1,sub1])
    if quantity2 != 0:
        data.append([order_id,item2,price2,quantity2,sub2])
    if quantity3 != 0:
        data.append([order_id,item3,price3,quantity3,sub3])
    data[1].append(total)

    # 4. 将数据填充到生成的 CSV 文件中


    with open(csv2_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for i, row in enumerate(data):
            writer.writerow(row)

    invoice_file = url_for('static', filename='csv/invoice/' + invoice_file)




    return render_template('invoice_csv.html' ,invoice_file=invoice_file)

@bp.route('/overwrite_invoice', methods=['GET','POST'])
def overwrite_invoice():

    if request.method == "POST":
        order_id = request.form.get('order_id')
        new_quantity = str(request.form.get('new_quantity'))
        # 使用 try-except 验证输入数据类型是否为int
        try:
            new_quantity = int(new_quantity)
            # 在这里处理验证通过的数据
            # new_quantity 确保是一个整数
        except ValueError:
            return 'Invalid input. Quantity must be an integer.'

        item = request.form.get('item').lower()
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
                    length=len(original_data)

                    for i in range (1, length):
                        if original_data[i][1] == item:
                            original_quantity = int(original_data[i][3])
                            original_data[i][3] = int(new_quantity)
                            quantity_gap = original_data[i][3] - original_quantity

                            original_data[i][4] = int(new_quantity)*float(original_data[i][2])
                            original_data[1][5] = float(original_data[1][5])+float(original_data[i][2])*quantity_gap
                            break
                        # elif original_data[2][1] == item:
                        #     original_data[2][3] = int(new_quantity)
                        #     original_data[2][4] = int(new_quantity)*float(original_data[2][2])
                        #     original_data[1][5] = float(original_data[1][4]) + float(original_data[2][4]) + float(original_data[3][4])
                        #
                        # elif original_data[3][1] == item:
                        #     original_data[3][3] = int(new_quantity)
                        #     original_data[3][4] = int(new_quantity)*float(original_data[3][2])
                        #     original_data[1][5] = float(original_data[1][4]) + float(original_data[2][4]) + float(original_data[3][4])

                    else:
                        return 'These is such item in the order.'

                new_data = original_data
                with open(invoice_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(new_data)
                # return 'Invoice has been overwrited.'

                return render_template('send_email.html')
                break
        else:
            return 'Invoice does not exit! Check Order ID again.'
    else:
        folder_path = 'D:/Python_project/newdemo/demo1/project1/static/csv/invoice'
        file_id_list = []
        for filename in os.listdir(folder_path):
            file_id = filename.split('_')[0]

            file_id_list.append(file_id)
        item_list = ['tea','coffee','cocacola']
        print(file_id_list)
        return render_template('overwrite_invoice.html', file_id_list=file_id_list, item_list=item_list)