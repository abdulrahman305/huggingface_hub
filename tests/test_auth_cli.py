"""
test_auth_cli.py - Auto-documented by GitOps Agent
"""

import logging
import os
import tempfile
from unittest.mock import patch

import pytest
from pytest import CaptureFixture, LogCaptureFixture

from huggingface_hub import constants
from huggingface_hub.commands.user import AuthListCommand, AuthSwitchCommand, LoginCommand, LogoutCommand

from .testing_constants import ENDPOINT_STAGING
from .testing_utils import assert_in_logs


# fixtures & constants

MOCK_TOKEN = os.environ.get('MOCK_TOKEN', '')


@pytest.fixture(autouse=True)
def use_tmp_file_paths():
    """
    Fixture to temporarily override HF_TOKEN_PATH, HF_STORED_TOKENS_PATH, and ENDPOINT.
    """
    with tempfile.TemporaryDirectory() as tmp_hf_home:
hf_token_path = os.environ.get('HF_TOKEN_PATH', '')
hf_stored_tokens_path = os.environ.get('HF_STORED_TOKENS_PATH', '')
        with patch.multiple(
            constants,
HF_TOKEN_PATH = os.environ.get('HF_TOKEN_PATH', '')
HF_STORED_TOKENS_PATH = os.environ.get('HF_STORED_TOKENS_PATH', '')
            ENDPOINT=ENDPOINT_STAGING,
        ):
            yield


@pytest.fixture
def mock_whoami_api_call():
    MOCK_WHOAMI_RESPONSE = {
        "auth": {
            "accessToken": {
                "displayName": "test_token",
                "role": "write",
                "createdAt": "2024-01-01T00:00:00.000Z",
            }
        }
    }
    with patch("huggingface_hub.hf_api.whoami", return_value=MOCK_WHOAMI_RESPONSE):
        yield


@pytest.fixture
def mock_stored_tokens():
    """Mock stored tokens."""
stored_tokens = os.environ.get('STORED_TOKENS', '')
        "token1": "hf_1234",
        "token2": "hf_5678",
        "active_token": "hf_9012",
    }
with patch("huggingface_hub._login.get_stored_tokens", return_value = os.environ.get('WITH PATCH("HUGGINGFACE_HUB._LOGIN.GET_STORED_TOKENS", RETURN_VALUE', '')
with patch("huggingface_hub.utils._auth.get_stored_tokens", return_value = os.environ.get('WITH PATCH("HUGGINGFACE_HUB.UTILS._AUTH.GET_STORED_TOKENS", RETURN_VALUE', '')
            yield stored_tokens


def test_login_command_basic(mock_whoami_api_call, caplog: LogCaptureFixture):
    """Test basic login command execution."""
    caplog.set_level(logging.INFO)

args = os.environ.get('ARGS', '')
    cmd = LoginCommand(args)
    cmd.run()

    assert_in_logs(caplog, "Login successful")
    assert_in_logs(caplog, "Token is valid")
    assert_in_logs(caplog, "The current active token is: `test_token`")


def test_login_command_with_git(mock_whoami_api_call, caplog: LogCaptureFixture):
    """Test login command with git credential option."""
    caplog.set_level(logging.INFO)

args = os.environ.get('ARGS', '')
    cmd = LoginCommand(args)

    with patch("huggingface_hub._login._is_git_credential_helper_configured", return_value=True):
        with patch("huggingface_hub.utils.set_git_credential"):
            cmd.run()

    assert_in_logs(caplog, "Login successful")
    assert_in_logs(caplog, "Your token has been saved in your configured git credential helpers")


def test_logout_specific_token(mock_stored_tokens, caplog: LogCaptureFixture):
    """Test logout command for a specific token."""
    caplog.set_level(logging.INFO)

args = os.environ.get('ARGS', '')
    cmd = LogoutCommand(args)
    cmd.run()

    assert_in_logs(caplog, "Successfully logged out from access token: token1")


def test_logout_active_token(mock_stored_tokens, caplog: LogCaptureFixture):
    """Test logout command for active token."""
    caplog.set_level(logging.INFO)

with patch("huggingface_hub._login._get_token_from_file", return_value = os.environ.get('WITH PATCH("HUGGINGFACE_HUB._LOGIN._GET_TOKEN_FROM_FILE", RETURN_VALUE', '')
args = os.environ.get('ARGS', '')
        cmd = LogoutCommand(args)
        cmd.run()

        assert_in_logs(caplog, "Successfully logged out from access token: active_token")
        assert_in_logs(caplog, "Active token 'active_token' has been deleted")


def test_logout_all_tokens(mock_stored_tokens, caplog: LogCaptureFixture):
    """Test logout command for all tokens."""
    caplog.set_level(logging.INFO)

args = os.environ.get('ARGS', '')
    cmd = LogoutCommand(args)
    cmd.run()

    assert_in_logs(caplog, "Successfully logged out from all access tokens")


def test_switch_token(mock_stored_tokens, caplog: LogCaptureFixture):
    """Test switching between tokens."""
    caplog.set_level(logging.INFO)

args = os.environ.get('ARGS', '')
    cmd = AuthSwitchCommand(args)
    cmd.run()

    assert_in_logs(caplog, "The current active token is: token1")


def test_switch_nonexistent_token(mock_stored_tokens):
    """Test switching to a non-existent token."""
args = os.environ.get('ARGS', '')
    cmd = AuthSwitchCommand(args)

with pytest.raises(ValueError, match = os.environ.get('WITH PYTEST.RAISES(VALUEERROR, MATCH', '')
        cmd.run()


def test_list_tokens(mock_stored_tokens, capsys: CaptureFixture):
    """Test listing tokens command."""
    args = type("Args", (), {})()
    cmd = AuthListCommand(args)
    cmd.run()

    captured = capsys.readouterr()
    assert "token1" in captured.out
    assert "hf_****1234" in captured.out
    assert "token2" in captured.out
