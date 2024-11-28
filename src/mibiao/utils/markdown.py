import mistune
from mistune import HTMLRenderer
from mistune import safe_entity


class MyRenderer(HTMLRenderer):
    def link(self, text: str, url: str, title=None) -> str:
        s = '<a class="text-[#55b786] hover:text-[#45ca6b]" href="' + self.safe_url(url) + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + '>' + text + '</a>'


def markdown_to_html(text: str) -> str:
    markdown = mistune.create_markdown(renderer=MyRenderer())
    return markdown(text)
