import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon

class SystemTray(QSystemTrayIcon):
	def __init__(self, icon_path, parent=None, name='Test'):
		QSystemTrayIcon.__init__(self, icon_path, parent)
		self.app = parent
		
		self.setToolTip(name)

		self.set_menu()
	
	def set_menu(self):
		menu = QMenu()
		exitAction = menu.addAction('Exit')
		exitAction.triggered.connect(self.exit)

		self.setContextMenu(menu)
	
	def	exit(self):
		sys.exit(0)

def	main():
	app = QApplication(sys.argv)

	tray = SystemTray(QIcon('icon.png'), app)
	tray.show()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()