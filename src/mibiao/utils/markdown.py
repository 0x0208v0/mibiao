from __future__ import annotations

import mistune
from mistune import HTMLRenderer
from mistune.util import escape
from mistune.util import safe_entity
from mistune.util import striptags


class MyRenderer(HTMLRenderer):
    def paragraph(self, text: str) -> str:
        return '<p class="my-[7px] mx-0">' + text + '</p>\n'

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
        class_value = 'mx-auto my-1 max-w-[95%] h-auto'
        s = f'<img class="{class_value}" src="' + src + '" alt="' + alt + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + ' />'

    def block_code(self, code: str, info=None) -> str:
        html = (
            '<pre class="my-[14px] mx-0"><code class="block bg-[#ff9] overflow-auto py-[4px] px-[8px] border rounded-2'
        )
        if info is not None:
            info = safe_entity(info.strip())
        if info:
            lang = info.split(None, 1)[0]
            html += ' language-' + lang
        return html + '">' + escape(code) + '</code></pre>\n'

    def codespan(self, text: str) -> str:
        return '<code class="bg-[#ff9]">' + text + '</code>'

    def heading(self, text: str, level: int, **attrs) -> str:
        tag = 'h' + str(level)
        border = 'border-t-[1px] border-dotted border-[#e9e9e9] '
        text_class = {
            1: f'text-[17px] font-[700] text-[#2ea44f] pt-[3px] {border}',
            2: f'text-[16px] font-[700] text-[#2ea44f] pt-[3px] {border}',
            3: 'text-[15px] font-[700] text-[#555a62] leading-[1.25]',
            4: 'text-[14px] font-[700] text-[#555a62] leading-[1.25]',
            5: 'text-[13px] font-[700] text-[#555a62] leading-[1.25]',
        }
        class_value = 'my-[5px]' + ' ' + text_class.get(level, '')
        html = '<' + tag + f' class="{class_value}"'
        _id = attrs.get('id')
        if _id:
            html += ' id="' + _id + '"'
        return html + '>' + text + '</' + tag + '>\n'


def markdown_to_html(text: str) -> str:
    markdown = mistune.create_markdown(renderer=MyRenderer())
    return markdown(text)
