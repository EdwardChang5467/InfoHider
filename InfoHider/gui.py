from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox
import MainWindow
from functools import partial
from ImageSteganography import ImageSteganography
from TextSteganography import TextSteganography
from PIL import Image
from pylab import *
from AES import AESCrypt
import TextEncrypt
import hashlib

# 在载体图片中隐藏图片
def HideImage(ui):
    image1 = ui.lineEdit.text() #获取载体图片路径
    image2 = ui.lineEdit_2.text() #获取需要隐藏图像的路径
    outputpath1 = ui.lineEdit_4.text() #获取输出图片路径
    if image1 == '' or image2 == '' or outputpath1 == '':
        ui.label_9.setPixmap(QPixmap(""))
        ui.tip1()
    else:
        merged_image = ImageSteganography.merge(Image.open(image1), Image.open(image2)) # 进行图片隐藏
        if merged_image == 0:
            ui.tip4()
        else:
            merged_image.save(outputpath1)
            ui.showimage1()
            ui.tip2()

#  提取图片中隐藏私密图片
def ExtractImage(ui):
    image3 = ui.lineEdit.text()       # 获取要进行提取的私密图片
    outputpath2 = ui.lineEdit_4.text()  # 获取图片输出路径
    if image3 == '' or outputpath2 == '':
        ui.label_9.setPixmap(QPixmap(""))
        ui.tip1()
    else:
        unmerged_image = ImageSteganography.unmerge(Image.open(image3))  # 进行图片提取
        unmerged_image.save(outputpath2)
        ui.showimage1()
        ui.tip3()

# 在载体图片中隐藏文本信息
def HideInformation(ui):
    inputpath = ui.lineEdit.text()          # 获取载体图片路径
    message = ui.textEdit.toPlainText()     # 获取要隐藏的私密信息
    outputpath = ui.lineEdit_4.text()       # 获取图片输出路径
    key = ui.lineEdit_6.text()              # 获取用户输入的6位密钥
    if inputpath == '' or message == '' or outputpath == '' or key == '':
        ui.label_9.setPixmap(QPixmap(""))
        ui.tip1()
    elif len(key) != 6:
        ui.label_9.setPixmap(QPixmap(""))
        ui.warn2()
    else:
        message += key
        message = cryptor.aes_encrypt(message)                    # 使用AES加密算法对要隐藏的信息进行加密
        TextSteganography.encode(inputpath, outputpath, message)  # 在图像中隐藏文本信息
        ui.showimage1()
        ui.success1()

# 提取图像中隐藏文本信息
def ExtractInformation(ui):
    img = ui.lineEdit.text()      
    key1 = ui.lineEdit_6.text()   
    if img == '' or key1 == '':
        ui.textEdit_2.setText('')
        ui.tip1()
    elif len(key1) != 6:
        ui.textEdit_2.setText('')
        ui.warn2()
    else:
        result = TextSteganography.decode(img)      # 提取图片中隐藏的文本信息
        if (result == 0):                           # 若提取后文本信息为空提示找不到图片中隐藏信息
            ui.textEdit_2.setText('')
            ui.warn4()
        else:
            result = cryptor.aes_decrypt(result)   # 提取后使用AES算法进行解密
            if (result[-6:] == key1):              # 比对提取后的6位密钥是否与用户输入的密钥相同以判断密钥是否正确
                ui.textEdit_2.setText(str(result[:-6]))
                ui.success2()
            else:
                ui.textEdit_2.setText('')          
                ui.warn5()                          # 发出密钥错误时警告

#在载体文字中隐藏文字
def HideText(ui):
    secret_text = str(ui.textEdit.toPlainText())
    plain_text = str(ui.textEdit_3.toPlainText())
    secret_key = str(ui.lineEdit_6.text())

    #text = plain_text | Encode(AES(secret_text) | md5(secret_key))
    signature = hashlib.md5()
    signature.update(secret_key.encode('utf-8'))
    aesencrypt_text = cryptor.aes_encrypt(secret_text)
    text = plain_text + f'{TextEncrypt.text_to_zero(aesencrypt_text + signature.hexdigest())}'

    ui.textEdit_4.clear()
    ui.textEdit_4.setText(text)

#提取载体文字中隐藏的文字
def ExtractText(ui):
    text = str(ui.textEdit.toPlainText())
    plain_text = str(ui.textEdit_3.toPlainText())
    secret_key = str(ui.lineEdit_6.text())
    signature = hashlib.md5()
    signature.update(secret_key.encode('utf-8'))
    check_text = text.removeprefix(plain_text)
    check_text = TextEncrypt.zero_to_text(check_text)

    if check_text[-32:] == signature.hexdigest():
        aesdecrypt_text = check_text[:-32]
        secret_text = cryptor.aes_decrypt(aesdecrypt_text)
        ui.textEdit_4.clear()
        ui.textEdit_4.setText(secret_text)
    else:
        ui.warn6()

if __name__ == '__main__':
    # 自定义设置AES对称加密16位密匙以提高信息安全性
    secretkey = 'ZGJfXxZNGPqWAC53'
    cryptor = AESCrypt(secretkey)

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    
    # 图像里隐藏图像按钮
    ui.pushButton_10.clicked.connect(partial(HideImage, ui))
    # 图像中提取图像按钮
    ui.pushButton_9.clicked.connect(partial(ExtractImage, ui))
    #图像中隐藏文字按钮
    ui.pushButton_12.clicked.connect(partial(HideInformation, ui))
    #图像中提取文字按钮
    ui.pushButton_13.clicked.connect(partial(ExtractInformation, ui))
    #文字中隐藏文字按钮
    ui.pushButton_14.clicked.connect(partial(HideText, ui))
    #文字中提取文字按钮
    ui.pushButton_15.clicked.connect(partial(ExtractText, ui))

    sys.exit(app.exec_())