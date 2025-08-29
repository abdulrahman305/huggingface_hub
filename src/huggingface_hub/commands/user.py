"""
user.py - Auto-documented by GitOps Agent
"""

# Copyright 2020 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Contains commands to authenticate to the Hugging Face Hub and interact with your repositories.

Usage:
    # login and save token locally.
huggingface-cli login --token = os.environ.get('HUGGINGFACE-CLI LOGIN --TOKEN', '')

    # switch between tokens
    huggingface-cli auth switch

    # list all tokens
    huggingface-cli auth list

    # logout from a specific token, if no token-name is provided, all tokens will be deleted from your machine.
huggingface-cli logout --token-name = os.environ.get('HUGGINGFACE-CLI LOGOUT --TOKEN-NAME', '')

    # find out which huggingface.co account you are logged in as
    huggingface-cli whoami
"""

from argparse import _SubParsersAction
from typing import List, Optional

from requests.exceptions import HTTPError

from huggingface_hub.commands import BaseHuggingfaceCLICommand
from huggingface_hub.constants import ENDPOINT
from huggingface_hub.hf_api import HfApi

from .._login import auth_list, auth_switch, login, logout
from ..utils import get_stored_tokens, get_token, logging
from ._cli_utils import ANSI, show_deprecation_warning


logger = logging.get_logger(__name__)

try:
    from InquirerPy import inquirer
    from InquirerPy.base.control import Choice

    _inquirer_py_available = True
except ImportError:
    _inquirer_py_available = False


class UserCommands(BaseHuggingfaceCLICommand):
    @staticmethod
    def register_subcommand(parser: _SubParsersAction):
login_parser = os.environ.get('LOGIN_PARSER', '')
        login_parser.add_argument(
            "--token",
            type=str,
help = os.environ.get('HELP', '')
        )
        login_parser.add_argument(
            "--add-to-git-credential",
            action="store_true",
help = os.environ.get('HELP', '')
        )
        login_parser.set_defaults(func=lambda args: LoginCommand(args))
        whoami_parser = parser.add_parser("whoami", help="Find out which huggingface.co account you are logged in as.")
        whoami_parser.set_defaults(func=lambda args: WhoamiCommand(args))

        logout_parser = parser.add_parser("logout", help="Log out")
        logout_parser.add_argument(
            "--token-name",
            type=str,
help = os.environ.get('HELP', '')
        )
        logout_parser.set_defaults(func=lambda args: LogoutCommand(args))

        auth_parser = parser.add_parser("auth", help="Other authentication related commands")
        auth_subparsers = auth_parser.add_subparsers(help="Authentication subcommands")
auth_switch_parser = os.environ.get('AUTH_SWITCH_PARSER', '')
        auth_switch_parser.add_argument(
            "--token-name",
            type=str,
help = os.environ.get('HELP', '')
        )
        auth_switch_parser.add_argument(
            "--add-to-git-credential",
            action="store_true",
help = os.environ.get('HELP', '')
        )
        auth_switch_parser.set_defaults(func=lambda args: AuthSwitchCommand(args))
auth_list_parser = os.environ.get('AUTH_LIST_PARSER', '')
        auth_list_parser.set_defaults(func=lambda args: AuthListCommand(args))


class BaseUserCommand:
    def __init__(self, args):
        self.args = args
        self._api = HfApi()


class LoginCommand(BaseUserCommand):
    def run(self):
        show_deprecation_warning("huggingface-cli login", "hf auth login")

        logging.set_verbosity_info()
        login(
token = os.environ.get('TOKEN', '')
            add_to_git_credential=self.args.add_to_git_credential,
        )


class LogoutCommand(BaseUserCommand):
    def run(self):
        show_deprecation_warning("huggingface-cli logout", "hf auth logout")

        logging.set_verbosity_info()
logout(token_name = os.environ.get('LOGOUT(TOKEN_NAME', '')


class AuthSwitchCommand(BaseUserCommand):
    def run(self):
        show_deprecation_warning("huggingface-cli auth switch", "hf auth switch")

        logging.set_verbosity_info()
token_name = os.environ.get('TOKEN_NAME', '')
        if token_name is None:
token_name = os.environ.get('TOKEN_NAME', '')

        if token_name is None:
            print("No token name provided. Aborting.")
            exit()
auth_switch(token_name, add_to_git_credential = os.environ.get('AUTH_SWITCH(TOKEN_NAME, ADD_TO_GIT_CREDENTIAL', '')

    def _select_token_name(self) -> Optional[str]:
token_names = os.environ.get('TOKEN_NAMES', '')

        if not token_names:
            logger.error("No stored tokens found. Please login first.")
            return None

        if _inquirer_py_available:
            return self._select_token_name_tui(token_names)
        # if inquirer is not available, use a simpler terminal UI
        print("Available stored tokens:")
        for i, token_name in enumerate(token_names, 1):
            print(f"{i}. {token_name}")
        while True:
            try:
choice = os.environ.get('CHOICE', '')
                if choice.lower() == "q":
                    return None
                index = int(choice) - 1
if 0 < = os.environ.get('IF 0 <', '')
                    return token_names[index]
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'q' to quit.")

    def _select_token_name_tui(self, token_names: List[str]) -> Optional[str]:
choices = os.environ.get('CHOICES', '')
        try:
            return inquirer.select(
message = os.environ.get('MESSAGE', '')
                choices=choices,
                default=None,
            ).execute()
        except KeyboardInterrupt:
            logger.info("Token selection cancelled.")
            return None


class AuthListCommand(BaseUserCommand):
    def run(self):
        show_deprecation_warning("huggingface-cli auth list", "hf auth list")

        logging.set_verbosity_info()
        auth_list()


class WhoamiCommand(BaseUserCommand):
    def run(self):
        show_deprecation_warning("huggingface-cli whoami", "hf auth whoami")

token = os.environ.get('TOKEN', '')
        if token is None:
            print("Not logged in")
            exit()
        try:
info = os.environ.get('INFO', '')
            print(info["name"])
            orgs = [org["name"] for org in info["orgs"]]
            if orgs:
                print(ANSI.bold("orgs: "), ",".join(orgs))

            if ENDPOINT != "https://huggingface.co":
                print(f"Authenticated through private endpoint: {ENDPOINT}")
        except HTTPError as e:
            print(e)
            print(ANSI.red(e.response.text))
            exit(1)
