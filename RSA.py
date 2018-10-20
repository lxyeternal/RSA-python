#-*- coding：UTF-8 -*-


''' sichuan university

    author: guowenbo


    time:  2018-5-30


    content:RSA

    python 3.6

    mac os

'''

from random import randint
import random
import math
import sys


def  charToAscii(message):       #将字符转化为ASCII码
  Output = []
  for i in message:
      Output.append(ord(i))
  return Output

                                  #将ASCII码变为十六进制
def AsciiToHex(message):
  Output = ''
  for each in message:
    Output = Output + str(hex(each)).split('x')[1]
  return Output


def Hex_to_dec(hexnumber):        #16进制字符串转化为十进制
    decnumber = int(hexnumber,16)
    return decnumber



def dec_to_Hex(decumber):          #十进制转化为十六进制
    hexnumber = hex(decumber)
    return hexnumber



def big_P_Q():                  #产生两个大素数
    flag = 0
    while not flag:
        p = random.randrange(10**10,10**11)

        if charge_sushu_1(p) and _ack(2,p):

            q = random.randrange(p,10**11)
            if charge_sushu_1(q) and p != q and _ack(2,q):
                flag = 1
    return p,q







def fastExpMod(b, e, m):          #快速求模
    result = 1
    while e != 0:
        if (e&1) == 1:
            # ei = 1, then mul
            result = (result * b) % m
        e >>= 1
        # b, b^2, b^4, b^8, ... , b^(2^n)
        b = (b*b) % m
    return result

def gcd(a,b):                     #判断互素
    if a<b:
        a,b = b,a
    while b != 0:
        temp = a%b
        a = b
        b = temp
    return (a,b)


def find_e(En):                     #寻找e
    while 1:
        e = random.randrange(10000)
        if gcd(e,En) == (1,0):
            break

    return e

def find_d(e,s):                    #求d

    u1, u2, u3 = 1, 0, e
    v1, v2, v3 = 0, 1, s
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % s

# def miller_Rabin(n):                #素性检验
#     if n == 1:
#         return False
#     if n == 2:
#         return True
#     N = n-1
#     a = randint(2, N)
#     t = int(math.floor(math.log(N,2)))
#     u = 1
#     while t>0:
#         u = N/2**t
#         if N%2*t==0 and u%2 == 1:
#             break
#         u = t-1
#     b = fastExpMod(a,u,n)
#     if(b == 1):
#         return True
#
#     for n in range(0,t,1):
#         if(b == n-1):
#             return True
#         else:
#             b = fastExpMod(b,2,n)
#     return False

def charge_sushu_1(n):
    Sushu = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41
                 , 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
    for y in Sushu:
        if n % y == 0:
            return False
    return True

def _ack(a,n):

    a1 = pow(17-a,n,n)
    a2 = pow(17,n,n) - (a%n)
    if a1 == a2:
        return 1
    else:
        return 0

def charge_sushu_2(n, k):
    if n < 2:
           return False
    d = n - 1
    r = 0
    while not (d & 1):
            r += 1
            d >>= 1
    for i in range(k):
            a = randint(120)        #随机数
            x = fastExpMod(a, d, n)
            if x == 1 or x == n - 1:
                    continue
            for i in range(r - 1):
                    x = fastExpMod(x, 2, n)
            if x == 1:
                    return False
            if x == n - 1:
                    break
    else:
            return False
    return True




