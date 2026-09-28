import sys
import copy
import io

from .snapshot import Snapshot


USER_FILENAME = "<user_code>"
MAX_SNAPSHOTS = 8000


# ----------------------------------------------------------------------
# safe helpers for numpy / arbitrary objects
# ----------------------------------------------------------------------
def _is_ambiguous(value) -> bool:
    """True for numpy arrays / pandas that can't be used with `==`."""
    mod = type(value).__module__ or ""
    return mod.startswith("numpy") or mod.startswith("pandas")


def _safe_equal(a, b) -> bool:
    """Compare two arbitrary values without raising on numpy arrays."""
    try:
        if _is_ambiguous(a) or _is_ambiguous(b):
            # cheap identity check + shape/dtype string comparison
            try:
                if a is b:
                    return True
                if type(a) is not type(b):
                    return False
                if hasattr(a, "shape") and getattr(a, "shape", None) != getattr(b, "shape", None):
                    return False
                if hasattr(a, "dtype") and getattr(a, "dtype", None) != getattr(b, "dtype", None):
                    return False
                # element-wise equality then .all()
                try:
                    return bool((a == b).all())
                except Exception:
                    return repr(a) == repr(b)
            except Exception:
                return False
        return bool(a == b)
    except Exception:
        return False


def _safe_repr(value) -> str:
    """Short, readable repr — numpy arrays become `array shape=(..)`."""
    try:
        mod = type(value).__module__ or ""
        if mod.startswith("numpy"):
            shape = getattr(value, "shape", None)
            dtype = getattr(value, "dtype", None)
            if shape is not None:
                return f"array(shape={tuple(shape)}, dtype={dtype})"
        if isinstance(value, (list, tuple, dict, set)):
            r = repr(value)
            return r if len(r) <= 120 else r[:117] + "..."
        r = repr(value)
        return r if len(r) <= 120 else r[:117] + "..."
    except Exception:
        return "<unrepresentable>"


class PythonDebugger:
    def __init__(self, code: str):
        self.code = code
        self.lines = code.splitlines()
        self.snapshots: list[Snapshot] = []
        self.current_index = -1
        self.error: str | None = None
        self.globals: dict = {"__name__": "__main__"}
        self._trace_events()

    # ------------------------------------------------------------------
    # Tracing
    # ------------------------------------------------------------------
    def _trace_events(self) -> None:
        step_counter = 0
        last_seen: dict[str, object] = {}
        line_stdout = io.StringIO()
        real_stdout = sys.stdout
        hit_limit = False
        pending_snapshot: Snapshot | None = None

        def snapshot_vars(frame):
            result: dict = {}
            for name, value in frame.f_locals.items():
                if name.startswith("__"):
                    continue
                result[name] = self._safe_copy(value)
            for name, value in frame.f_globals.items():
                if name.startswith("__") or name in result:
                    continue
                if name in {"sys", "copy", "io", "PythonDebugger"}:
                    continue
                result[name] = self._safe_copy(value)
            return result

        def flush_pending():
            """Attach captured stdout to the last pending snapshot."""
            nonlocal pending_snapshot, line_stdout
            if pending_snapshot is not None:
                pending_snapshot.stdout = line_stdout.getvalue()
                pending_snapshot = None

        def tracer(frame, event, arg):
            nonlocal step_counter, last_seen, line_stdout, hit_limit, pending_snapshot

            if frame.f_code.co_filename != USER_FILENAME:
                return tracer

            if event == "line":
                # ---- 1) finalize previous line: flush stdout to it ----
                flush_pending()

                if step_counter >= MAX_SNAPSHOTS:
                    hit_limit = True
                    return None

                step_counter += 1
                line_stdout = io.StringIO()
                sys.stdout = line_stdout

                vars_now = snapshot_vars(frame)

                changed = {}
                for k, v in vars_now.items():
                    if k not in last_seen or not _safe_equal(last_seen[k], v):
                        changed[k] = v

                line_no = frame.f_lineno
                src = (
                    self.lines[line_no - 1].rstrip()
                    if 1 <= line_no <= len(self.lines)
                    else ""
                )

                snap = Snapshot(
                    step=step_counter,
                    line_number=line_no,
                    event="line",
                    source_line=src,
                    stdout="",
                    changed_vars=changed,
                    variables=vars_now,
                )
                self.snapshots.append(snap)
                pending_snapshot = snap

                last_seen = vars_now

            elif event == "return":
                # end of the whole user frame — flush last stdout
                flush_pending()
                sys.stdout = real_stdout

            elif event == "exception":
                exc_type, exc_value, _ = arg
                self.error = f"{exc_type.__name__}: {exc_value}"

            return tracer

        try:
            compiled = compile(self.code, USER_FILENAME, "exec")
        except SyntaxError as e:
            self.error = f"SyntaxError: {e}"
            return

        old_trace = sys.gettrace()
        try:
            sys.settrace(tracer)
            exec(compiled, self.globals, self.globals)
        except Exception as e:  # noqa: BLE001
            self.error = f"{type(e).__name__}: {e}"
        finally:
            sys.settrace(old_trace)
            sys.stdout = real_stdout
            # final flush for the very last line
            flush_pending()

        if hit_limit:
            self.error = (
                f"Trace stopped after {MAX_SNAPSHOTS} steps "
                f"(possible runaway loop or heavy library calls)."
            )

        self.current_index = -1

    @staticmethod
    def _safe_copy(value):
        try:
            return copy.deepcopy(value)
        except Exception:  # noqa: BLE001
            try:
                return repr(value)
            except Exception:  # noqa: BLE001
                return "<unrepresentable>"

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
    def next_step(self):
        if not self.snapshots:
            return None
        if self.current_index < len(self.snapshots) - 1:
            self.current_index += 1
            return self.snapshots[self.current_index]
        return None

    def previous_step(self):
        if not self.snapshots:
            return None
        if self.current_index > 0:
            self.current_index -= 1
            return self.snapshots[self.current_index]
        return None

    def restart(self) -> None:
        self.current_index = -1

    def current(self):
        if 0 <= self.current_index < len(self.snapshots):
            return self.snapshots[self.current_index]
        return None

    # expose for UI to use safe repr in the variables panel
    safe_repr = staticmethod(_safe_repr)