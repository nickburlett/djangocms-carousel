from cms.api import add_plugin
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from django.test import TestCase
from django.test.client import RequestFactory

from cmsplugin_carousel.cms_plugins import CMSCarouselPlugin
from cmsplugin_carousel.models import CarouselPlugin


class CMSCarouselPluginTest(TestCase):
    def test_plugin_context(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            CMSCarouselPlugin,
            'en',
        )
        plugin_instance = model_instance.get_plugin_class_instance()
        context = plugin_instance.render({}, model_instance, None)
        self.assertIn('rotate_interval', context)
        self.assertEqual(context['rotate_interval'], 5000)

    def test_plugin_html(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            CMSCarouselPlugin,
            'en',
        )
        renderer = ContentRenderer(request=RequestFactory())
        html = renderer.render_plugin(model_instance, {})

        self.assertIn('id="carousel_1"', html)
        self.assertIn('data-interval="5000"', html)
        self.assertIn('<ol class="carousel-indicators">', html)
        self.assertIn('<div class="carousel-inner">', html)

    def test_plugin_stringified(self):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            CMSCarouselPlugin,
            'en',
        )
        self.assertEqual(str(model_instance), str(model_instance.pk))

        model_instance.title = "Test Plugin"

        self.assertEqual(str(model_instance), "Test Plugin")
