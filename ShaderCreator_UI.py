from PySide2 import QtUiTools, QtCore, QtWidgets
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import os


class ShaderCreatorUI(QtWidgets.QWidget):
    def __init__(self, parent = None):
        """
         Initialize the Shader Creator UI. This is called by the constructor and should not be called directly.
         
         @param parent - The parent of the widget. If None the widget will be placed in the top level
        """
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
        self.widget.btn_diffuse.clicked.connect(self.browse_file)
        self.widget.btn_specular.clicked.connect(self.browse_file)
        self.widget.btn_roughness.clicked.connect(self.browse_file)
        self.widget.btn_transmission.clicked.connect(self.browse_file)
        self.widget.btn_sss.clicked.connect(self.browse_file)
        self.widget.btn_sssColor.clicked.connect(self.browse_file)
        self.widget.btn_bump.clicked.connect(self.browse_file)
        self.widget.btn_displacement.clicked.connect(self.browse_file)

    def update_cbox_shader(self):
        """
         Update cbox_shader combobox with shaders from MelHelper.
        """
        from .utilities.mel_helper import get_all_shaders
        shaders_list = get_all_shaders()
        self.widget.cbox_shader.clear()
        # Add shader to the widget from shader list
        for shader in sorted(shaders_list):
            self.widget.cbox_shader.addItem(shader)

    def browse_file(self):
        """
         Browse for file and save it in lEdit widget
        """
        from .utilities.mel_helper import dialog_window
        button = self.sender()
        lEdit_name = 'lEdit_{}'.format(button.objectName().split('_')[-1])
        lEdit = self.widget.findChild(QtCore.QObject, lEdit_name)
        path = dialog_window()
        lEdit.setText(path[0])

    def action_create_shader(self):
        """
         Create a Shader and return the material and SG for it.
        """
        from .utilities.btn_actions import run_create
        shader_name = self.widget.lEdit_name.text()
        shader_type = self.widget.cbox_shader.currentText()
        assign = self.widget.chbox_assign.checkState()

        attr_status_dict = {
            'diffuse': self.widget.chbox_diffuse.checkState(),
            'specular': self.widget.chbox_specular.checkState(),
            'roughness': self.widget.chbox_roughness.checkState(),
            'transmission': self.widget.chbox_transmission.checkState(),
            'sss': self.widget.chbox_sss.checkState(),
            'sssColor': self.widget.chbox_sssColor.checkState(),
            'bump': self.widget.chbox_bump.checkState(),
            'displacement': self.widget.chbox_displacement.checkState(),
        }

        #Checks if the checkbox value is False to remove does keys
        attr_list = [k for (k,v) in attr_status_dict.items() if v!=0]
        textures_path_dict = dict()
        # This function will set the textures_path_dict dictionary of textures in the widget.
        if attr_list:
            # This function will be called by the widget to get the textures path_dict
            for attr in attr_list:
                item = "lEdit_{}".format(attr)
                textures_path_dict[attr] = self.widget.findChild(QtCore.QObject, item).property("text")
        
        message = run_create(shader_name, shader_type, assign, textures_path_dict)
        if message:
            dlg = QtWidgets.QMessageBox(self)
            dlg.setWindowTitle("Error Found")
            dlg.setText(message)
            dlg.exec_()

def main():
    """
     Launch Shader Creator Tool in a new QApplication. This is called by omui. MQtUtil. mainWindow
    """
    # Destroy all Windows and all Windows.
    if QtWidgets.QApplication.instance():
        for win in (QtWidgets.QApplication.allWindows()):
            if "ShaderCreatorUI" in win.objectName():
                win.destroy()

    tool_name = 'Shader Creator Tool'
    tool_version = "v1.0.1"
    author = "Abraham Gonzalez"
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    ShaderCreatorUI.window = ShaderCreatorUI(parent = mayaMainWindow)
    ShaderCreatorUI.window.setObjectName('ShaderCreatorUI') # code above uses this to ID any existing windows
    ShaderCreatorUI.window.setWindowTitle('{0} {1}'.format(tool_name, tool_version))
    ShaderCreatorUI.window.show()
