import pytest

from fmconfig.utils import get_graphics_path, get_system, get_username


class TestGetSystem:
    def test_get_system_mac(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # MacOS system
        expected = "Darwin"
        monkeypatch.setattr("platform.system", lambda: expected)

        # When
        # Getting the system
        actual = get_system()

        # Then
        # It is as expected
        assert actual == expected

    def test_get_system_unsupported(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # Windows system
        monkeypatch.setattr("platform.system", lambda: "Windows")

        # When
        # Getting the system

        # Then
        # An OSError should be raised
        with pytest.raises(OSError, match="Unsupported operating system"):
            get_system()

class TestGetUsername:
    def test_get_username_from_env(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # A username as environment variable
        expected = "testuser"
        monkeypatch.setenv("USER", expected)

        # When
        # Calling the function
        actual = get_username()

        # Then
        # It is as expected
        assert actual == expected

    def test_get_username_from_pwd(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # A username as environment variable
        expected = "testuser"
        monkeypatch.delenv("USER", raising=False)
        monkeypatch.setattr("os.geteuid", lambda: 1000)
        monkeypatch.setattr("pwd.getpwuid", lambda x: type('p', (object,), {'pw_name': expected}))

        # When
        # Calling the function
        actual = get_username()

        # Then
        # It is as expected
        assert actual == expected

class TestGetGraphicPath:
    def test_get_graphics_path_mac(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # MacOS system and a username
        monkeypatch.setattr("platform.system", lambda: "Darwin")
        monkeypatch.setenv("USER", "testuser")

        # When
        # Calling the function to get the graphics path
        actual = get_graphics_path()

        # Then
        # It is as expected
        expected = "/Users/testuser/Library/Application Support/Sports Interactive/Football Manager 2023/graphics"
        assert actual == expected

    def test_get_graphics_path_unsupported(self, monkeypatch: pytest.MonkeyPatch):
        # Given
        # Windows system
        monkeypatch.setattr("platform.system", lambda: "Windows")

        # When
        # Calling the function to get the graphics path

        # Then
        # An OSError should be raised
        with pytest.raises(OSError, match="Unsupported operating system"):
            get_graphics_path()
