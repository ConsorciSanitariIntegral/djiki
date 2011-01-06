import re
from creole import Parser
from creole.html_emitter import HtmlEmitter
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from . import models

class DjikiHtmlEmitter(HtmlEmitter):
	image_params_re = re.compile(r'^(?:(?P<size>[0-9]+x[0-9]+)(?:\||$))?(?P<title>.*)$')

	def image_emit(self, node):
		target = node.content
		text = self.get_text(node)
		m = self.link_rules.addr_re.match(target)
		try:
			ctx = self.image_params_re.match(text).groupdict()
		except AttributeError:
			ctx = {}
		if m:
			if m.group('extern_addr'):
				ctx['url'] = self.attr_escape(target)
			elif m.group('inter_wiki'):
				raise NotImplementedError
		else:
			try:
				image = models.Image.objects.get(name=target)
				ctx['image'] = image
			except models.Image.DoesNotExist:
				pass
		return render_to_string('djiki/parser/image.html', ctx)

def render(src):
	doc = Parser(src).parse()
	return DjikiHtmlEmitter(doc).emit().encode('utf-8', 'ignore')
