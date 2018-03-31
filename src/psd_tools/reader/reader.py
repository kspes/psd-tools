# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, division
import logging

import psd_tools.reader.header
import psd_tools.reader.color_mode_data
import psd_tools.reader.image_resources
import psd_tools.reader.layers
from psd_tools.debug import pretty_namedtuple

logger = logging.getLogger(__name__)

ParseResult = pretty_namedtuple(
    'ParseResult',
    'header, color_data, image_resource_blocks, layer_and_mask_data, image_data'
)

def parse(fp, encoding='utf8', progress_callback = None):
    def progress(value):
        if progress_callback != None:
            progress_callback(value)

    header = psd_tools.reader.header.read(fp)
    progress(0.2)
    color_mode_data = psd_tools.reader.color_mode_data.read(fp)
    progress(0.4)
    image_resources = psd_tools.reader.image_resources.read(fp, encoding)
    progress(0.6)
    layers = psd_tools.reader.layers.read(fp, encoding, header.depth)
    progress(0.8)
    image_data = psd_tools.reader.layers.read_image_data(fp, header)
    progress(1.0)
    return ParseResult(
        header,
        color_mode_data,
        image_resources,
        layers,
        image_data
    )
