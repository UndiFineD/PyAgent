# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-ovo\ovo\cli\app.py
#!/usr/bin/env python

import os
import runpy
import secrets
import sys

import typer

app = typer.Typer(pretty_exceptions_enable=False)


@app.command(
    name="app",
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
)
def main(
    token: bool = typer.Option(
        False,
        "--token",
        help="Require a token to access the web app. Use set OVO_LOGIN_TOKEN env var for a custom token.",
    ),
    streamlit_run_args: typer.Context = typer.Option(None),
):
    """Run OVO streamlit web application
    \n

    OVO Config variables can be overriden with env vars in this format:
    \n
    OVO_SOME_FIELD_SUBFIELD env var will override some_field.subfield
    \n

    Additional commandline arguments will be passed to `streamlit run`, for example:
    \n
    ovo app --server.address 127.0.0.1 --server.port 5001
    \n

    See `streamlit run --help` for more info.
    """
    from ovo import config, console

    streamlit_script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "run_app.py")
    sys.argv = ["streamlit", "run", streamlit_script_path]
    sys.argv.extend(["--browser.gatherUsageStats", "0"])  # disable streamlit usage stats
    sys.argv.extend(["--server.showEmailPrompt", "0"])  # disable streamlit email prompt (first run)
    sys.argv.extend(["--logger.enableRich", "0"])  # disable rich logging to avoid weird tracebacks
    sys.argv.extend(streamlit_run_args.args)

    if token or os.environ.get("OVO_LOGIN_TOKEN") or config.auth.always_require_token:
        token_value = os.environ.get("OVO_LOGIN_TOKEN", secrets.token_urlsafe(16))
        os.environ["OVO_LOGIN_TOKEN"] = token_value
        console.print(f"OVO Login Token: {token_value}")
    elif config.auth.admin_users and not config.auth.streamlit_auth and not config.auth.hide_admin_warning:
        console.print(
            "[yellow]Warning:[/yellow] Running with admin mode enabled but no auth configured or token set, "
            "anyone who can access the app will be able to run arbitrary commands on the server. "
            "Run with --token to generate a token, use OVO_LOGIN_TOKEN env variable to set custom a login token, "
            "or set auth.always_require_token: true in the OVO config to always generate a token. "
            "Hide this message by setting auth.hide_admin_warning: true in the OVO config."
        )

    runpy.run_module("streamlit", run_name="__main__")


if __name__ == "__main__":
    app()
