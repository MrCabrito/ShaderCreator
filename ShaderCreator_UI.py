from PySide2 import QtUiTools, QtCore, QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import os


class ShaderCreatorUI(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super(ShaderCreatorUI, self).__init__(parent=parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.widgetPath = "{}/ui/ShaderCreator.ui".format(self.current_dir)
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath)
        self.widget.setParent(self)
        
        # Signals Update UI
        self.update_cbox_shader()

        # Signals Actions
        self.widget.btn_create.clicked.connect(self.action_create_shader)

    def update_cbox_shader(self):
        from .utilities.mel_helper import get_all_shaders
        shaders_list = get_all_shaders()
        self.widget.cbox_shader.clear()
        for shader in shaders_list:
            self.widget.cbox_shader.addItem(shader)

    def action_create_shader(self):
        from.utilities.btn_actions import run_create_shader, run_assign_shader
        shader_name = self.widget.lEdit_name.text()
        shader_type = self.widget.cbox_shader.currentText()
        assign = self.widget.chbox_assign.checkState()
        if assign:
            run_assign_shader(shader_name, shader_type)
        else:
            run_create_shader(shader_name, shader_type)

def main():
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if "ShaderCreatorUI" in win.objectName():
                win.destroy()

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    ShaderCreatorUI.window = ShaderCreatorUI(parent = mayaMainWindow)
    ShaderCreatorUI.window.setObjectName('ShaderCreatorUI') # code above uses this to ID any existing windows
    ShaderCreatorUI.window.setWindowTitle('Shader Creator Tool')
    ShaderCreatorUI.window.show()
