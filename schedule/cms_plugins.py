from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models.events import EventPluginModel


class EventPlugin(CMSPluginBase):
    model = EventPluginModel  # Model where data about this plugin is saved
    name = _("Event Plugin")  # Name of the plugin
    render_template = "event/plugin.html"  # template to render

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context

plugin_pool.register_plugin(EventPlugin)  # register the plugin
plugin_pool.unregister_plugin(EventPlugin)  # register the plugin