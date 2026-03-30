from markdown.extensions import Extension

from .snippet_preprocessor import TestSnippets
from .tab_label_icons import TabLabelIcons

__all__ = ["makeExtension"]


class BecDocsExtension(Extension):
    def extendMarkdown(self, md):
        TabLabelIcons().extendMarkdown(md)
        TestSnippets().extendMarkdown(md)


def makeExtension(**kwargs):
    return BecDocsExtension(**kwargs)
