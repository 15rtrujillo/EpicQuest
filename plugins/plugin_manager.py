from plugins.script_context import ScriptContext


class PluginManager:
    """Object for managing plugins and their context"""

    context: ScriptContext | None = None

    @staticmethod
    def get_script_context() -> ScriptContext:
        """
        Get the script context
        :rtype: ScriptContext
        :return: The script context
        """
        if PluginManager.context is None:
            PluginManager.context = ScriptContext()
        return PluginManager.context
