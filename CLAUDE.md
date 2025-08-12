# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

**Essential Commands (use these exact commands):**
- `mise run format` - Format code with RUFF - ONLY allowed formatting command
- `mise run type-check` - Run mypy type checking - ONLY allowed type checking command  
- `mise run test` - Run tests
- `mise run lint` - Check code style without fixing

**Test Markers:**
Available pytest markers for selective testing:
- `markdown` - for Markdown language server tests
- `snapshot` - for symbolic editing operation tests

**Project Management:**
- `uv run mdstar-mcp-server` - Start MCP server from project root
- `uv run index-project` - Index project for faster tool performance

**Always run format, type-check, and test before completing any task.**

## Architecture Overview

Mdstar is a dual-layer coding agent toolkit:

### Core Components

**1. MdstarAgent (`src/mdstar/agent.py`)**
- Central orchestrator managing projects, tools, and user interactions
- Coordinates language servers, memory persistence, and MCP server interface
- Manages tool registry and context/mode configurations

**2. SolidLanguageServer (`src/solidlsp/ls.py`)**  
- Unified wrapper around Language Server Protocol (LSP) implementations
- Provides language-agnostic interface for symbol operations
- Handles caching, error recovery, and multiple language server lifecycle

**3. Tool System (`src/mdstar/tools/`)**
- **file_tools.py** - File system operations, search, regex replacements
- **symbol_tools.py** - Language-aware symbol finding, navigation, editing
- **memory_tools.py** - Project knowledge persistence and retrieval
- **config_tools.py** - Project activation, mode switching
- **workflow_tools.py** - Onboarding and meta-operations

**4. Configuration System (`src/mdstar/config/`)**
- **Contexts** - Define tool sets for different environments (desktop-app, agent, ide-assistant)
- **Modes** - Operational patterns (planning, editing, interactive, one-shot)
- **Projects** - Per-project settings and language server configs

### Language Support Architecture

Each supported language has:
1. **Language Server Implementation** in `src/solidlsp/language_servers/`
2. **Runtime Dependencies** - Automatic language server downloads when needed
3. **Test Repository** in `test/resources/repos/<language>/`
4. **Test Suite** in `test/solidlsp/<language>/`

### Memory & Knowledge System

- **Markdown-based storage** in `.mdstar/memories/` directories
- **Project-specific knowledge** persistence across sessions
- **Contextual retrieval** based on relevance
- **Onboarding support** for new projects

## Development Patterns

### Adding New Languages
1. Create language server class in `src/solidlsp/language_servers/`
2. Add to Language enum in `src/solidlsp/ls_config.py` 
3. Update factory method in `src/solidlsp/ls.py`
4. Create test repository in `test/resources/repos/<language>/`
5. Write test suite in `test/solidlsp/<language>/`
6. Add pytest marker to `pyproject.toml`

### Adding New Tools
1. Inherit from `Tool` base class in `src/mdstar/tools/tools_base.py`
2. Implement required methods and parameter validation
3. Register in appropriate tool registry
4. Add to context/mode configurations

### Testing Strategy
- Language-specific tests use pytest markers
- Symbolic editing operations have snapshot tests
- Integration tests in `test_mdstar_agent.py`
- Test repositories provide realistic symbol structures

## Configuration Hierarchy

Configuration is loaded from (in order of precedence):
1. Command-line arguments to `mdstar-mcp-server`
2. Project-specific `.mdstar/project.yml`
3. User config `~/.mdstar/mdstar_config.yml`
4. Active modes and contexts

## Key Implementation Notes

- **Symbol-based editing** - Uses LSP for precise code manipulation
- **Caching strategy** - Reduces language server overhead
- **Error recovery** - Automatic language server restart on crashes
- **Markdown support** - Specialized for Markdown with Marksman LSP integration
- **MCP protocol** - Exposes tools to AI agents via Model Context Protocol
- **Async operation** - Non-blocking language server interactions

## Working with the Codebase

- Project uses Python 3.11 with `uv` for dependency management
- Strict typing with mypy, formatted with black + ruff
- Language servers run as separate processes with LSP communication
- Memory system enables persistent project knowledge
- Context/mode system allows workflow customization

## Creating Markdown-specific MCP Server from Mdstar

### Migration Steps for Creating a Markdown MCP Server

When creating a specialized Markdown MCP server based on Mdstar, follow these steps:

#### 1. Code Removal Phase
Start by removing unnecessary code for languages other than Markdown:

**Language Servers to Remove:**
- `src/solidlsp/language_servers/` - Keep only `markdown_language_server.py`
- Remove all language servers except `markdown_language_server.py`

**Language Enum Cleanup:**
- In `src/solidlsp/ls_config.py`: Keep only `MARKDOWN` in the Language enum
- Remove all other language entries

**Factory Method Simplification:**
- In `src/solidlsp/ls.py`: Simplify `SolidLanguageServer.create()` to only handle Markdown
- Remove all conditional branches for other languages

**Test Cleanup:**
- Remove `test/resources/repos/` for all languages except markdown
- Remove `test/solidlsp/` test directories except markdown tests

**Tool Removal:**
- Remove language-specific symbolic editing tools that don't apply to Markdown
- Keep file operations and search tools

#### 2. Markdown-specific Enhancements

**Add Markdown-specific Tools:**
- TOC generation tool
- Heading level adjustment tool
- Link validation tool
- Code block extraction tool
- Front matter parsing tool
- Cross-reference management tool

**Optimize for Markdown:**
- Remove caching mechanisms designed for compiled languages
- Simplify symbol retrieval for flat Markdown structure
- Add Markdown-specific symbol kinds (headings, links, code blocks)

#### 3. Configuration Simplification

**Remove Multi-language Support:**
- Simplify project configuration to assume Markdown-only projects
- Remove language detection logic
- Remove language-specific settings

**Streamline Contexts:**
- Create Markdown-specific contexts (documentation, wiki, notes)
- Remove programming language contexts

#### 4. Dependency Reduction

**Remove Unnecessary Dependencies:**
- Remove language server dependencies for other languages
- Keep only Marksman and potentially other Markdown LSPs
- Remove compilation/build tool integrations

#### 5. Testing Strategy

**Markdown-focused Tests:**
- Test heading extraction
- Test link resolution
- Test TOC generation
- Test code block identification
- Test front matter parsing

### Important Notes

**Preserve Core Infrastructure:**
- Keep the MCP server framework
- Keep the LSP communication layer
- Keep the basic tool system architecture

**Marksman Integration Issues:**
- Be aware that Marksman's document symbol support may vary
- Current issue: When used in multi-language projects, wrong language server may process .md files
- Solution: Dedicated Markdown MCP ensures Marksman is always used for .md files
