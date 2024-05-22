from typer.testing import CliRunner

from fmconfig.cli import app

runner = CliRunner()


def test_app():
    result = runner.invoke(app)
    assert result.exit_code == 0
    assert "Football Manager" in result.stdout
