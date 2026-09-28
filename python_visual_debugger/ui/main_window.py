from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QListWidget, QSplitter, QMessageBox,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QColor, QTextFormat, QTextCursor

from engine.debugger import PythonDebugger
from ui.python_highlighter import PythonHighlighter
from ui.code_editor import CodeEditor


DEFAULT_CODE = '''# مثال ساده‌ی حلقه و شرط
x = 10
y = 20
total = x + y
print("total =", total)

for i in range(3):
    value = i * 2
    print("i =", i, "value =", value)

print("done")
'''


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Python Visual Debugger")
        self.resize(1500, 900)

        self.debugger: PythonDebugger | None = None
        self.current_line = -1

        self.play_timer = QTimer(self)
        self.play_timer.setInterval(600)
        self.play_timer.timeout.connect(self._auto_play_tick)

        self.setup_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------
    def setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(4)

        title = QLabel("Python Visual Debugger")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "QLabel { font-size: 24px; font-weight: bold; padding: 2px 0 6px 0; }"
        )
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # ============ Code panel ============
        code_widget = QWidget()
        code_layout = QVBoxLayout(code_widget)
        code_layout.setContentsMargins(2, 2, 2, 2)
        code_layout.setSpacing(2)
        code_layout.addWidget(QLabel("Python Code"))

        self.code_editor = CodeEditor()
        self.code_editor.setPlainText(DEFAULT_CODE)
        self.code_editor.setFont(QFont("Consolas", 13))
        self.code_editor.setLineWrapMode(CodeEditor.NoWrap)
        self.code_editor.setTabStopDistance(
            4 * self.code_editor.fontMetrics().horizontalAdvance(' ')
        )
        self.code_editor.setStyleSheet(
            "QPlainTextEdit {"
            "  background-color: #1E1E1E;"
            "  color: #D4D4D4;"
            "  border: 1px solid #333;"
            "  selection-background-color: #264F78;"
            "}"
        )
        self.code_editor.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.highlighter = PythonHighlighter(self.code_editor.document())

        code_layout.addWidget(self.code_editor)
        splitter.addWidget(code_widget)

        # ============ Center panel ============
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(2, 2, 2, 2)
        center_layout.setSpacing(4)

        self.step_label = QLabel("Step: 0")
        self.step_label.setStyleSheet("QLabel { font-size: 15px; }")

        self.current_line_label = QLabel("Current line: —")
        self.current_line_label.setStyleSheet(
            "QLabel { font-size: 16px; font-weight: bold; padding: 2px; }"
        )

        self.explanation = QTextEdit()
        self.explanation.setReadOnly(True)
        self.explanation.setPlaceholderText("What is happening will appear here...")
        self.explanation.setFont(QFont("Consolas", 12))
        self.explanation.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        center_layout.addWidget(self.step_label)
        center_layout.addWidget(self.current_line_label)
        center_layout.addWidget(self.explanation, 1)
        splitter.addWidget(center_widget)

        # ============ Variables panel ============
        variable_widget = QWidget()
        variable_layout = QVBoxLayout(variable_widget)
        variable_layout.setContentsMargins(2, 2, 2, 2)
        variable_layout.setSpacing(2)
        variable_layout.addWidget(QLabel("Variables"))

        self.variables_list = QListWidget()
        self.variables_list.setFont(QFont("Consolas", 12))
        self.variables_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        variable_layout.addWidget(self.variables_list)
        splitter.addWidget(variable_widget)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)
        splitter.setStretchFactor(2, 3)
        splitter.setSizes([600, 400, 500])

        main_layout.addWidget(splitter, 1)

        # ---------------- Buttons ----------------
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(4)

        self.start_button    = QPushButton("▶ Start")
        self.previous_button = QPushButton("◀ Previous")
        self.next_button     = QPushButton("Next ▶")
        self.run_button      = QPushButton("⏩ Auto Run")
        self.restart_button  = QPushButton("↻ Restart")
        self.clear_button    = QPushButton("🧹 Clear output")

        for b in (
            self.start_button, self.previous_button, self.next_button,
            self.run_button, self.restart_button, self.clear_button,
        ):
            b.setMinimumHeight(30)
            b.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            button_layout.addWidget(b)

        main_layout.addLayout(button_layout)

        # ---------------- Signals ----------------
        self.start_button.clicked.connect(self.start_debugging)
        self.next_button.clicked.connect(self.next_step)
        self.previous_button.clicked.connect(self.previous_step)
        self.restart_button.clicked.connect(self.restart)
        self.run_button.clicked.connect(self.toggle_auto_run)
        self.clear_button.clicked.connect(self.clear_output)

    # ------------------------------------------------------------------
    # Debugger control
    # ------------------------------------------------------------------
    def start_debugging(self) -> None:
        self.play_timer.stop()
        self.run_button.setText("⏩ Auto Run")

        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "Error", "Please enter some Python code.")
            return

        self.debugger = PythonDebugger(code)

        if self.debugger.error:
            QMessageBox.warning(
                self, "Trace warning",
                self.debugger.error
                + "\n\nTracing may have stopped early. "
                  "See the snapshots recorded so far.",
            )

        n = len(self.debugger.snapshots)
        self.step_label.setText(f"Steps recorded: {n}")
        self.current_line_label.setText("Current line: —")
        self.variables_list.clear()
        self.explanation.clear()

        if n == 0:
            self.explanation.setPlainText(
                "No steps were traced.\n\n"
                + (self.debugger.error or "Unknown reason.")
            )
            return

        first = self.debugger.next_step()
        if first is not None:
            self.show_snapshot(first)

    def next_step(self) -> None:
        if self.debugger is None:
            self.start_debugging()
            return
        snapshot = self.debugger.next_step()
        if snapshot is None:
            return
        self.show_snapshot(snapshot)

    def previous_step(self) -> None:
        if self.debugger is None:
            return
        snapshot = self.debugger.previous_step()
        if snapshot is None:
            return
        self.show_snapshot(snapshot)

    def restart(self) -> None:
        self.play_timer.stop()
        self.run_button.setText("⏩ Auto Run")
        if self.debugger is None:
            return
        self.debugger.restart()
        self.step_label.setText("Step: 0")
        self.current_line_label.setText("Current line: —")
        self.variables_list.clear()
        self.explanation.clear()
        self._clear_highlight()

    def clear_output(self) -> None:
        self.explanation.clear()
        self.variables_list.clear()
        self.step_label.setText("Step: 0")
        self.current_line_label.setText("Current line: —")
        self._clear_highlight()

    def toggle_auto_run(self) -> None:
        if self.debugger is None:
            self.start_debugging()

        if self.debugger is None or not self.debugger.snapshots:
            return

        if self.play_timer.isActive():
            self.play_timer.stop()
            self.run_button.setText("⏩ Auto Run")
        else:
            self.run_button.setText("⏸ Pause")
            self.play_timer.start()

    def _auto_play_tick(self) -> None:
        snapshot = self.debugger.next_step() if self.debugger else None
        if snapshot is None:
            self.play_timer.stop()
            self.run_button.setText("⏩ Auto Run")
            return
        self.show_snapshot(snapshot)

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------
    def show_snapshot(self, snapshot) -> None:
        self.step_label.setText(f"Step: {snapshot.step}")
        self.current_line_label.setText(f"Current line: {snapshot.line_number}")

        self.variables_list.clear()
        safe_repr = PythonDebugger.safe_repr
        for name, value in snapshot.variables.items():
            self.variables_list.addItem(f"{name} = {safe_repr(value)}")

        self.highlight_line(snapshot.line_number)
        self.explanation.setPlainText(self.create_explanation(snapshot))

    # -------- line highlight --------
    def highlight_line(self, line_number: int) -> None:
        doc = self.code_editor.document()
        if line_number < 1 or line_number > doc.blockCount():
            return

        block = doc.findBlockByNumber(line_number - 1)
        if not block.isValid():
            return

        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor("#264F78"))
        selection.format.setProperty(QTextFormat.FullWidthSelection, True)

        cursor = QTextCursor(block)
        cursor.clearSelection()
        selection.cursor = cursor

        self.code_editor.setExtraSelections([selection])

        # scroll
        visible = QTextCursor(block)
        self.code_editor.setTextCursor(visible)
        self.code_editor.centerCursor()

    def _clear_highlight(self) -> None:
        self.code_editor.setExtraSelections([])

    def create_explanation(self, snapshot) -> str:
        parts = []
        parts.append(f"▶ Executing line {snapshot.line_number}:")
        parts.append(f"    {snapshot.source_line}")
        parts.append("")

        if snapshot.stdout:
            parts.append("🖨  Output on this line:")
            for line in snapshot.stdout.rstrip("\n").splitlines():
                parts.append(f"    {line}")
            parts.append("")

        if snapshot.changed_vars:
            parts.append("✏  Variables changed on this line:")
            safe_repr = PythonDebugger.safe_repr
            for name, value in snapshot.changed_vars.items():
                parts.append(f"    {name} = {safe_repr(value)}")
            parts.append("")

        if not snapshot.stdout and not snapshot.changed_vars:
            parts.append("(no visible side-effects on this line)")

        return "\n".join(parts)