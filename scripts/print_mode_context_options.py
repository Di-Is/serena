from mdstar.config.context_mode import MdstarAgentContext, MdstarAgentMode

if __name__ == "__main__":
    print("---------- Available modes: ----------")
    for mode_name in MdstarAgentMode.list_registered_mode_names():
        mode = MdstarAgentMode.load(mode_name)
        mode.print_overview()
        print("\n")
    print("---------- Available contexts: ----------")
    for context_name in MdstarAgentContext.list_registered_context_names():
        context = MdstarAgentContext.load(context_name)
        context.print_overview()
        print("\n")