def main():

    while True:

        choose = input()
        if choose == '1':
            print("-------测试数据加密--------\n")
            with open('rsa_plain.txt', 'r') as f:        #读取明文                            #测试数据
                plaindata = f.read().strip('\n')
                print("读入的明文为：",plaindata)
                f.close()
            dec_plain = Hex_to_dec(plaindata)
            print("明文十进制为：:",dec_plain)


            with open('rsa_pubkey.txt', 'r') as f:
                 pubkey_n = f.readline().strip('\n')
                 pubkey_e = f.readline().strip('\n')
                 print("n为：", pubkey_n)
                 print("e为：", pubkey_e)
                 f.close()
            dec_e = Hex_to_dec(pubkey_e)
            print("e十进制为：",dec_e)
            dec_n = Hex_to_dec(pubkey_n)
            print("n十进制为：",dec_n)

            dec_cipher = fastExpMod(dec_plain,dec_e,dec_n)

            print("dec_cipher",dec_cipher)
            cipher = dec_to_Hex(dec_cipher)
            str_cipher = str(cipher).upper()
            with open('rsa_cipher.txt', 'w') as f:        #写入密文
                f.write(str_cipher[2:])
                f.close()
            print("密文为：",str_cipher[2:])




        if choose == '2':

            print("---------测试数据解密---------\n")
                                                   #测试数据
            with open('rsa_cipher.txt', 'r') as f:        #读取密文
                cipher = f.read().strip('\n')
                f.close()
            print("待解密的密文：", cipher)
            dec_cipher = Hex_to_dec(cipher)
            with open('rsa_pubkey.txt', 'r') as f:
                 pubkey_n = f.readline().strip('\n')
                 print("n为：", pubkey_n)
                 f.close()
            dec_n = Hex_to_dec(pubkey_n)
            print("n十进制为：",dec_n)
            with open('rsa_prikey.txt','r') as f:
                d = f.read().strip('\n')
                print("d为：",d)
            dec_d = Hex_to_dec(d)
            dec_plain = fastExpMod(dec_cipher,dec_d,dec_n)
            print("明文十进制为：",dec_cipher)
            plain = dec_to_Hex(dec_plain)
            str_plain = str(plain)
            with open('rsa_plain.txt', 'w') as f:  # 解密后的放入文件
                f.write(str_plain[2:])
                f.close()
            print("明文为：", str_plain[2:])
            print("解密完成，请查看rsa_plain.txt文件")


        if choose == '3':

            print("----------学号姓名加密-----------\n")
            print("加密前请保证文件内容为学号姓名\n")
            with open('rsa_plain_SN.txt', 'r') as f:        #读取明文                            #学号姓名
                plaindata = f.read().strip('\n')
                print("读入的明文为：",plaindata)
                f.close()

            print("明文十六进制为：",AsciiToHex(charToAscii(plaindata)))
            dec_plain = Hex_to_dec(AsciiToHex(charToAscii(plaindata)))

            print("明文十进制为：:",dec_plain)
            p = big_P_Q()[0]
            str_p = str(dec_to_Hex(p))
            q = big_P_Q()[1]
            str_q = str(dec_to_Hex(q))

            with open('p.txt','w') as f:
                f.write(str_p[2:])
                f.close()
            with open('q.txt','w') as f:
                f.write(str_q[2:])
                f.close()
            print("生成的素数p为：",p)
            print("生成的素数q为：",q)

            N = p*q
            str_N = str(dec_to_Hex(N))
            with open('n.txt','w') as f:
                f.write(str_N[2:])
                f.close()
            print("生成的N为：",N)
            En = (p-1)*(q-1)
            e = find_e(En)
            str_e = str(dec_to_Hex(e))
            with open('e.txt','w') as f:
                f.write(str_e[2:])
                f.close()
            print("e为：",e)
            d = int(find_d(e,En))
            str_d = str(dec_to_Hex(d))
            with open('d.txt','w') as f:
                f.write(str_d[2:])
                f.close()
            print("十进制d为：",d)
            print("十六进制d为",str_d[2:])

            f_cipher = []
            len_plain = len(plaindata)
            for i in range(0,len_plain,8):                          #明文分组
                # print(plaindata[i:i+8])
                cut_plain = Hex_to_dec(AsciiToHex(charToAscii(plaindata[i:i+8])))
                # print("明文分组：",cut_plain)
                cipher = fastExpMod(cut_plain,e,N)
                str_cipher_cut = str(dec_to_Hex(cipher))
                # print(str_cipher_cut)
                f_cipher.append(str_cipher_cut)
            str_cipher = ''.join(f_cipher)
            with open('rsa_cipher_SN.txt', 'w') as f:        #写入密文
                f.write(str_cipher)
                f.close()
            print("密文为：",str_cipher)
            print("加密成功！")
            print("请查看rsa_cipher_SN.txt文件")



        if choose == '4':

            print("----------学号姓名解密-----------\n")

            with open('rsa_cipher_SN.txt', 'r') as f:       # 读取密文
                cipher = f.read().strip('\n')
                f.close()
            print("待解密的密文：", cipher)
            # dec_cipher = Hex_to_dec(cipher)


            with open('d.txt','r') as f:                    #读取d
                str_d = f.read().strip('\n')
                f.close()
            print("私钥d为：",str_d)
            dec_d = Hex_to_dec(str_d)
            print("十进制d为：",dec_d)


            with open('n.txt','r') as f:                            #读取N
                str_N = f.read().strip('\n')
                f.close()
            N = Hex_to_dec(str_N)
            f_plain = cipher.split('0x')
            f_cut_plain = []
            for i in range(1,4):
                # print(f_plain[i])
                dec_cipher = Hex_to_dec(f_plain[i])
                cut_plain = fastExpMod(dec_cipher, dec_d, N)        #进行解密
                # print(cut_plain)
                str_plain_cut = str(dec_to_Hex(cut_plain))[2:]
                f_cut_plain.append(str_plain_cut)
            plain = ''.join(f_cut_plain)
            str_plain = str(plain)
            a1 = []                                                    # 写入明文
            for i in range(0, len(str_plain), 2):
                b = str_plain[i:i + 2]
                a1.append(chr(int(b, 16)))
            str_plain_char = ''.join(a1)


            with open('rsa_plain_SN.txt','w') as f:
                f.write(str_plain_char)
                f.close()
            print("解密的明文为：",str_plain_char)
            print("解密成功！")



        elif choose == '0':
            print("退出")
            exit()




if  __name__ == '__main__':
    print("*--------------------------------------------------------------------------*\n")
    print("                              请选择要进行的操作\n")
    print("加密（测试数据）：1  解密（测试数据）：2  加密（学号）：3   解密（学号）：4    退出：0\n")
    print("*--------------------------------------------------------------------------*\n")
    main()







