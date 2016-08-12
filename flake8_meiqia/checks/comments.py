import re
import tokenize

from flake8_meiqia import core


_TODO_RE = re.compile(r'\b(TODO|FIXME|XXX)(\()?')

@core.flake8ext
def meiqia_todo_format(physical_line, tokens):
    """Checks for 'TODO()' in comments.

    Okay: # TODO(timonwong)
    MQ101: # TODO
    MQ101: # TODO xxx
    MQ101: # TODO (timonwong)
    MQ101: # @ToDo
    """

    for token_type, text, start_index, _, _ in tokens:
        if token_type == tokenize.COMMENT:
            pos = text.find('@ToDo')
            if pos >= 0:
                return pos + start_index[1], "MQ101: Use TODO(NAME)"

            m = _TODO_RE.search(text)
            if not m:
                continue

            pos = m.pos
            groups = m.groups()
            if not groups[-1]:
                return pos + start_index[1], "MQ101: Use %s(NAME)" % groups[0]
