"""
Basic integration tests for the Markdown language server functionality.

These tests validate the functionality of the language server APIs
like request_document_symbols using the Markdown test repository.
"""

import pytest

from solidlsp import SolidLanguageServer
from solidlsp.ls_config import Language


@pytest.mark.markdown
class TestMarkdownLanguageServerBasics:
    """Test basic functionality of the Markdown language server."""

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_language_server_initialization(self, language_server: SolidLanguageServer) -> None:
        """Test that Markdown language server can be initialized successfully."""
        assert language_server is not None
        assert language_server.language == Language.MARKDOWN

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_request_document_symbols(self, language_server: SolidLanguageServer) -> None:
        """Test request_document_symbols for Markdown files."""
        # Test getting symbols from README.md
        all_symbols, root_symbols = language_server.request_document_symbols("README.md", include_body=False)

        # Extract heading symbols (LSP Symbol Kind 15 = String, but Marksman uses different kinds for headers)
        # Marksman typically uses SymbolKind.Namespace (3) or Module (2) for headers
        # Get symbol names
        symbol_names = [symbol["name"] for symbol in all_symbols]

        # Check for main headings from README.md
        expected_headings = [
            "Project Documentation",
            "Table of Contents",
            "Introduction",
            "Installation",
            "Usage",
            "API Reference",
            "Contributing",
            "License",
        ]

        for heading in expected_headings:
            assert heading in symbol_names, f"Should find heading '{heading}'"

        # Verify hierarchical structure - check for nested headings
        assert "Background" in symbol_names, "Should find sub-heading 'Background'"
        assert "Goals" in symbol_names, "Should find sub-heading 'Goals'"
        assert "Prerequisites" in symbol_names, "Should find sub-heading 'Prerequisites'"

        # Check that we have a reasonable number of symbols
        assert len(all_symbols) >= 15, f"Should find at least 15 symbols, found {len(all_symbols)}"

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_hierarchical_symbols(self, language_server: SolidLanguageServer) -> None:
        """Test that Markdown symbols have proper hierarchical structure."""
        # Test with features.md which has various heading levels
        all_symbols, root_symbols = language_server.request_document_symbols("features.md", include_body=False)

        # Get symbol names
        symbol_names = [symbol["name"] for symbol in all_symbols]

        # Check for various feature headings
        expected_features = [
            "Markdown Features",
            "Basic Formatting",
            "Lists",
            "Tables",
            "Code Blocks",
            "Links and Images",
            "Blockquotes",
        ]

        for feature in expected_features:
            assert feature in symbol_names, f"Should find feature heading '{feature}'"

        # Check for sub-sections
        assert "Unordered List" in symbol_names, "Should find 'Unordered List' sub-heading"
        assert "Ordered List" in symbol_names, "Should find 'Ordered List' sub-heading"
        assert "Task List" in symbol_names, "Should find 'Task List' sub-heading"

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_document_symbols_with_body(self, language_server: SolidLanguageServer) -> None:
        """Test request_document_symbols with body extraction."""
        # Test with include_body=True on CONTRIBUTING.md
        all_symbols, root_symbols = language_server.request_document_symbols("CONTRIBUTING.md", include_body=True)

        # Find a specific heading and check if it has body content
        contributing_symbol = next((sym for sym in all_symbols if sym["name"] == "Contributing Guidelines"), None)

        assert contributing_symbol is not None, "Should find 'Contributing Guidelines' heading"

        # If body is included, check that it contains expected content
        if "body" in contributing_symbol:
            body = contributing_symbol["body"]
            # The body should contain the heading and some content
            assert "Contributing Guidelines" in body or "#" in body, "Body should contain the heading"

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_code_block_symbols(self, language_server: SolidLanguageServer) -> None:
        """Test that code blocks are detected as symbols if supported."""
        # Test with features.md which has multiple code blocks
        all_symbols, root_symbols = language_server.request_document_symbols("features.md", include_body=False)

        # Look for code block related symbols
        # Different Markdown LSPs may or may not include code blocks as symbols
        # This is more of an exploratory test to understand capabilities
        symbol_names = [symbol["name"] for symbol in all_symbols]

        # At minimum, we should find the section headings that contain code blocks
        assert "Code Blocks" in symbol_names, "Should find 'Code Blocks' heading"

        # Check if sub-headings for code examples are found
        code_sections = ["Python Example", "JavaScript Example", "YAML Example"]
        found_code_sections = [s for s in code_sections if s in symbol_names]

        # We expect to find at least some of these
        assert len(found_code_sections) > 0, f"Should find at least one code section heading, found: {found_code_sections}"

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_link_references(self, language_server: SolidLanguageServer) -> None:
        """Test that internal links and references are handled."""
        # This test verifies the server can handle files with links
        # The actual link validation would be done through goto_definition
        all_symbols, root_symbols = language_server.request_document_symbols("README.md", include_body=False)

        # Check that sections referenced by links exist
        symbol_names = [symbol["name"] for symbol in all_symbols]

        # These are sections that are linked to in the README
        linked_sections = ["Introduction", "Installation", "Usage", "API Reference", "Contributing"]

        for section in linked_sections:
            assert section in symbol_names, f"Should find linked section '{section}'"

    @pytest.mark.parametrize("language_server", [Language.MARKDOWN], indirect=True)
    def test_markdown_table_detection(self, language_server: SolidLanguageServer) -> None:
        """Test that tables are properly handled in the document structure."""
        # Test with features.md which has tables
        all_symbols, root_symbols = language_server.request_document_symbols("features.md", include_body=False)

        symbol_names = [symbol["name"] for symbol in all_symbols]

        # Check that the Tables section and its subsections are found
        assert "Tables" in symbol_names, "Should find 'Tables' heading"
        assert "Complex Table" in symbol_names, "Should find 'Complex Table' sub-heading"
