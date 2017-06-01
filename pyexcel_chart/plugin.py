from lml.plugin import PluginInfoChain


class ChartPluginChain(PluginInfoChain):
    def add_a_plugin(self, submodule=None, **keywords):
        return PluginInfoChain.add_a_plugin(
            self, 'chart', submodule=submodule, **keywords)
