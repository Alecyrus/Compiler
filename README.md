# 运行环境
`操作系统`：ubuntu 16.04 LTS
`语言环境`：Python 3.4+

# 操作步骤
>语法分析器为`syntax.py`
词法分析器为`lexicale.py`
入口文件为`analyzer.py`

## 安装
### 获取源代码
通过提交的源代码或者从github上clone
> \# git clone https://github.com/Alecyrus/Compliers.git

### 安装依赖
> \# pip3 install -r requirement.txt

### 试运行
> \# python3 analyzer.py test
若出现缺少模块错误，使用pip3安装相应模块即可

## 使用说明
> 默认文法为报告书上的文法经过修改后的可通过以下命令查看
> \# python3 analyzer.py like_c_productions
>
>![](http://upload-images.jianshu.io/upload_images/1113810-20bfc03113c47c0d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
>
>暂不支持界面输入文法，若需要修改文法，进入`analyzer.py` 修改变量`self.like_c_productions`即可

### 运行测试示例
> \# python3 analyzer.py test --verbose


`--verbose`: `Optional`，除了显示结果外，还会显示符号表，分析表等内容

### 显示当前文法以及对应的分析表
> \# python3 analyzer.py show


### 进入即时编译环境
> \# python3 analyzer.py compiler

>然后，输入多行代码，按`Ctrl+D`结束代码输入进行编译，若输入的代码不符合文法，则会显示相应错误。
>
>![](http://upload-images.jianshu.io/upload_images/1113810-1d7d6a31e0cf3137.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 示例：

>![Paste_Image.png](http://upload-images.jianshu.io/upload_images/1113810-4c5cd9aa2c6ccb7e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

>![Paste_Image.png](http://upload-images.jianshu.io/upload_images/1113810-dabb42b903c37764.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)





