# encoding=utf-8
# author EvilsoulM
# rewrite by evasnowind at 2018.1.23

import commands
import os
import struct
import sys, getopt
import shutil

input_path = ""
quality = "80"

output_path = ""
compress_size = ""
max_img_size = 100
set_max_size_flag = False

show_process = False

'''
    -s X 大小超过X kb的图片才进行压缩
    -m X 压缩后的图片不能超过X kb
    -i X 输入文件夹路径
    -o X 输出文件夹路径，如果不写，默认为输入文件夹下新建一个webp文件夹
    -q X 设置百分比进行压缩，0-100，100质量最高，默认80
    --process 不用带参数，开关变量，设置后将显示webp压缩图片过程（google cwebp命令的输出）

用于限定webp格式图片最多可以多少KB，用于动态限定图片压缩大小。
因为实际工作中经常遇到要求图片不能超过多少KB的情况，那么此时压缩配置项
中应该配置：
    -i inputpath -o outputpath -s X -m Y   
    小于X KB的文件不用压缩
    图片最大达到Y左右
    
    而google提供的压缩工具包只能设置压缩比例。因此对于上述情况，
    需要不断循环尝试，从比较大的quality开始，看结果是否满足要求，
    如此不断重复尝试，设置一个步长来逐次逼近。
    
    如果图片过大、不能达到要求，那么就用quality = 1的比例进行压缩。
    
    
    add by evasnowind 2018.1.23
'''

def getInputArguments():

    opts, args = getopt.getopt(sys.argv[1:], "hi:o:q:s:m:",["process"])
    global quality
    global output_path
    global compress_size
    global input_path
    global show_process
    global max_img_size
    global set_max_size_flag

    print "Compress Config:"
    for op, value in opts:
        print("op:" + op + " "),
        if op == "-i":
            input_path = value
            print("input path = " + input_path)
        elif op == "-o":
            output_path = value
            print("output path = " + output_path)
        elif op == "-h":
            print("help")
        elif op == "-q":
            quality = value
            print("image quality[0-poor, 100-very good, deault=75] = " + quality)
        elif op == "-s":
            compress_size = value
            print("images which are bigger than " + compress_size + " KB will be compressed.")
        elif op == "--process":
            show_process = True
            print("show cwebp compress process.")
        elif op == "-m":
            max_img_size = int(value)
            set_max_size_flag = True
            print("max output webp size = "+value)
    print ""


def transFiles():

    files = os.listdir(input_path)
    for f in files:

        img_file_path = input_path + f
        if os.path.isfile(img_file_path):
            file_type = filetype(img_file_path)
            if file_type == "JPEG" or file_type == "PNG": #JPEG和JPG的魔数是一样的，不必单独做区分
                splitext_arr = os.path.splitext(f)
                img_output_path = output_path + splitext_arr[0] + ".webp"
                transToWebp(img_file_path, img_output_path)

def transToSpecifiedSizeWebp(input_file_path, output_file_path, max_webp_size):
    trans_quality = quality
    while True:
        transToWebpByQuality(input_file_path, output_file_path, trans_quality)
        trans_file_size = os.path.getsize(output_file_path) / 1024.0
        if trans_file_size > max_webp_size:

            trans_quality_int = int(trans_quality) - 5;
            if trans_quality_int <= 0:
                break;
            trans_quality = "" + str(trans_quality_int)
            print("current size = " + str(trans_file_size) + ", target size="+str(max_webp_size) +", try again!")
        else:
            break;



def transToWebpByQuality(input_file_path, output_file_path, img_quality):
    if os.path.exists(output_file_path):
        os.remove(output_file_path)

    command = "cwebp -q " + img_quality + " " + input_file_path + " -o " + output_file_path
    print("压缩 " + input_file_path + "，执行命令:" + command)
    if (show_process):
        os.system(command)
    else:
        commands.getstatusoutput(command)


def transToWebp(input_file_path, output_file_path):
    # compress_size 不为空，则只对大于compress_size kb的文件进行压缩操作
    if compress_size.strip() != "" and os.path.getsize(input_file_path) / 1024.0 > int(compress_size):
        if set_max_size_flag:
            transToSpecifiedSizeWebp(input_file_path, output_file_path, max_img_size)
        else:
            transToWebpByQuality(input_file_path, output_file_path, quality)
    elif compress_size.strip() == "" :
        if set_max_size_flag:
            transToSpecifiedSizeWebp(input_file_path, output_file_path, max_img_size)
        else:
            transToWebpByQuality(input_file_path, output_file_path, quality)


def checkInputArgs():
    global input_path
    global output_path

    if (input_path.strip() == ""):
        print("请输入要转换的文件夹路径")
        exit()

    if not input_path.endswith(os.path.sep):
        input_path = input_path + os.path.sep

    if output_path == "":
        output_path = input_path + "webp"

    if not output_path.endswith(os.path.sep):
        output_path = output_path + os.path.sep

    #cwebp命令并不会自动创建输出目录，如果输出目录不存在，则cwebp会报错
    if not os.path.exists(output_path):
        os.makedirs(output_path)


# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少则2字符，长则8字符
'''
文件格式 文件头(十六进制)
JPEG (jpg) FFD8FF
PNG (png) 89504E47
GIF (gif) 47494638
TIFF (tif) 49492A00
Windows Bitmap (bmp) 424D
CAD (dwg) 41433130
Adobe Photoshop (psd) 38425053
Rich Text Format (rtf) 7B5C727466
XML (xml) 3C3F786D6C
HTML (html) 68746D6C3E
Email [thorough only] (eml) 44656C69766572792D646174653A
Outlook Express (dbx) CFAD12FEC5FD746F
Outlook (pst) 2142444E
MS Word/Excel (xls.or.doc) D0CF11E0
MS Access (mdb) 5374616E64617264204A
'''
def typeList():
    return {
        "FFD8FF": "JPEG",
        "89504E47": "PNG",
        "47494638":"GIF",
        "49492A00":"TIFF",
        "424D":"BMP",
        "41433130":"DWG",
        "38425053":"PSD",
        "7B5C727466":"RTF",
        "3C3F786D6C":"XML",
        "68746D6C3E":"HTML",
        "44656C69766572792D646174653A":"EML",
        "CFAD12FEC5FD746F":"DBX",
        "2142444E":"PST",
        "D0CF11E0":"MS",
        "504B0304":"ZIP",
        "5374616E64617264204A":"MDB",
        "25504446":"PDF"
    }

# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()

# 获取文件类型
def filetype(filename):
    binfile = open(filename, 'rb') # 必需二制字读取
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        numOfBytes = len(hcode) / 2 # 需要读多少字节
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype

if __name__ == '__main__':

    getInputArguments()
    checkInputArgs()
    transFiles()