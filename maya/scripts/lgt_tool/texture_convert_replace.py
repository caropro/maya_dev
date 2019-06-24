#coding=utf-8
#author:Jonathon Woo
#version:1.0.0
import pymel.core as pm
import os
import sys
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore


# 贴图格式转换工具面板
class convert_texture(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(convert_texture, self).__init__(parent)
        self.texture_dic = {}
        self.setWindowTitle("Texture format convert")
        self.main_layout = QtWidgets.QVBoxLayout(self)
        # 刷新按钮，与工具信息
        self.task_layout = QtWidgets.QHBoxLayout()
        self.task_label = QtWidgets.QLabel(u"主要目的是将tiff贴图转换为jpg")
        self.refresh_btn = QtWidgets.QPushButton(u"刷新")
        self.mid_path_btn = QtWidgets.QLineEdit("Low_res_tex")
        self.convert_all_btn = QtWidgets.QPushButton(u"转换所有")
        self.convert_btn = QtWidgets.QPushButton(u"转换所选")
        self.replace_all_btn = QtWidgets.QPushButton(u"替换所有")
        self.replace_btn = QtWidgets.QPushButton(u"替换所选")
        self.task_layout.addWidget(self.task_label)
        self.task_layout.addWidget(self.mid_path_btn)
        self.task_layout.addWidget(self.convert_all_btn)
        self.task_layout.addWidget(self.convert_btn)
        self.task_layout.addWidget(self.replace_all_btn)
        self.task_layout.addWidget(self.replace_btn)
        self.task_layout.addWidget(self.refresh_btn)
        self.main_layout.addLayout(self.task_layout)
        # 场景内贴图显示列表
        self.texture_view = QtWidgets.QTableWidget(0, 4)
        self.texture_view.setHorizontalHeaderLabels(
            [u"节点名称",u"贴图路径", u"转换状态", u"替换状态"])
        self.main_layout.addWidget(self.texture_view)
        # 工具关联
        self.refresh_btn.clicked.connect(self.update)
        self.convert_all_btn.clicked.connect(self.convert_all_tex)
        self.convert_btn.clicked.connect(self.convert_tex)
        self.replace_all_btn.clicked.connect(self.replace_all_tex)
        self.replace_btn.clicked.connect(self.replace_tex)
        self.resize(550, 650)
        self.update()
    def update(self):
        # 重置列表，在更新
        self.texture_view.setSortingEnabled(False)
        self.reset_table()
        # 获取所有贴图节点信息，添加到节点列表中。
        textures = pm.ls(type="file")
        rowcount = 0
        for texture in textures:
            texture_map = texture.getAttr("fileTextureName")
            if not self.texture_dic.get(str(texture)):
                self.texture_dic[str(texture)] = {"origin_path":texture_map,"node":texture}
            if texture_map.endswith(".jpg") or texture_map.endswith(".jpeg"):
                continue
            self.texture_view.insertRow(rowcount)
            self.texture_view.setItem(rowcount, 0, QtWidgets.QTableWidgetItem(str(texture)))
            self.texture_view.setItem(rowcount, 1, QtWidgets.QTableWidgetItem(texture_map))
            status_item = QtWidgets.QTableWidgetItem(u"是否转换")
            status_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            print(self.texture_dic[str(texture)],"!!!!!!!!!!!!!!!!!!!!")
            if self.texture_dic[str(texture)].get("new_path"):
                status_item.setFlags(QtCore.Qt.ItemIsEditable)
            self.texture_view.setItem(rowcount,2 , status_item)
            replace_status_item = QtWidgets.QTableWidgetItem(u"是否替换")
            replace_status_item.setCheckState(QtCore.Qt.CheckState.Unchecked)
            self.texture_view.setItem(rowcount,3 , replace_status_item)
            rowcount += 1
        self.texture_view.setSortingEnabled(True)

    def convert_all_tex(self):
        #转换所有并更新
        count = self.texture_view.rowCount()
        for code in range(count):
            print(self.texture_view.item(code, 2).checkState())
            texture_node = self.texture_view.item(code, 0).text()
            old_path = self.texture_view.item(code, 1).text()
            new_path = convert_map(old_path,self.mid_path_btn.text())
            print(self.texture_dic[texture_node])
            self.texture_dic[texture_node]["new_path"] = new_path
            print(self.texture_dic[texture_node])
            print(self.texture_dic[texture_node])
        QtWidgets.QMessageBox.information(self, "Attention", "Done!",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.update()

    def convert_tex(self):
        count = self.texture_view.rowCount()
        for code in range(count):
            if not self.texture_view.item(code, 2).checkState():
                continue
            print(self.texture_view.item(code, 2).checkState())
            texture_node = self.texture_view.item(code, 0).text()
            old_path = self.texture_view.item(code, 1).text()
            new_path = convert_map(old_path,self.mid_path_btn.text())
            print(self.texture_dic[texture_node])
            self.texture_dic[texture_node]["new_path"] = new_path
            print(self.texture_dic[texture_node])
            print(self.texture_dic[texture_node])
        QtWidgets.QMessageBox.information(self, "Attention", "Done!",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.update()

    def replace_all_tex(self):
        #替换所有
        count = self.texture_view.rowCount()
        for code in range(count):
            texture_node_name = self.texture_view.item(code, 0).text()
            replace_map(self.texture_dic[texture_node_name].get("node"),self.texture_dic[texture_node_name].get("new_path"))
        QtWidgets.QMessageBox.information(self, "Attention", "Done!",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.update()

    def replace_tex(self):
        count = self.texture_view.rowCount()
        for code in range(count):
            if not self.texture_view.item(code, 3).checkState():
                continue
            texture_node_name = self.texture_view.item(code, 0).text()
            replace_map(self.texture_dic[texture_node_name].get("node"),self.texture_dic[texture_node_name].get("new_path"))
        QtWidgets.QMessageBox.information(self, "Attention", "Done!",
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        self.update()

    def reset_table(self):
        # 重置列表
        rows = self.texture_view.rowCount()
        row_list = [x for x in range(rows)][::-1]
        for row in row_list:
            self.texture_view.removeRow(row)



# 转换图片为jpg，如果有自定文件夹名称，可以传入
def convert_map(old_path, mid_path=""):
    dir_path = os.path.dirname(old_path)
    file_name = os.path.basename(old_path).replace(".tif", ".jpg")
    if not os.path.exists(os.path.join(dir_path, mid_path)):
        tar_dir=os.mkdir(os.path.join(dir_path, mid_path))
    result_path = os.path.join(dir_path, mid_path, file_name)
    if os.path.exists(result_path):
        return result_path
    image_a = QtGui.QImage(old_path)
    current_image_size = image_a.size()
    result = QtGui.QImage(current_image_size.width(), current_image_size.height(), QtGui.QImage.Format_RGB32)
    painter = QtGui.QPainter()
    painter.begin(result)
    painter.drawImage(0, 0, image_a)
    painter.end()
    result.save(result_path)
    return result_path


# 替换贴图
def replace_map(texture_node, result_path):
    texture_node.setAttr("fileTextureName", result_path)

def run():
    app = convert_texture()
    app.show()
    app.exec_()
