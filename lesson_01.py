import subprocess

# Задание №1

word1, word2, word3 = 'разработка', 'сокет', 'декоратор'
print(f'Задание №1')
print(type(word1), word1)
print(type(word2), word2)
print(type(word3), word3, '\n')

b_word1 = b'\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
b_word2 = b'\u0441\u043e\u043a\u0435\u0442'
b_word3 = b'\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
print(type(b_word1), b_word1)
print(type(b_word2), b_word2)
print(type(b_word3), b_word3, '\n')

# Задание №2

a = b'class'
b = b'function'
c = b'method'
print(f'Задание №2')
print(f'{type(a)}, {a}, длина = {len(a)}')
print(f'{type(b)}, {b}, длина = {len(b)}')
print(f'{type(c)}, {c}, длина = {len(c)}', '\n')

# Задание №3

d = b'attribute'
# e = b'класс' - невозможно записать в байтовом виде, т.к. написаны кириллицей
# f = b'функция' - невозможно записать в байтовом виде, т.к. написаны кириллицей
g = b'type'
print(f'Задание №3')
print(f'{type(d)}, {d}')
# print(f'{type(e)}, {e}')
# print(f'{type(f)}, {f}')
print(f'{type(g)}, {g}', '\n')

# Задание №4

word4 = 'разработка'
word5 = 'администрирование'
word6 = 'protocol'
word7 = 'standard'

enc_word4 = word4.encode('utf-8')
enc_word5 = word5.encode('utf-8')
enc_word6 = word6.encode('utf-8')
enc_word7 = word7.encode('utf-8')

dec_word4 = enc_word4.decode('utf-8')
dec_word5 = enc_word5.decode('utf-8')
dec_word6 = enc_word6.decode('utf-8')
dec_word7 = enc_word7.decode('utf-8')

print(f'Задание №4')
print(enc_word4, dec_word4)
print(enc_word5, dec_word5)
print(enc_word6, dec_word6)
print(enc_word7, dec_word7, '\n')

# Задание №5

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']
print(f'Задание №5')

for _comm in [args1, args2]:
    subproc_ping = subprocess.Popen(_comm, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        # line = line.decode('cp1251')
        # f2.write(f'{line}')
        # print(f2)
        line = line.decode('cp866').encode('utf-8')
        print(line.decode('utf-8'))

# Задание №6

f1 = open('test_file.txt', 'w')
f1.write('сетевое программирование, сокет, декоратор')
f1.close()
print(f'Задание №6')
print(f1, '\n')
f1.close()

with open('test_file.txt', encoding='utf-8') as f2:
    for txt_str in f2:
        print(txt_str, end=' ')
f2.close()
