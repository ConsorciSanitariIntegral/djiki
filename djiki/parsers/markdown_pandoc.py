# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.files import File
from tempfile import NamedTemporaryFile

import pandoc


def render(src):
    # pandoc.PANDOC_PATH = settings.MEDIA_ROOT
    doc = pandoc.Document()
    doc.markdown = src
    return doc.html
