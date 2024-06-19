import qtawesome
from qtpy import QtWidgets, QtCore

from ayon_core.tools.utils import (
    PlaceholderLineEdit,
    SquareButton,
    RefreshButton,
)
from ayon_core.tools.utils import (
    ProjectsCombobox,
    FoldersWidget,
    TasksWidget,
)


class JiraPage(QtWidgets.QWidget):
    def __init__(self, controller, parent):
        super(JiraPage, self).__init__(parent)

        # Header
        header_widget = QtWidgets.QWidget(self)

        btn_back_icon = qtawesome.icon("fa.angle-left", color="white")
        btn_back = SquareButton(header_widget)
        btn_back.setIcon(btn_back_icon)

        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(btn_back, 0)
        header_layout.addWidget(QtWidgets.QLabel("Create Jira Ticket"), 1)

        self._is_visible = False
        self._controller = controller
        self._btn_back = btn_back

        lbl_description = QtWidgets.QLabel("Description")
        txt_description = QtWidgets.QLineEdit()

        lbl_steps = QtWidgets.QLabel("Steps to Reproduce")
        txt_steps = QtWidgets.QLineEdit()

        lbl_priority = QtWidgets.QLabel("Priority")
        cmb_priority = QtWidgets.QComboBox()
        cmb_priority.addItems(["Lowest", "Low", "Medium", "High", "Highest", "Fire"])

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(header_widget)
        layout.addWidget(lbl_description)
        layout.addWidget(txt_description)
        layout.addWidget(lbl_steps)
        layout.addWidget(txt_steps)
        layout.addWidget(lbl_priority)
        layout.addWidget(cmb_priority)

        btn_submit = QtWidgets.QPushButton("Submit")
        btn_cancel = QtWidgets.QPushButton("Cancel")
        layout.addWidget(btn_submit)
        layout.addWidget(btn_cancel)

    def set_page_visible(self, visible, project_name=None):
        if self._is_visible == visible:
            return
        self._is_visible = visible

    def _on_back_clicked(self):
        self._controller.set_selected_project(None)
