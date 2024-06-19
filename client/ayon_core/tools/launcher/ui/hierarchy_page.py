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


class HierarchyPage(QtWidgets.QWidget):
    def __init__(self, controller, parent):
        super(HierarchyPage, self).__init__(parent)

        # Header
        header_widget = QtWidgets.QWidget(self)

        btn_back_icon = qtawesome.icon("fa.angle-left", color="white")
        btn_back = SquareButton(header_widget)
        btn_back.setIcon(btn_back_icon)

        projects_combobox = ProjectsCombobox(controller, header_widget)

        refresh_btn = RefreshButton(header_widget)

        # Create header layout
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.addWidget(btn_back, 0)
        header_layout.addWidget(projects_combobox, 1)
        header_layout.addWidget(refresh_btn, 0)

        # Create the "create" button
        create_button = QtWidgets.QPushButton("Create Jira Ticket")
        create_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        create_button.clicked.connect(lambda: self._on_jira_ticket_clicked(self._projects_combobox.get_selected_project_name()))

        # Create a layout for the "create" button
        create_button_layout = QtWidgets.QHBoxLayout()
        create_button_layout.setContentsMargins(0, 0, 0, 0)
        create_button_layout.addWidget(create_button)

        create_button_widget = QtWidgets.QWidget()
        create_button_widget.setLayout(create_button_layout)

        # Create content body
        content_body = QtWidgets.QSplitter(self)
        content_body.setContentsMargins(0, 0, 0, 0)
        content_body.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )
        content_body.setOrientation(QtCore.Qt.Horizontal)

        # - Folders widget with filter
        folders_wrapper = QtWidgets.QWidget(content_body)

        folders_filter_text = PlaceholderLineEdit(folders_wrapper)
        folders_filter_text.setPlaceholderText("Filter folders...")

        folders_widget = FoldersWidget(controller, folders_wrapper)

        folders_wrapper_layout = QtWidgets.QVBoxLayout(folders_wrapper)
        folders_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        folders_wrapper_layout.addWidget(folders_filter_text, 0)
        folders_wrapper_layout.addWidget(folders_widget, 1)

        # - Tasks widget
        tasks_widget = TasksWidget(controller, content_body)

        content_body.addWidget(folders_wrapper)
        content_body.addWidget(tasks_widget)
        content_body.setStretchFactor(0, 100)
        content_body.setStretchFactor(1, 65)

        # Create main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(header_widget, 0)
        main_layout.addWidget(create_button_widget, 0)
        main_layout.addWidget(content_body, 1)

        btn_back.clicked.connect(self._on_back_clicked)
        refresh_btn.clicked.connect(self._on_refreh_clicked)
        folders_filter_text.textChanged.connect(self._on_filter_text_changed)

        self._is_visible = False
        self._controller = controller

        self._btn_back = btn_back
        self._projects_combobox = projects_combobox
        self._folders_widget = folders_widget
        self._tasks_widget = tasks_widget

        # Post init
        projects_combobox.set_listen_to_selection_change(self._is_visible)

    def set_page_visible(self, visible, project_name=None):
        if self._is_visible == visible:
            return
        self._is_visible = visible
        self._projects_combobox.set_listen_to_selection_change(visible)
        if visible and project_name:
            self._projects_combobox.set_selection(project_name)

    def refresh(self):
        self._folders_widget.refresh()
        self._tasks_widget.refresh()

    def _on_back_clicked(self):
        self._controller.set_selected_project(None)

    def _on_refreh_clicked(self):
        self._controller.refresh()

    def _on_filter_text_changed(self, text):
        self._folders_widget.set_name_filter(text)

    def _on_jira_ticket_clicked(self, project_name):
        print("here 1")
        self._controller.start_jira_creation(project_name)
