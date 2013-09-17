from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.safestring import mark_safe

from utils import edit_string_for_tags


class TagAutocomplete(forms.TextInput):
	input_type = 'text'
	
	def render(self, name, value, attrs=None):
		list_view = '/dynamic/autocomplete/1/taggable/'
		if value is not None and not isinstance(value, basestring):
			value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
		attrs['class'] = 'vTextField'
		html = super(TagAutocomplete, self).render(name, value, attrs)
		js = u'''<script type="text/javascript">
			$(document).ready(function() { 
				$("#%s").autocomplete({ serviceUrl: "%s", delimiter: /(,|;)\s*/ });
			});
			</script>''' % (attrs['id'], list_view)
		return mark_safe("\n".join([html, js]))
	
	class Media:
		css = {
		    'all': (settings.STATIC_URL + 'css/jquery.autocomplete.css',)
		}
		js = (
			'http://code.jquery.com/jquery-latest.js',
			settings.STATIC_URL +'js/jquery.autocomplete.js'
		)
