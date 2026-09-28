from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import (
    QSyntaxHighlighter,
    QTextCharFormat,
    QColor,
    QFont,
)


class PythonHighlighter(QSyntaxHighlighter):
    """Python syntax highlighter with triple-quoted string support."""

    def __init__(self, document):
        super().__init__(document)
        self.rules = []

        # ---------- formats ----------
        keyword_fmt = QTextCharFormat()
        keyword_fmt.setForeground(QColor("#C586C0"))
        keyword_fmt.setFontWeight(QFont.Bold)

        builtin_fmt = QTextCharFormat()
        builtin_fmt.setForeground(QColor("#4EC9B0"))

        string_fmt = QTextCharFormat()
        string_fmt.setForeground(QColor("#CE9178"))

        comment_fmt = QTextCharFormat()
        comment_fmt.setForeground(QColor("#6A9955"))
        comment_fmt.setFontItalic(True)

        number_fmt = QTextCharFormat()
        number_fmt.setForeground(QColor("#B5CEA8"))

        decorator_fmt = QTextCharFormat()
        decorator_fmt.setForeground(QColor("#DCDCAA"))

        # ---------- single-line rules ----------
        keywords = [
            "False", "None", "True", "and", "as", "assert", "async",
            "await", "break", "class", "continue", "def", "del", "elif",
            "else", "except", "finally", "for", "from", "global", "if",
            "import", "in", "is", "lambda", "nonlocal", "not", "or",
            "pass", "raise", "return", "try", "while", "with", "yield",
        ]
        for kw in keywords:
            self.rules.append((QRegularExpression(rf"\b{kw}\b"), keyword_fmt))

        builtins = [
            "print", "len", "range", "int", "float", "str", "list",
            "dict", "set", "tuple", "sum", "min", "max", "abs",
            "enumerate", "zip", "map", "filter", "sorted", "reversed",
            "open", "input", "type", "isinstance", "round",
        ]
        for b in builtins:
            self.rules.append((QRegularExpression(rf"\b{b}\b"), builtin_fmt))

        self.rules.append((
            QRegularExpression(r"\b[0-9]+\.?[0-9]*([eE][+-]?[0-9]+)?\b"),
            number_fmt,
        ))
        self.rules.append((
            QRegularExpression(r"@\w+(\.\w+)*"),
            decorator_fmt,
        ))
        self.rules.append((
            QRegularExpression(r"#[^\n]*"),
            comment_fmt,
        ))
        self.rules.append((
            QRegularExpression(r"'[^'\\\n]*(\\.[^'\\\n]*)*'"),
            string_fmt,
        ))
        self.rules.append((
            QRegularExpression(r'"[^"\\\n]*(\\.[^"\\\n]*)*"'),
            string_fmt,
        ))

        # ---------- multi-line strings ----------
        self.string_fmt = string_fmt
        self.tri_single = QRegularExpression(r"'''")
        self.tri_double = QRegularExpression(r'"""')

    def highlightBlock(self, text: str) -> None:
        # single-line rules
        for pattern, fmt in self.rules:
            it = pattern.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

        # --- triple-quote state machine ---
        self.setCurrentBlockState(0)

        start = 0
        if self.previousBlockState() != 1:
            m = self.tri_single.match(text)
            m2 = self.tri_double.match(text)
            m = m if m.hasMatch() and (not m2.hasMatch() or m.capturedStart() < m2.capturedStart()) else m2
            if m.hasMatch():
                start = m.capturedStart()
            else:
                start = -1

        while start >= 0:
            # find the matching end quote
            end_single = text.find("'''", start + 3)
            end_double = text.find('"""', start + 3)
            ends = [e for e in (end_single, end_double) if e >= 0]
            if ends:
                end = min(ends) + 3
                length = end - start
                self.setFormat(start, length, self.string_fmt)
                # continue looking for another triple-quote in the rest
                rest = text[start + length:]
                m = self.tri_single.match(rest) if "'''" in rest else self.tri_double.match(rest)
                if m.hasMatch():
                    start = start + length + m.capturedStart()
                else:
                    start = -1
            else:
                # unterminated — color to the end and mark block state
                self.setFormat(start, len(text) - start, self.string_fmt)
                self.setCurrentBlockState(1)
                start = -1