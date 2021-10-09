import sys
from design import Ui_MainWindow
from PyQt5 import QtWidgets
import DES

ERR = -1
ENCRYPT = 0
DECRYPT = 1


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnSelectFile.clicked.connect(self.select_image)
        self.ui.btnCalculate.clicked.connect(self.calculate)

    def select_image(self):
        self.ui.txtInputFile.setText(
            QtWidgets.QFileDialog.getOpenFileName()[0])

    def validate_selected_operation(self):
        decrypt = self.ui.rbDecrypt.isChecked()
        encrypt = self.ui.rbEncrypt.isChecked()
        if decrypt or encrypt:
            return True, DECRYPT if decrypt else ENCRYPT
        else:
            return False, ERR

    def get_selected_mode(self):
        if self.ui.rbECB.isChecked():
            return DES.ECB
        elif self.ui.rbCFB.isChecked():
            return DES.CFB
        elif self.ui.rbCBC.isChecked():
            return DES.CBC
        elif self.ui.rbOFB.isChecked():
            return DES.OFB
        else:
            return ERR

    def calculate(self):
        dialog = QtWidgets.QMessageBox
        desCipher = DES.DESCipher()
        selected, operation = self.validate_selected_operation()
        selected_mode = self.get_selected_mode()
        image_path = self.ui.txtInputFile.text()
        key = self.ui.txtKey.text()
        init_vector = self.ui.txtInitVector.text()

        if not selected:
            dialog.about(self, "Invalid operation",
                         "Please select a valid operation")
            return

        if selected_mode == ERR:
            dialog.about(self, "Invalid mode",
                         "Please select a valid mode")
            return

        if(not image_path or image_path[-4:] != ".bmp"):
            dialog.about(self, "Invalid image",
                         "Please select a valid image in format bmp")
            return

        if(not key or len(key) != 8):
            dialog.about(self, "Invalid key",
                         "Please enter a valid key")
            return

        if(not init_vector or len(init_vector) != 8):
            dialog.about(self, "Invalid init vector",
                         "Please enter a valid init vector")
            return

        if operation == ENCRYPT:
            desCipher.encrypt(key, selected_mode,
                              image_path, init_vector)
        elif operation == DECRYPT:
            desCipher.decrypt(key, selected_mode,
                              image_path, init_vector)
        else:
            dialog.about(self, "ERROR",
                         "Sorry, something went wrong. Try again")
            return


app = QtWidgets.QApplication([])

application = Window()

application.show()

sys.exit(app.exec())
