"""
Provides Markdown specific instantiation of the LanguageServer class using Marksman.
Contains various configurations and settings specific to Markdown documents.
"""

import logging
import os
import pathlib
import platform
import threading
import urllib.request
from typing import cast

from solidlsp.ls import SolidLanguageServer
from solidlsp.ls_config import LanguageServerConfig
from solidlsp.ls_logger import LanguageServerLogger
from solidlsp.lsp_protocol_handler.lsp_types import InitializeParams
from solidlsp.settings import SolidLSPSettings


class MarkdownLanguageServer(SolidLanguageServer):
    """
    Provides Markdown specific instantiation of the LanguageServer class using Marksman.
    Marksman is a language server for Markdown that provides document symbols, completions,
    goto definition, find references, rename refactoring, and diagnostics.
    """

    def __init__(
        self,
        config: LanguageServerConfig,
        logger: LanguageServerLogger,
        repository_root_path: str,
        solidlsp_settings: SolidLSPSettings | None = None,
    ):
        # Setup runtime dependencies first
        language_server_command = self._setup_runtime_dependencies(logger, config, solidlsp_settings or SolidLSPSettings())

        # Enable LSP trace for debugging
        trace_lsp = os.environ.get("TRACE_MARKSMAN_LSP", "false").lower() == "true"

        # Update config with the command
        config.language_server_command = language_server_command
        config.trace_lsp_communication = trace_lsp or config.trace_lsp_communication

        # Create ProcessLaunchInfo
        from solidlsp.lsp_protocol_handler.server import ProcessLaunchInfo

        process_launch_info = ProcessLaunchInfo(cmd=language_server_command, env={}, cwd=repository_root_path)

        super().__init__(config, logger, repository_root_path, process_launch_info, "markdown", solidlsp_settings or SolidLSPSettings())

        self.server_ready = threading.Event()
        self.completions_available = threading.Event()

    @classmethod
    def _setup_runtime_dependencies(
        cls, logger: LanguageServerLogger, config: LanguageServerConfig, solidlsp_settings: SolidLSPSettings
    ) -> str:
        """
        Setup runtime dependencies for Marksman Language Server and return the command to start the server.
        Downloads the appropriate binary for the platform if not already present.
        """
        marksman_dir = os.path.join(cls.ls_resources_dir(solidlsp_settings), "marksman")
        os.makedirs(marksman_dir, exist_ok=True)

        # Determine platform-specific binary name and download URL
        system = platform.system().lower()
        machine = platform.machine().lower()

        if system == "darwin":
            # The 2024-12-18 release has a universal binary for macOS
            binary_name = "marksman-macos"
            download_url = "https://github.com/artempyanykh/marksman/releases/download/2024-12-18/marksman-macos"
        elif system == "linux":
            if "arm" in machine or "aarch64" in machine:
                binary_name = "marksman-linux-arm64"
                download_url = "https://github.com/artempyanykh/marksman/releases/download/2024-12-18/marksman-linux-arm64"
            else:
                binary_name = "marksman-linux-x64"
                download_url = "https://github.com/artempyanykh/marksman/releases/download/2024-12-18/marksman-linux-x64"
        elif system == "windows":
            binary_name = "marksman.exe"
            download_url = "https://github.com/artempyanykh/marksman/releases/download/2024-12-18/marksman.exe"
        else:
            raise RuntimeError(f"Unsupported platform: {system} {machine}")

        marksman_executable_path = os.path.join(marksman_dir, binary_name)

        # Download if not exists
        if not os.path.exists(marksman_executable_path):
            logger.log(f"Marksman executable not found at {marksman_executable_path}. Downloading...", logging.INFO)

            try:
                # Download the binary
                urllib.request.urlretrieve(download_url, marksman_executable_path)

                # Make executable on Unix-like systems
                if system != "windows":
                    os.chmod(marksman_executable_path, 0o755)

                logger.log("Marksman downloaded and installed successfully", logging.INFO)
            except Exception as e:
                raise RuntimeError(f"Failed to download Marksman: {e}")

        if not os.path.exists(marksman_executable_path):
            raise FileNotFoundError(
                f"Marksman executable not found at {marksman_executable_path}, something went wrong with the installation."
            )

        return marksman_executable_path

    @staticmethod
    def _get_initialize_params(repository_absolute_path: str) -> InitializeParams:
        """
        Returns the initialize params for the Marksman Language Server.
        """
        root_uri = pathlib.Path(repository_absolute_path).as_uri()
        initialize_params = {
            "processId": os.getpid(),
            "rootPath": repository_absolute_path,
            "rootUri": root_uri,
            "capabilities": {
                "textDocument": {
                    "synchronization": {
                        "dynamicRegistration": True,
                        "willSave": True,
                        "willSaveWaitUntil": True,
                        "didSave": True,
                    },
                    "completion": {
                        "dynamicRegistration": True,
                        "completionItem": {
                            "snippetSupport": True,
                            "documentationFormat": ["markdown", "plaintext"],
                        },
                    },
                    "hover": {
                        "dynamicRegistration": True,
                        "contentFormat": ["markdown", "plaintext"],
                    },
                    "definition": {"dynamicRegistration": True},
                    "references": {"dynamicRegistration": True},
                    "documentSymbol": {
                        "dynamicRegistration": True,
                        "hierarchicalDocumentSymbolSupport": True,
                        "symbolKind": {"valueSet": list(range(1, 27))},
                    },
                    "rename": {"dynamicRegistration": True},
                    "foldingRange": {"dynamicRegistration": True},
                },
                "workspace": {
                    "workspaceFolders": True,
                    "didChangeConfiguration": {"dynamicRegistration": True},
                    "symbol": {"dynamicRegistration": True},
                    "executeCommand": {"dynamicRegistration": True},
                },
            },
            "workspaceFolders": [
                {
                    "uri": root_uri,
                    "name": os.path.basename(repository_absolute_path),
                }
            ],
        }
        return cast(InitializeParams, initialize_params)

    def _start_server(self):
        """
        Starts the Marksman Language Server, waits for the server to be ready and yields the LanguageServer instance.
        """

        def do_nothing(params):
            return

        def window_log_message(msg):
            self.logger.log(f"LSP: window/logMessage: {msg}", logging.INFO)
            # Marksman is typically ready immediately after initialization
            self.server_ready.set()
            self.completions_available.set()

        self.server.on_notification("window/logMessage", window_log_message)
        self.server.on_notification("$/progress", do_nothing)
        self.server.on_notification("textDocument/publishDiagnostics", do_nothing)

        self.logger.log("Starting Marksman server process", logging.INFO)
        self.server.start()

        initialize_params = self._get_initialize_params(self.repository_root_path)
        self.logger.log(
            "Sending initialize request from LSP client to LSP server and awaiting response",
            logging.INFO,
        )
        init_response = self.server.send.initialize(initialize_params)
        self.logger.log(f"Received initialize response from Marksman server: {init_response}", logging.DEBUG)

        # Verify capabilities
        capabilities = init_response.get("capabilities", {})

        # Check for essential capabilities
        assert "completionProvider" in capabilities, "Marksman should support completions"
        assert "definitionProvider" in capabilities, "Marksman should support goto definition"
        assert "referencesProvider" in capabilities, "Marksman should support find references"
        assert "documentSymbolProvider" in capabilities, "Marksman should support document symbols"
        assert "renameProvider" in capabilities, "Marksman should support rename"

        self.logger.log("Marksman server capabilities verified", logging.INFO)

        self.server.notify.initialized({})

        # Marksman is typically ready immediately
        self.server_ready.set()
        self.completions_available.set()
        self.logger.log("Marksman server initialization complete", logging.INFO)

    def is_ignored_dirname(self, dirname: str) -> bool:
        """
        Markdown-specific directories to ignore.
        """
        # Common directories to ignore in documentation projects
        ignored_dirs = {".git", ".github", "node_modules", "_site", ".jekyll-cache", ".obsidian"}
        return dirname in ignored_dirs or dirname.startswith(".")
