import json


def write_order_to_json(item, quantity, price, buyer, date):
    order_dict = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
    with open('orders.json', 'r', encoding='utf-8') as f_n:
        r_data = json.load(f_n)
    with open('orders.json', 'w', encoding='utf-8') as f_n:
        r_data['orders'].append(order_dict)
        json.dump(r_data, f_n, indent=4)
    return


write_order_to_json('iron', 300, 5.4, 'Ivanov', '09.04.2023')
