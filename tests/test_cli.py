import pytest
from typer.testing import CliRunner

from fmconfig.cli import app

runner = CliRunner()


def test_app(monkeypatch: pytest.MonkeyPatch):
    # Given
    # MacOS system
    expected = "Darwin"
    monkeypatch.setattr("platform.system", lambda: expected)

    # When
    # Invoking the app
    result = runner.invoke(app)

    # Then
    # It should run as expected
    assert result.exit_code == 0
    assert "Football Manager" in result.stdout
