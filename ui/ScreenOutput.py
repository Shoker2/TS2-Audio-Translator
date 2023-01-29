import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut


class Ui_Output_Ui(QMainWindow):
	resized = QtCore.pyqtSignal()

	def __init__(self, use_flags=True, icon_path=''):
		super(Ui_Output_Ui, self).__init__()

		if icon_path != '':
			self.setWindowIcon(QtGui.QIcon(icon_path))

		if use_flags:
			self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)  # Делаю окно поверх всех окон и без рамок
		self.setObjectName("Output_Ui")

		self.textBrowser = QtWidgets.QTextBrowser(self)
		self.textBrowser.setGeometry(QtCore.QRect(0, 0, 0, 0))
		self.textBrowser.setObjectName("textBrowser")

		self.close_shortcut = QShortcut(QKeySequence("Esc"), self) # Выход при 'esc'
		self.close_shortcut.activated.connect(self.close)

		self.resized.connect(self.resize_textBrowser) # Делаю ивент на изменение размера окна
	
	def	setText(self, text: str, point_size: int, font_family:str = ''):
		font = self.font()
		font.setPointSize(point_size) # Делаю шрифт нужного размера
		if font_family != '':
			font.setFamily(font_family)
		self.setWindowTitle("TS2_Output")
		self.textBrowser.setText(text)
		self.textBrowser.setFont(font)
		
	def resizeEvent(self, event):
		self.resized.emit()
		return super(Ui_Output_Ui, self).resizeEvent(event)

	def resize_textBrowser(self):
		self.textBrowser.setGeometry(QtCore.QRect(0, 0, self.size().width(), self.size().height())) #Устанавливаю размер textBrowser как у окна
							
	def closeEvent(self, event):
		self.position_x = self.pos().x()
		self.position_y = self.pos().y()

		self.win_width = self.size().width()
		self.win_height = self.size().height()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	
	Output_Ui = Ui_Output_Ui(False)

	Output_Ui.setText('тестовый текст', 10, 'Wingdings 3')
	Output_Ui.resize(100, 200)
	Output_Ui.move(0, 0)
	
	Output_Ui.show()
	
	sys.exit(app.exec_())