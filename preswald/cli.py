import os
import click
import sys
import webbrowser
import pkg_resources
from preswald.server import start_server
from preswald.deploy import deploy as deploy_app, stop as stop_app
from preswald.utils import read_template, configure_logging


@click.group()
def cli():
    """
    Preswald CLI - A lightweight framework for interactive data apps.
    """
    pass


@cli.command()
@click.argument("name", default="preswald_project")
def init(name):
    """
    Initialize a new Preswald project.

    This creates a directory with boilerplate files like `hello.py` and `config.toml`.
    """
    try:
        os.makedirs(name, exist_ok=True)
        os.makedirs(os.path.join(name, "images"), exist_ok=True)

        # Copy default branding files from package resources
        import shutil

        default_static_dir = pkg_resources.resource_filename("preswald", "static")
        default_favicon = os.path.join(default_static_dir, "favicon.ico")
        default_logo = os.path.join(default_static_dir, "logo.png")

        shutil.copy2(default_favicon, os.path.join(name, "images", "favicon.ico"))
        shutil.copy2(default_logo, os.path.join(name, "images", "logo.png"))

        file_templates = {
            "hello.py": "hello.py",
            "config.toml": "config.toml",
            "secrets.toml": "secrets.toml",
            ".gitignore": "gitignore",
            "README.md": "readme.md",
        }

        for file_name, template_name in file_templates.items():
            content = read_template(template_name)
            with open(os.path.join(name, file_name), "w") as f:
                f.write(content)

        click.echo(f"Initialized a new Preswald project in '{name}/' 🎉!")
    except Exception as e:
        click.echo(f"Error initializing project: {e} ❌")


@cli.command()
@click.argument("script", default="hello.py")
@click.option("--port", default=8501, help="Port to run the server on.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,
    help="Set the logging level (overrides config file)",
)
def run(script, port, log_level):
    """
    Run a Preswald app.

    By default, it runs the `hello.py` script on localhost:8501.
    """
    if not os.path.exists(script):
        click.echo(f"Error: Script '{script}' not found. ❌")
        return

    config_path = os.path.join(os.path.dirname(script), "config.toml")
    log_level = configure_logging(config_path=config_path, level=log_level)

    url = f"http://localhost:{port}"
    click.echo(f"Running '{script}' on {url} with log level {log_level}  🎉!")

    # Open the URL in the default web browser
    webbrowser.open(url)

    start_server(script=script, port=port)


@cli.command()
@click.argument("script", default="app.py")
@click.option(
    "--target",
    type=click.Choice(["local", "gcp", "aws"], case_sensitive=False),
    default="local",
    help="Target platform for deployment.",
)
@click.option("--port", default=8501, help="Port for deployment.")
@click.option(
    "--log-level",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    default=None,
    help="Set the logging level (overrides config file)",
)
def deploy(script, target, port, log_level):
    """
    Deploy your Preswald app locally.

    This allows you to share the app within your local network.
    """
    try:
        if target == "aws":
            click.echo(
                f"\nWe're working on supporting AWS soon! Please enjoy some ☕ and 🍌 in the meantime"
            )
            return

        if not os.path.exists(script):
            click.echo(f"Error: Script '{script}' not found. ❌")
            return

        config_path = os.path.join(os.path.dirname(script), "config.toml")
        log_level = configure_logging(config_path=config_path, level=log_level)

        url = deploy_app(script, target, port=port)
        click.echo(f"\nDeployment successful! 🎉")
        click.echo(f"Your app is running at: {url}")

    except Exception as e:
        click.echo(f"Error deploying app: {e} ❌")


@cli.command()
@click.argument("script", default="app.py")
def stop(script):
    """
    Stop the currently running deployment.

    This command must be run from the same directory as your Preswald app.
    """
    try:
        if not os.path.exists(script):
            click.echo(f"Error: Script '{script}' not found. ❌")
            return
        stop_app(script)
        click.echo("Deployment stopped successfully. 🛑 ")
    except Exception as e:
        click.echo(f"Error stopping deployment: {e} ❌")
        sys.exit(1)


if __name__ == "__main__":
    cli()
