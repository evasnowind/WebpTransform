# encoding=utf-8
# author EvilsoulM
# rewrite by evasnowind at 2018.1.23

import commands
import os
import sys, getopt
import shutil

input_path = ""
quality = "75"

output_path = "webp"
compress_size = ""

show_process = False

'''
TODO 一些想法：
添加-t XXX 配置项，用于限定webp格式图片最多可以多少KB，用于动态限定图片压缩大小。
因为实际工作中经常遇到要求图片不能超过多少KB的情况，那么此时压缩配置项
中应该配置：
    -i inputpath -o outputpath -s X -t Y   
    小于X KB的文件不用压缩
    图片最大达到Y左右
    
    而google提供的压缩工具包只能设置压缩比例。因此对于上述情况，
    需要不断循环尝试，从比较大的quality开始，看结果是否满足要求，
    如此不断重复尝试，设置一个步长来逐次逼近。
    
    如果图片过大、不能达到要求，那么就用quality = 1的比例进行压缩。
    
    上述思路是完全可以做到的，有兴趣的童鞋可以练练手。
    add by evasnowind 2018.1.23
'''

def getInputArguments():

    opts, args = getopt.getopt(sys.argv[1:], "hi:o:q:s:",["process"])
    global quality
    global output_path
    global compress_size
    global input_path
    global show_process

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
            print("image quality[0-poor, 100-very good] = " + quality)
        elif op == "-s":
            compress_size = value
            print("images which are bigger than " + compress_size + " KB will be compressed.")
        elif op == "--process":

            show_process = True
            print("show cwebp compress process.")

    print ""


def transformToWebp():

    files = os.listdir(input_path)
    for f in files:
        splite_name = os.path.splitext(f)

        img_file_path = input_path + f

        #TODO 根据文件头的magic number来判断文件类型更准确，因此后续可以改成：如果magic number不是webp，则进行压缩
        if (splite_name[1] == ".webp" or (splite_name[1] != ".jpg" and splite_name[1] != ".png")):
            continue

        webp_output_path = output_path + "/" + splite_name[0] + ".webp"

        # compress_size 不为空，则只对大于compress_size kb的文件进行压缩操作
        if (compress_size.strip() != "" and os.path.getsize(img_file_path) / 1024.0 > int(compress_size)):
            command = "cwebp -q " + quality + " " + img_file_path + " -o " + webp_output_path
            print("压缩 " + img_file_path + "，执行命令:" + command)
            if(show_process):
                os.system(command)
            else:
                commands.getstatusoutput(command)
        elif (compress_size.strip() == ""):
            command = "cwebp -q " + quality + " " + img_file_path + " -o " + webp_output_path
            print("压缩 " + img_file_path + "，执行命令:" + command)
            if (show_process):
                os.system(command)
            else:
                commands.getstatusoutput(command)
        else:
            print("没有压缩文件 " + img_file_path)

    #copyWebpFiles(final_input_file, outputPath + output_file)

def checkInputArgs():
    global input_path
    global output_path

    if (input_path.strip() == ""):
        print("请输入要转换的文件夹路径")
        exit()

    if not input_path.endswith("/"):
        input_path = input_path + "/"

    if not output_path.endswith(""):
        output_path = output_path + "/"

    #cwebp命令并不会自动创建输出目录，如果输出目录不存在，则cwebp会报错
    if not os.path.exists(output_path):
        os.makedirs(output_path)

def copyToOutputFile():
    final_input_file = sys.path[0] + "/" + input_path

    files = os.listdir(final_input_file)
    for f in files:
        print(f)

#直接在输入参数中写明输出目录，也就没必要再复制一遍
def copyWebpFiles(sourceDir, targetDir):
    if not os.path.exists(targetDir):
        os.makedirs(targetDir)

    print sourceDir
    print(targetDir)

    for file in os.listdir(sourceDir):
        spliteName = os.path.splitext(file)
        if (spliteName[1] != ".webp"):  # 只复制webp文件
            continue

        sourceFile = os.path.join(sourceDir, file)
        targetFile = os.path.join(targetDir, file)

        if os.path.isfile(sourceFile):
            shutil.copy(sourceFile, targetFile)
            os.remove(sourceFile)


if __name__ == '__main__':

    getInputArguments()
    checkInputArgs()
    transformToWebp()