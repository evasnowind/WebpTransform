##Webp png jpg 批量转webp脚本

###使用
- 配置环境 <p>
 1.安装cwebp <p>
   brew install webp <p>
- 参数 <p>
    -s X 大小超过X kb的图片才进行压缩
    -m X 压缩后的图片不能超过X kb
    -i X 输入文件夹路径
    -o X 输出文件夹路径，如果不写，默认为输入文件夹下新建一个webp文件夹
    -q X 设置百分比进行压缩，0-100，100质量最高，默认80
    --process 不用带参数，开关变量，设置后将显示webp压缩图片过程（google cwebp命令的输出）

- 使用 <p>
-i 是必须输入的参数
-o 不输入情况下采用输入文件夹下新建一个webp文件夹
-s 不输入则直接压缩
-q 默认为80
-m 不输入情况下仅进行一次压缩，输出文件大小不做限定
 ```
    python webputils.py -i img/source/dir -s 20 -q 50 -o webp/output/dir -m 50 #转换img/source/dir中大于20kb的图片到webp/output/dir目录下（质量是50）
    如果设置了-m配置项，则-q的配置项将不再生效。因为设置了输出文件最大阈值的情况下，需要不断调整压缩质量参数（第一次压缩时采用默认压缩质量80），逐步逼近。
 ```
