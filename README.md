##Webp png jpg 批量转webp脚本

###使用
- 配置环境 <p>
 1.安装cwebp <p>
   brew install webp <p>
- 参数 <p>
 -s 最小要压缩图片大小 （kb）<p>
 -i 要压缩的图片文件夹目录 <p>
 -o 输出目录 <p>
 -q 压缩图片质量  默认75 <p>
 --process 不需要带参数，用于控制是否显示压缩过程中的一些信息（cwebp命令的输出）<p>

- 使用 <p>

 ```
    python webputils.py -i img/source/dir -s 20 -q 50 -o webp/output/dir  #转换img/source/dir中大于20kb的图片到webp/output/dir目录下（质量是50）
 ```

- 后续的一些想法 <p>

添加-t XXX 配置项，用于限定webp格式图片最多可以多少KB，用于动态限定图片压缩大小。
因为实际工作中经常遇到要求图片不能超过多少KB的情况，那么此时压缩配置项
中应该配置：

 ```
    -i inputpath -o outputpath -s X -t Y   
    小于X KB的文件不用压缩
    图片最大达到Y左右
 ```

而google提供的压缩工具包只能设置压缩比例。因此对于上述情况，需要不断循环尝试，从比较大的quality开始，看结果是否满足要求，如此不断重复尝试，设置一个步长来逐次逼近。如果图片过大、不能达到要求，那么就用quality = 1的比例进行压缩。上述思路是完全可以做到的，有兴趣的童鞋可以练练手。