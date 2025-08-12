"""
This script demonstrates how to use Mdstar's tools locally, useful
for testing or development. Here the tools will be operation the mdstar repo itself.
"""

import json
from pprint import pprint

from mdstar.agent import MdstarAgent
from mdstar.config.mdstar_config import MdstarConfig
from mdstar.constants import REPO_ROOT
from mdstar.tools import FindFileTool, FindReferencingSymbolsTool, GetSymbolsOverviewTool, SearchForPatternTool

if __name__ == "__main__":
    agent = MdstarAgent(project=REPO_ROOT, mdstar_config=MdstarConfig(gui_log_window_enabled=False, web_dashboard=False))

    # apply a tool
    find_refs_tool = agent.get_tool(FindReferencingSymbolsTool)
    find_file_tool = agent.get_tool(FindFileTool)
    search_pattern_tool = agent.get_tool(SearchForPatternTool)
    overview_tool = agent.get_tool(GetSymbolsOverviewTool)

    result = agent.execute_task(
        lambda: overview_tool.apply("src/solidlsp/ls.py"),
    )
    pprint(json.loads(result))
