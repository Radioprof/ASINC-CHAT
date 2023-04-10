import yaml

data = {'first': ['red', 'blue', 'white'], 'second': 253, 'third': {'iron': '300Ω', 'glass': '26Ω', 'wood': '160Ω'}}

with open('file.yaml', 'w', encoding='utf-8') as f_n:
    yaml.dump(data, f_n, default_flow_style=False, allow_unicode=True)

with open('file.yaml', encoding='utf-8') as f_n:
    read_data = yaml.load(f_n, Loader=yaml.SafeLoader)
    print(read_data == data)
