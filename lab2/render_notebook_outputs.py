import ast
import base64
import io
import sys
import traceback
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import nbformat


NOTEBOOK_PATH = Path(__file__).resolve().parent / "lab2_notebook.ipynb"


def format_result(value):
    data = {"text/plain": repr(value)}

    if hasattr(value, "to_html"):
        try:
            data["text/html"] = value.to_html()
        except Exception:
            pass

    return nbformat.v4.new_output("execute_result", data=data, execution_count=None)


def make_stream_output(name, text):
    if not text:
        return None
    return nbformat.v4.new_output("stream", name=name, text=text)


def capture_figures(plt_module):
    outputs = []
    for fig_num in list(plt_module.get_fignums()):
        fig = plt_module.figure(fig_num)
        buffer = io.BytesIO()
        fig.savefig(buffer, format="png", bbox_inches="tight")
        png_data = base64.b64encode(buffer.getvalue()).decode("ascii")
        outputs.append(
            nbformat.v4.new_output(
                "display_data",
                data={"image/png": png_data},
                metadata={},
            )
        )
        plt_module.close(fig)
    return outputs


def execute_cell(source, ns):
    module_ast = ast.parse(source)
    last_expr = None

    if module_ast.body and isinstance(module_ast.body[-1], ast.Expr):
        last_expr = ast.Expression(module_ast.body.pop().value)

    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    outputs = []

    plt_module = ns.get("plt")
    original_show = None

    if plt_module is not None:
        original_show = plt_module.show

        def patched_show(*args, **kwargs):
            outputs.extend(capture_figures(plt_module))

        plt_module.show = patched_show

    try:
        with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
            if module_ast.body:
                exec(compile(module_ast, "<notebook-cell>", "exec"), ns, ns)
            if last_expr is not None:
                value = eval(compile(last_expr, "<notebook-cell>", "eval"), ns, ns)
                if value is not None:
                    outputs.append(format_result(value))

        plt_module = ns.get("plt")
        if plt_module is not None:
            outputs.extend(capture_figures(plt_module))

    except Exception:
        tb = traceback.format_exc()
        outputs.append(
            nbformat.v4.new_output(
                "error",
                ename=type(sys.exc_info()[1]).__name__,
                evalue=str(sys.exc_info()[1]),
                traceback=tb.splitlines(),
            )
        )
        raise
    finally:
        if original_show is not None:
            plt_module.show = original_show

    stdout_output = make_stream_output("stdout", stdout_buffer.getvalue())
    stderr_output = make_stream_output("stderr", stderr_buffer.getvalue())

    final_outputs = []
    if stdout_output is not None:
        final_outputs.append(stdout_output)
    if stderr_output is not None:
        final_outputs.append(stderr_output)
    final_outputs.extend(outputs)
    return final_outputs


def main():
    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
    namespace = {}
    exec_count = 1

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        cell.outputs = execute_cell(cell.source, namespace)
        cell.execution_count = exec_count
        exec_count += 1

    nbformat.write(nb, NOTEBOOK_PATH)
    print(f"rendered_outputs_into={NOTEBOOK_PATH}")


if __name__ == "__main__":
    main()
