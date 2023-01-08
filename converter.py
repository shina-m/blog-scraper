import pypandoc
import logging
import os


logging.getLogger('pypandoc').addHandler(logging.NullHandler())

filters = []
pdoc_args =[] #['--mathjax', '-smart']
output = pypandoc.convert_file(
    'book.md',
    'docx',
    outputfile="book2.docx",
    format='md',
    extra_args=pdoc_args,
    filters=filters,
)
assert output == ""

