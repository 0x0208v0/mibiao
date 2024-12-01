from __future__ import annotations

import mistune
from mistune import HTMLRenderer
from mistune.util import escape
from mistune.util import safe_entity
from mistune.util import striptags


class MyRenderer(HTMLRenderer):
    def link(self, text: str, url: str, title=None) -> str:
        s = '<a class="text-[#55b786] hover:text-[#45ca6b]" href="' + self.safe_url(url) + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + '>' + text + '</a>'

    def thematic_break(self) -> str:
        return '<hr class="mt-1 mb-1" />\n'

    def image(self, text: str, url: str, title=None) -> str:
        src = self.safe_url(url)
        alt = escape(striptags(text))
        s = '<img class="mt-1 mb-1" src="' + src + '" alt="' + alt + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + ' />'


def markdown_to_html(text: str) -> str:
    markdown = mistune.create_markdown(renderer=MyRenderer())
    return markdown(text)
