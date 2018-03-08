import aiohttp_jinja2
import jinja2


class View:

    def __init__(self, app_name, webapp):
        self.app_name = app_name
        self.webapp = webapp


class TemplateView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        aiohttp_jinja2.setup(
            self.webapp, 
            loader=jinja2.PackageLoader(self.app_name, 'templates')
        )
