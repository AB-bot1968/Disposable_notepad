#====================================================================
# За осноу примера взят Шифр Вернама
# Шифр является разновидностью криптосистемы одноразовых блокнотов.
# В нём используется булева функция «исключающее или».
#====================================================================
# Новизна предлагаемого решения касается способа генерации одноразовых
# блокнотов, для чего используются координаты траектории аттрактора
# Лоренца на значительном удалении от его начальной точки.
#====================================================================
# Одноразовый блокнот формируется динамически для чего используется
# уникальное значение начала координат и количество шагов (точек
# траектории). Ниже представлен принцип работы предложенного алгоритма.
# При разработке штатного алгоритма выбор координат для формирования
# шифроблокнота может быть произвольно усложнен например использованием
# нескольких траекторий. Ниже пример трех траекторий.
#====================================================================
import numpy as np
import os
import math
from itertools import cycle
from hashlib import sha512
from scipy.integrate import odeint
import argparse
#====================================================================
# Получение параметров командной строки
#====================================================================
def param():
    parser = argparse.ArgumentParser(
    prog='L240.py',
    description='Шифр Вернама. Новизна предлагаемого решения касается ' \
                'способа генерации одноразовых блокнотов, для чего ' \
                'используются координаты траектории аттрактора Лоренца ' \
                'на значительном удалении от его начальной точки.',
    epilog='(c) Автор: Ботнев А.В. <abotnev00@gmail.com> 08.12.2016 г.'
    )

    parser.add_argument('-f','--fname', nargs='?', default='text0.txt')
    args = parser.parse_args()
    return args.fname

#====================================================================
# Коэффициенты уравнений Лореца для получения класического аттрактора
#====================================================================
s,r,b=10,28,8/3
#====================================================================
# Количество точек траектории до начала координат используемых
# в качестве одноразового блокнота
#====================================================================
coutn_iter = 5001
#====================================================================
# Шифрование (дешифрование) a xor b Шифр Вернама
#====================================================================
def encrypt1(var, key):
    return  [a ^ ord(b) for (a,b) in zip(var, key)]
#====================================================================
# Система ОДУ Лоренца для вычистения аттрактора
#====================================================================
def f(y, t):
   # x   y   z
    y1, y2, y3 = y
    return [s*(y2-y1), -y2+(r-y3)*y1, -b*y3+y1*y2]
#====================================================================
# Решаем систему ОДУ вычисляем ее фазовую траекторию
# Начальное значение например
# x =  1.0000000000000001,
# y = -1.0000000000000001,
# z = 10.0000000000000001
# Количество шагов для получения достаточного разброса точек
# n=5001
# a0 = [x, y, z] решение ОДУ (координаты траектории на их основе
# динамически создается одноразовый блокнот)
#====================================================================
def lorenz(x,y,z,n):
    t = np.linspace(0,50,n)
    y0 = [x, y, z]
    a0 = odeint(f, y0, t, full_output=False).T
    return a0
#====================================================================
#         Получаем очередную строку шифроблокнота 128 байт
#====================================================================
def m_read(a0,a1,a2,nzap):
    if len(a0[0]) >= nzap:
        line0 = str(a0[0][nzap]) + str(a0[1][nzap]) + str(a0[2][nzap]) +'\n'
        line1 = sha512(line0.encode()).hexdigest()
        #print(line0.strip())
        line2 = str(a1[0][nzap]) + str(a1[1][nzap]) + str(a1[2][nzap]) + line1 +'\n'
        line3 = sha512(line2.encode()).hexdigest()
        #print(line2.strip())
        line4 = line3 + str(a2[0][nzap]) + str(a2[1][nzap]) + str(a2[2][nzap]) +'\n'
        line5 = sha512(line4.encode()).hexdigest()
        #print(line4.strip())
        #print(line5)
        return line5
    return [1]
#====================================================================
# Вычисляем размер одноразового блокнота, где 128 - длина в байтах
# хеша вычисленного по алгоритму sha512. Основой для вычисления хеша
# являются координата траектории аттрактора. При этом, размер файла
# в байтах до шифрования и после равны.
### print(sha256(bytes([1, 2, 3])).hexdigest())
### print(sha512(bytes([1, 2, 3])).hexdigest())
#====================================================================
def file_crypt(fpath):
    siz = os.path.getsize(fpath) # размер файла в байтах.
    key = math.ceil(siz/128)     # количество точек используемых для
    return key                   # получения шифроблокнота
                                 # (округление в большую сторону)
#====================================================================
#                 Шифрование главная процедура
#====================================================================
def crypt(f1,f2):
    file1 = open(f1,'rb')
    file2 = open(f2, 'ab')

    for i in range(keylen):
        text1     = file1.read(128)
        key1      = m_read(a0=zap0,a1=zap1,a2=zap2,nzap=coutn_iter+i)
        encrypted = encrypt1(text1, key1)
        barray    = bytearray(encrypted)
        file2.write(barray)

    file2.close()
    file1.close()
#====================================================================
#        Проверка существования и удаление тестовых файлов
#====================================================================
def fexists(f):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f)
    if os.path.exists(path):
        os.remove(path)
#====================================================================
#             Удаляем тестовые файлы если они есть
#====================================================================
fexists(f='encrypted.txt')
fexists(f='decrypted.txt')
#====================================================================
#              Получение параметров командной строки
#====================================================================
fname = param()
#====================================================================
#    Вычисляем длину одноразового блокнота для шифруемого файла
#====================================================================
keylen = file_crypt(fpath=fname) #'text0.txt')
#====================================================================
# Вычисляем траекторию (с учетом длины одноразового блокнота)
#====================================================================
zap0 =lorenz(x =  1.0012400000000001, \
             y = -1.0000000010000001, \
             z = 10.0000000000000101, \
             n = coutn_iter+keylen)
#====================================================================
zap1 =lorenz(x =  1.0012400001000001, \
             y = -1.0000000020000001, \
             z = 10.0000000300000101, \
             n = coutn_iter+keylen)
#====================================================================
zap2 =lorenz(x =  1.0012400004000001, \
             y = -1.0000000050000001, \
             z = 10.0000000600000101, \
             n = coutn_iter+keylen)
#====================================================================
#                 Шифрование одноразовым блокнотом
#====================================================================
crypt(f1 = fname,    f2 = 'encrypted.txt')
#====================================================================
#               Расшифровывание одноразовым блокнотом
#====================================================================
crypt(f1 = 'encrypted.txt',f2 = 'decrypted.txt')
#====================================================================
# Помним
# coutn_iter = 5001

# x =  1.0012400000000001
# y = -1.0000000010000001
# z = 10.0000000000000101

# x =  1.0012400001000001
# y = -1.0000000020000001
# z = 10.0000000300000101

# x =  1.0012400004000001
# y = -1.0000000050000001
# z = 10.0000000600000101

# и файл зашифрованный этим шифроблокнотом (encrypted.txt)
#====================================================================
