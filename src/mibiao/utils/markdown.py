import functools

import mistune
from mistune import HTMLRenderer
from mistune import safe_entity


class MyRenderer(HTMLRenderer):
    def link(self, text: str, url: str, title=None) -> str:
        s = '<a class="text-[#0dbc79]" href="' + self.safe_url(url) + '"'
        if title:
            s += ' title="' + safe_entity(title) + '"'
        return s + '>' + text + '</a>'


@functools.lru_cache(maxsize=32)
def markdown_to_html(text: str) -> str:
    markdown = mistune.create_markdown(renderer=MyRenderer())
    return markdown(text)


if __name__ == '__main__':
    print(markdown_to_html('''[example](http://example.com)'''))
