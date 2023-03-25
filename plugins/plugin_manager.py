from plugins.script_context import ScriptContext


class PluginManager:

    context: ScriptContext | None = None

    @staticmethod
    def get_script_context() -> ScriptContext:
        """Get the script context"""
        if PluginManager.context is None:
            PluginManager.context = ScriptContext()
        return PluginManager.context
