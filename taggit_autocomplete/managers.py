#coding=utf-8

from django.contrib.admin.widgets import AdminTextInputWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

from taggit.forms import TagField
from taggit.managers import TaggableManager as BaseTaggableManager

from widgets import TagAutocomplete

class TaggableManager(BaseTaggableManager):
    def formfield(self, form_class=TagField, **kwargs):
        defaults = {
            "label": capfirst(self.verbose_name),
            "help_text": self.help_text,
            "required": not self.blank
        }
        defaults.update(kwargs)
        
        defaults['widget'] = TagAutocomplete
        
        return form_class(**defaults)

def exsiting_only(self, *tags):
    str_tags = set([
        t
        for t in tags
        if not isinstance(t, self.through.tag_model())
    ])
    tag_objs = set(tags) - str_tags
    # If str_tags has 0 elements Django actually optimizes that to not do a
    # query.  Malcolm is very smart.
    existing = self.through.tag_model().objects.filter(
        name__in=str_tags
    )
    tag_objs.update(existing)

    for tag in tag_objs: #это возможно тоже надо убрать
        self.through.objects.get_or_create(tag=tag, **self._lookup_kwargs())

from taggit.managers import _TaggableManager
from taggit.utils import require_instance_manager

_TaggableManager.add = require_instance_manager(exsiting_only)

