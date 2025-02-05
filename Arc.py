import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QFileDialog, QHBoxLayout
from PyQt5.QtCore import QResource
from PyQt5.QtGui import QIcon


class FolderCreatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("文件夹创建工具")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("C:/Users/Jiading Zhang/Desktop/Project/Arc/icon.png"))
        # self.setStyleSheet("background-color: #f0f0f0;")
        # 创建布局
        layout = QVBoxLayout()

        # 创建标签和输入框
        self.label_path = QLabel("目标路径:")
        self.entry_path = QLineEdit()
        self.entry_path.setPlaceholderText("请输入目标路径")
        self.button_browse = QPushButton("浏览")
        self.button_browse.clicked.connect(self.browsePath)

        path_layout = QVBoxLayout()
        path_layout.addWidget(self.label_path)
        path_layout.addWidget(self.entry_path)
        path_layout.addWidget(self.button_browse)

        self.label_first_folder = QLabel("一级文件夹:")
        self.entry_first_folder = QLineEdit()
        self.entry_first_folder.setPlaceholderText("请输入一级文件夹名称")

        first_folder_layout = QVBoxLayout()
        first_folder_layout.addWidget(self.label_first_folder)
        first_folder_layout.addWidget(self.entry_first_folder)

        self.label_second_folder = QLabel("二级文件夹（换行分隔）:")
        self.entry_second_folder = QTextEdit()
        self.entry_second_folder.setPlaceholderText("请输入二级文件夹名称，每个名称占一行")

        second_folder_layout = QVBoxLayout()
        second_folder_layout.addWidget(self.label_second_folder)
        second_folder_layout.addWidget(self.entry_second_folder)

        # 创建按钮
        self.button_create = QPushButton("确定")
        self.button_create.clicked.connect(self.createFolders)
        self.button_clear = QPushButton("清空")
        self.button_clear.clicked.connect(self.clearEntries)
        self.button_exit = QPushButton("退出")
        self.button_exit.clicked.connect(self.close)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button_create)
        button_layout.addWidget(self.button_clear)
        button_layout.addWidget(self.button_exit)

        # 添加到布局
        layout.addLayout(path_layout)
        layout.addLayout(first_folder_layout)
        layout.addLayout(second_folder_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def browsePath(self):
        path = QFileDialog.getExistingDirectory(self, "选择目录")
        if path:
            self.entry_path.setText(path)

    def validatePath(self, path):
        return os.path.exists(path) and os.access(path, os.W_OK)

    def createFolders(self):
        base_path = self.entry_path.text().strip()
        first_folder_name = self.entry_first_folder.text().strip()
        second_folders = [folder.strip() for folder in self.entry_second_folder.toPlainText().split('\n') if folder.strip()]

        if not base_path or not first_folder_name:
            QMessageBox.warning(self, "警告", "请输入目标路径和一级文件夹名称")
            return

        if not self.validatePath(base_path):
            QMessageBox.critical(self, "错误", "目标路径无效或不可写，请检查路径")
            return

        success_count = 0
        error_count = 0

        for folder in second_folders:
            full_path = os.path.join(base_path, first_folder_name, folder)
            try:
                os.makedirs(full_path, exist_ok=True)
                success_count += 1
            except PermissionError:
                error_count += 1
                QMessageBox.critical(self, "错误", f"权限不足，无法创建文件夹: {full_path}")
                break
            except OSError as e:
                error_count += 1
                QMessageBox.critical(self, "错误", f"创建文件夹失败: {full_path}，原因: {e}")
                break

        if success_count > 0 and error_count == 0:
            QMessageBox.information(self, "成功", f"共创建 {success_count} 个文件夹")
        elif error_count > 0 and success_count == 0:
            QMessageBox.critical(self, "错误", "创建所有文件夹时出错，请检查输入路径和名称是否正确。")
        else:
            QMessageBox.warning(self, "警告", f"成功创建 {success_count} 个文件夹，{error_count} 个文件夹创建失败")

    def clearEntries(self):
        self.entry_path.clear()
        self.entry_first_folder.clear()
        self.entry_second_folder.clear()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出', '确定要退出吗？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FolderCreatorApp()
    ex.show()
    sys.exit(app.exec_())
