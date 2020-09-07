from PIL import Image
import sys
import binascii

def bgrcon(dir):
    f=open(dir,'rb')
    f.seek(10)
    가로=f.read(2)
    세로=f.read(2)
    가로변환1=binascii.hexlify(가로)
    가로변환2=가로변환1.decode('ascii')
    가로값=int(가로변환2, base=16)
    print(가로값)
    세로변환1=binascii.hexlify(세로)
    세로변환2=세로변환1.decode('ascii')
    세로값=int(세로변환2, base=16)
    print(세로값)
    f.seek(32)
    rawData = b''
    while True : 
        사진y1=f.read(1)
        사진v=f.read(1)
        사진y2=f.read(1)
        사진u=f.read(1)
        if 사진y1 == b'' :
            print('끗')
            break
        else :
            y1변환=int(binascii.hexlify(사진y1).decode('ascii'), base=16)
            v변환=int(binascii.hexlify(사진v).decode('ascii'), base=16)
            y2변환=int(binascii.hexlify(사진y2).decode('ascii'), base=16)
            u변환=int(binascii.hexlify(사진u).decode('ascii'), base=16)
            b1값=round(65536*(1.164*(y1변환-16)+2.018*(u변환-128))/65536)
            g1값=round(65536*(1.164*(y1변환-16)-0.813*(v변환-128)-0.391*(u변환-128))/65536)
            r1값=round(65536*(1.164*(y1변환-16)+1.596*(v변환-128))/65536)
            b2값=round((76284*(y2변환-16)+132252*(u변환-128))>>16)
            g2값=round((76284*(y2변환-16)-53281*(v변환-128)-25625*(u변환-128))>>16)
            r2값=round((76284*(y2변환-16)+104595*(v변환-128))>>16)  
            #print('r1값은'+str(r1값)+'g1값은'+str(g1값)+'r1값은'+str(r1값))
            if r1값 < 0 :
                r1값 = 0
            if g1값 < 0 :
                g1값 = 0
            if b1값 < 0 :
                b1값 = 0
            if r2값 < 0 :
                r2값 = 0
            if g2값 < 0 :
                g2값 = 0
            if b2값 < 0 :
                b2값 = 0                
            r1바이트=r1값.to_bytes(1,byteorder='big')
            g1바이트=g1값.to_bytes(1,byteorder='big')
            b1바이트=b1값.to_bytes(1,byteorder='big')
            r2바이트=r2값.to_bytes(1,byteorder='big')
            g2바이트=g2값.to_bytes(1,byteorder='big')
            b2바이트=b2값.to_bytes(1,byteorder='big')
            rawData = rawData + r1바이트 + g1바이트 + b1바이트 + r2바이트 + g2바이트 + b2바이트
    imgSize = 가로값, 세로값
    img = Image.frombytes('RGB',imgSize,rawData,decoder_name='raw')
    img.save(sys.argv[1]+'.png')    
bgrcon(sys.argv[1])