import sys

from kernel import find_pyqt

if not find_pyqt:
    print("没有安装 PyQT6 库，请使用 cli 版本")
    sys.exit(1)

from PyQt6.QtWidgets import QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt


class QtComponent:
    QComponentDispatchDict = {
        "PushButton": QPushButton,
        "Label": QLabel,
        "Combo": QComboBox,
        "LineEdit": QLineEdit,
        "TextEdit": QTextEdit,
    }

    def __init__(self, parent, file_path):
        self.parent = parent
        self.components = {}
        # self.strings = {"nul": ""}

        with open(file_path, "r", encoding="utf-8") as f:
            self.read_layout(f)

    def make_component(self, fn: str, key: str, dct: dict[str, str]):
        print(fn, key, dct)
        if fn not in self.QComponentDispatchDict:
            return
        self.components[key] = self.QComponentDispatchDict[fn](self.parent)
        for k, v in dct.items():
            match k:
                case "text":
                    self.components[key].setText(v)
                case "geometry":
                    self.components[key].setGeometry(*map(int, v.split()))
                case "style":
                    with open(f"./assets/{v}.qss", "r", encoding="utf-8") as f:
                        self.components[key].setStyleSheet(f.read())
                case "align":
                    if "left" in v.split('|'):
                        self.components[key].setAlignment(Qt.AlignmentFlag.AlignLeft)
                    if "center" in v.split('|'):
                        self.components[key].setAlignment(Qt.AlignmentFlag.AlignCenter)
                    if "top" in v.split('|'):
                        self.components[key].setAlignment(Qt.AlignmentFlag.AlignTop)
                case "enabled":
                    if v == "true":
                        self.components[key].setEnabled(True)
                    if v == "false":
                        self.components[key].setEnabled(False)

    def read_layout(self, f):
        in_component = False
        fn = ""
        key = ""
        attrs = {}
        for line in f.readlines():
            line = line.strip(" \r\n")
            if line == "" or line.startswith("#"):
                continue
            if line == "End":
                self.make_component(fn, key, attrs)
                in_component = False
                attrs = {}
                continue
            if not in_component:
                fn = line.split()[0]
                key = line.split()[1]
                in_component = True
            else:
                attrs[line.split("=")[0]] = line[line.find("=") + 1:]

    # def make_string(self, key: str, string: str):
    #     self.strings[key] = string
