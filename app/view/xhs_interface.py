# coding:utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidgetItem,
    QAbstractItemView,
)
from qfluentwidgets import SearchLineEdit, TableWidget, ComboBox, CheckBox
import config


class SearchLineEdits(SearchLineEdit):
    """Search line edit"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setPlaceholderText("请输入🔎关键词搜索🔍")


class SearchComboBox(ComboBox):
    """Search line edit"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 爬取类型，search(关键词搜索) | detail(帖子详情)| creator(创作者主页数据)
        self.addItem("🔎关键词搜索🔍", userData="search")
        self.addItem("📃帖子详情📃", userData="detail")
        self.addItem("🙆‍♀️创作者主页数据🙆‍♀️", userData="creator")

        self.setMinimumWidth(180)

        # self.currentIndexChanged.connect()

    def setConfig(self):
        self.setCurrentText(config.search_type)


class LoginStatusBox(CheckBox):
    """Login Status CheckBox"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText("是否保存登录状态")
        self.setCheckable(True)


class XhsView(QFrame):
    """Xhs interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.loginStatus = LoginStatusBox(self)
        self.searchLineEdit = SearchLineEdits(self)
        self.searchComboBox = SearchComboBox(self)

        self.searchComboBox.currentIndexChanged.connect(
            lambda index: self.searchLineEdit.setPlaceholderText(
                f"请输入{self.searchComboBox.currentText()}"
            )
        )

        self.statusManagement = QFrame(self)
        self.formSearch = QFrame(self)
        self.table = QFrame(self)
        # self.tableSearch = TableWidget(self)

        self.statusManagementLayout = QHBoxLayout(self.statusManagement)
        self.viewLayout = QVBoxLayout(self)
        self.formSearchLayout = QHBoxLayout(self.formSearch)

        self.tableLayout = QHBoxLayout(self.table)

        self.__initWidget()

    def __initWidget(self):
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(12)
        self.viewLayout.addWidget(self.formSearch)
        self.viewLayout.addWidget(self.statusManagement)
        self.viewLayout.addWidget(self.table)
        # 搜索
        self.formSearchLayout.setContentsMargins(0, 0, 0, 0)
        self.formSearchLayout.setSpacing(12)
        self.formSearchLayout.addWidget(self.searchComboBox)
        self.formSearchLayout.addWidget(self.searchLineEdit)
        # 状态管理
        self.statusManagementLayout.setContentsMargins(0, 0, 0, 0)
        self.statusManagementLayout.setSpacing(12)
        self.statusManagementLayout.addWidget(self.loginStatus)
        # 表格
        self.tableLayout.setSpacing(0)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.addWidget(TableFrame(self))


class TableFrame(TableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # self.verticalHeader().hide() # 隐藏垂直表头
        self.setBorderRadius(8)  # 设置边框圆角
        self.setBorderVisible(True)  # 设置边框可见
        self.setColumnCount(14)  # 设置列数
        self.setRowCount(60)  # 设置行数
        self.setSortingEnabled(True)  # 开启排序功能
        self.setAlternatingRowColors(True)  # 开启交替行颜色

        header = {
            "red_id": "小红书ID",
            "nickname": "昵称",
            "like_count": "点赞数",
            "content": "评论内容",
            "comment_id": "评论ID",
            "user_id": "用户ID",
            "note_id": "帖子ID",
            "avatar": "头像",
            "pictures": "图片",
            "sub_comment_count": "子评论数",
            "parent_comment_id": "父评论ID",
            "last_modify_ts": "最后修改时间",
            "create_time": "评论时间",
            "ip_location": "IP地址",
        }

        header_value = []
        header_key = []

        for key, value in header.items():
            header_value.append(value)
            header_key.append(key)

        self.setHorizontalHeaderLabels(header_value)

        import json

        with open(
            "data/xhs/json/search_comments_2024-12-21.json", "r", encoding="utf-8"
        ) as f:
            data = json.load(f)
            for i, comment in enumerate(data):
                # 根据表头顺序重新排列数据
                ordered_comment = {key: comment.get(key, "") for key in header_key}

                for j, key in enumerate(header_key):
                    value = ordered_comment[key]
                    if value is None:
                        value = ""
                    # 使用 setItem 设置表格项，确保以表头定义的顺序填充数据
                    self.setItem(i, j, QTableWidgetItem(str(value)))

        self.resizeColumnsToContents()


class XhsInterface(QFrame):
    """Xhs interface"""

    def __init__(self, parent=None):
        super().__init__()
        self.setObjectName("xhsInterface")
        self.vBoxLayout = QVBoxLayout(self)

        self.xhsView = XhsView(self)
        self.vBoxLayout.addWidget(self.xhsView)
