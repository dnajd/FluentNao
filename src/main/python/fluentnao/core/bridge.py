"""Bridge between FluentNao and the HTTP server's event queue.

Keeps nao.py decoupled from the server module. The server calls
bridge.connect(nao) at startup to wire emit/emit_events into the
server's long poll queue.

Without connect(), nao.emit() is a silent no-op and emit_events()
logs a warning. All other FluentNao features work normally.
"""


class Bridge(object):
    """Mixin-style bridge that attaches to a Nao instance.

    Usage from server startup::

        from fluentnao.core.bridge import Bridge
        bridge = Bridge(nao, push_event_fn)

    This replaces nao.emit with a function that pushes to the server
    queue, and adds nao.emit_events() for subscribing NAO events to
    the queue.
    """

    def __init__(self, nao, push_event_fn):
        self.nao = nao
        self._push_event = push_event_fn

        # replace nao.emit with the wired version
        nao.emit = self._emit
        nao.emit_events = self._emit_events
        nao.log('bridge: connected')

    def _emit(self, event, value=None):
        """Push a custom event to the server's long poll queue.

        Args:
            event: event name string (can be anything)
            value: any value to include with the event

        Examples:
            nao.emit('greeting_complete', 'Don')
            nao.emit('task_done')
            nao.emit('object_found', {'name': 'mug', 'distance': 0.5})
        """
        self._push_event(event, value)
        return self.nao

    def _emit_events(self, event_names=None):
        """Subscribe to NAO events and push them to the server's long poll queue.

        Events become available via GET /events (long poll endpoint).
        Call with no args to emit all events.

        Args:
            event_names: list of event strings, a category set, or None for all.

        Returns:
            nao

        Examples:
            nao.emit_events()                        # all events
            nao.emit_events(nao.events.touch)        # only touch
            nao.emit_events(nao.events.all())        # explicit all
            nao.emit_events([nao.events.vision.FaceDetected,
                             nao.events.touch.ChestButtonPressed])
        """
        if event_names is None:
            event_names = self.nao.events.all()

        self.nao.subscribe(event_names, lambda event, value: self._push_event(event, value))
        self.nao.log('emit_events: {} events -> /events endpoint'.format(len(list(event_names))))
        return self.nao
