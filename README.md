# **steam个人资料动图制作**
## **本软件包括两个部分：**
 （1）通过ffmpeg实现的视频或者动图的缩小分辨率，调整FPS，并且动图分块，采用PyQt5来制作GUI界面。需要先安装好ffmpeg并且配置好环境变量。

 （2）通过selenium实现的自动上传文件到steam艺术作品中，并且每次上传都会自动填写好创意工坊的JS代码。

# steam个人资料动图的制作流程如下
 （1）把视频转成一个GIF图片，并且设置好各种缩放比例以及帧速率
 
（2）把一张GIF图片按照5/10/15的方法来分割，分别对应单行创意工坊展柜，双行创意工坊展柜以及三行创意工坊展柜。裁剪完成后检查是否有超过5MB的文件。

（3）分割后的图片需要修改文件的十六进制，把末尾的3B改为21。（软件的第一部分）

（4）打开 Steam 艺术作品上传页每次上传之前输入JS代码，软件的第二部分实现了利用selenium自动化上传：
```javascript
$J('#ConsumerAppID').val(480);$J('[name=visibility]').val(0);$J('[name=file_type]').val(0);
```

# 使用方法：
（1）方法1：安装requirements依赖之后运行Qt.py文件可以得到制作工具，打开uploader文件夹运行steamworksUpload.py得到自动上传工具。

（2）方法2：在release里下载我打包好的制作工具和上传工具。上传工具理论上在你下载安装好了Chrome之后，会自动下载一个ChromeDriver到目录
`C:\Users\你的用户名\.cache\selenium\chromedriver\win64`需要安装好Chrome浏览器，想使用别的浏览器可以在源码修改一下。

#### 并没有经过太多的测试，本人也并非专业，如果遇到问题自行解决吧，应该是没有特别大的bug的(😋)