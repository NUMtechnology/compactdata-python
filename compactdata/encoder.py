from compactdata.escapes import encode_basestring, encode_basestring_ascii

INFINITY = float("inf")


class CompactDataEncoder:
    """Extensible CompactData <https://compactdata.org> encoder for Python data structures.

    Supports the following objects and types by default:

    +-------------------+---------------+
    | Python            | CompactData          |
    +===================+===============+
    | dict              | object        |
    +-------------------+---------------+
    | list, tuple       | array         |
    +-------------------+---------------+
    | str               | string        |
    +-------------------+---------------+
    | int, float        | number        |
    +-------------------+---------------+
    | True              | true          |
    +-------------------+---------------+
    | False             | false         |
    +-------------------+---------------+
    | None              | null          |
    +-------------------+---------------+

    To extend this to recognize other objects, subclass and implement a
    ``.default()`` method with another method that returns a serializable
    object for ``o`` if possible, otherwise it should call the superclass
    implementation (to raise ``TypeError``).

    """

    def __init__(
        self,
        *,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        sort_keys=False,
        indent=None,
        default=None,
        escape_char="\\",
        quote_char='"',
        shortest=True,
        dns_optimized=False,
    ):
        """Constructor for CompactDataEncoder, with sensible defaults.

        If skipkeys is false, then it is a TypeError to attempt
        encoding of keys that are not str, int, float or None.  If
        skipkeys is True, such items are simply skipped.

        If ensure_ascii is true, the output is guaranteed to be str
        objects with all incoming non-ASCII characters escaped.  If
        ensure_ascii is false, the output can contain non-ASCII characters.

        If check_circular is true, then lists, dicts, and custom encoded
        objects will be checked for circular references during encoding to
        prevent an infinite recursion (which would cause an OverflowError).
        Otherwise, no such check takes place.

        If allow_nan is true, then NaN, Infinity, and -Infinity will be
        encoded as such.  This behavior is not CompactData specification compliant,
        but is consistent with most JavaScript based encoders and decoders.
        Otherwise, it will be a ValueError to encode such floats.

        If sort_keys is true, then the output of dictionaries will be
        sorted by key; this is useful for regression tests to ensure
        that CompactData serializations can be compared on a day-to-day basis.

        If indent is a non-negative integer, then CompactData array
        elements and object members will be pretty-printed with that
        indent level.  An indent level of 0 will only insert newlines.
        None is the most compact representation.

        If specified, default is a function that gets called for objects
        that can't otherwise be serialized.  It should return a CompactData
        encodable version of the object or raise a ``TypeError``.

        If specified, escape_char is the character used to escape special
        characters in strings.  The default is ``\\``.

        If specified, quote_char is the character used to quote strings.  The
        default is ``"``.

        If shortest is true, then the choice of quote_char will be made to
        minimize the length of the output and indent will be ignored.  The
        default is ``True``.

        If dns_optimized is true, then the output will be optimized for DNS
        TXT records.  Overrides shortest to ``True``, ensure_ascii to ``True``,
        and escape_char to ``~``.  The default is ``False``.
        """

        self.skipkeys = skipkeys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.sort_keys = sort_keys
        self.indent = indent
        if default is not None:
            self.default = default
        self.escape_char = escape_char
        self.quote_char = quote_char
        self.shortest = shortest
        self.dns_optimized = dns_optimized
        if dns_optimized:
            self.shortest = True
            self.escape_char = "~"
            self.indent = None
            self.ensure_ascii = True

    def default(self, obj):
        """Implement this method in a subclass such that it returns
        a serializable object for ``o``, or calls the base implementation
        (to raise a ``TypeError``).

        For example, to support arbitrary iterators, you could
        implement default like this::

            def default(self, o):
                try:
                    iterable = iter(o)
                except TypeError:
                    pass
                else:
                    return list(iterable)
                # Let the base class default method raise the TypeError
                return CompactDataEncoder.default(self, o)
        """
        raise TypeError(f"Object of type {type(obj).__name__} is not serializable")

    def encode(self, o):
        """Return a CompactData string representation of a Python data structure.

        >>> from compactdata.encoder import CompactDataEncoder
        >>> CompactDataEncoder().encode({"foo": ["bar", "baz"]})
        '(foo=[bar;baz])'

        """
        # This is for extremely simple cases and benchmarks.
        if isinstance(o, str):
            if self.ensure_ascii:
                return encode_basestring_ascii(o, self.escape_char, self.quote_char, self.shortest)
            else:
                return encode_basestring(o, self.escape_char, self.quote_char, self.shortest)
        # This doesn't pass the iterator directly to ''.join() because the
        # exceptions aren't as detailed.  The list call should be roughly
        # equivalent to the PySequence_Fast that ''.join() would do.
        chunks = self.iterencode(o)
        if not isinstance(chunks, (list, tuple)):
            chunks = list(chunks)
        return "".join(chunks)

    def iterencode(self, o):
        """Encode the given object and yield each string
        representation as available.

        For example::

            for chunk in CompactDataEncoder().iterencode(bigobject):
                mysocket.write(chunk)

        """
        if self.check_circular:
            markers = {}
        else:
            markers = None
        if self.ensure_ascii:
            _encoder = encode_basestring_ascii
        else:
            _encoder = encode_basestring

        def floatstr(o, allow_nan=self.allow_nan, _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
            # Check for specials.  Note that this type of test is processor
            # and/or platform-specific, so do tests which don't depend on the
            # internals.

            if o != o:
                text = "NaN"
            elif o == _inf:
                text = "Infinity"
            elif o == _neginf:
                text = "-Infinity"
            else:
                return _repr(o)

            if not allow_nan:
                raise ValueError("Out of range float values are not CompactData compliant: " + repr(o))

            return text

        _iterencode = _make_iterencode(
            markers,
            self.default,
            _encoder,
            self.indent,
            floatstr,
            self.sort_keys,
            self.skipkeys,
            self.escape_char,
            self.quote_char,
            self.shortest,
            self.dns_optimized,
        )
        return _iterencode(o, 0)


def _make_iterencode(
    markers,
    _default,
    _encoder,
    _indent,
    _floatstr,
    _sort_keys,
    _skipkeys,
    _escape_char,
    _quote_char,
    _shortest,
    _dns_optimized,
):
    _intstr = int.__repr__
    _key_separator = "="
    _item_separator = ";"
    if _indent is not None and not isinstance(_indent, str):
        _indent = " " * _indent

    def _iterencode_list(lst, _current_indent_level):
        if not lst:
            yield "[]"
            return
        if markers is not None:
            marker_id = id(lst)
            if marker_id in markers:
                raise ValueError("Circular reference detected")
            markers[marker_id] = lst
        buf = "["
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = "\n" + _indent * _current_indent_level
            separator = _item_separator + newline_indent
            buf += newline_indent
        else:
            newline_indent = None
            separator = _item_separator
        first = True
        for value in lst:
            if first:
                first = False
            else:
                buf = separator
            if isinstance(value, str):
                yield buf + _encoder(value, _escape_char, _quote_char, _shortest)
            elif value is None:
                yield buf + "null"
            elif value is True:
                yield buf + "true"
            elif value is False:
                yield buf + "false"
            elif isinstance(value, int):
                # Subclasses of int/float may override __repr__, but we still
                # want to encode them as integers/floats in CompactData. One example
                # within the standard library is IntEnum.
                yield buf + _intstr(value)
            elif isinstance(value, float):
                # see comment above for int
                yield buf + _floatstr(value)
            else:
                yield buf
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield "\n" + _indent * _current_indent_level
        yield "]"
        if markers is not None:
            del markers[marker_id]

    def _iterencode_dict(dct, _current_indent_level):
        if not dct:
            yield "()"
            return
        if markers is not None:
            marker_id = id(dct)
            if marker_id in markers:
                raise ValueError("Circular reference detected")
            markers[marker_id] = dct
        yield "("
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = "\n" + _indent * _current_indent_level
            item_separator = _item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = _item_separator
        first = True
        if _sort_keys:
            items = sorted(dct.items())
        else:
            items = dct.items()
        for key, value in items:
            if isinstance(key, str):
                pass
            elif isinstance(key, float):
                # see comment for int/float in _make_iterencode
                key = _floatstr(key)
            elif key is True:
                key = "true"
            elif key is False:
                key = "false"
            elif key is None:
                key = "null"
            elif isinstance(key, int):
                # see comment for int/float in _make_iterencode
                key = _intstr(key)
            elif _skipkeys:
                continue
            else:
                raise TypeError(f"keys must be str, int, float, bool or None, " f"not {key.__class__.__name__}")
            if first:
                first = False
            else:
                yield item_separator
            yield _encoder(key, _escape_char, _quote_char, _shortest)
            if not isinstance(value, (list, tuple, dict)):
                yield _key_separator
            if isinstance(value, str):
                yield _encoder(value, _escape_char, _quote_char, _shortest)
            elif value is None:
                yield "null"
            elif value is True:
                yield "true"
            elif value is False:
                yield "false"
            elif isinstance(value, int):
                # see comment for int/float in _make_iterencode
                yield _intstr(value)
            elif isinstance(value, float):
                # see comment for int/float in _make_iterencode
                yield _floatstr(value)
            else:
                if isinstance(value, (list, tuple)):
                    chunks = _iterencode_list(value, _current_indent_level)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                else:
                    chunks = _iterencode(value, _current_indent_level)
                yield from chunks
        if newline_indent is not None:
            _current_indent_level -= 1
            yield "\n" + _indent * _current_indent_level
        yield ")"
        if markers is not None:
            del markers[marker_id]

    def _iterencode(o, _current_indent_level):
        if isinstance(o, str):
            yield _encoder(o, _escape_char, _quote_char, _shortest)
        elif o is None:
            yield "null"
        elif o is True:
            yield "true"
        elif o is False:
            yield "false"
        elif isinstance(o, int):
            # see comment for int/float in _make_iterencode
            yield _intstr(o)
        elif isinstance(o, float):
            # see comment for int/float in _make_iterencode
            yield _floatstr(o)
        elif isinstance(o, (list, tuple)):
            yield from _iterencode_list(o, _current_indent_level)
        elif isinstance(o, dict):
            yield from _iterencode_dict(o, _current_indent_level)
        else:
            if markers is not None:
                marker_id = id(o)
                if marker_id in markers:
                    raise ValueError("Circular reference detected")
                markers[marker_id] = o
            o = _default(o)
            yield from _iterencode(o, _current_indent_level)
            if markers is not None:
                del markers[marker_id]

    return _iterencode


class CompactDataEncodeError(Exception):
    pass
