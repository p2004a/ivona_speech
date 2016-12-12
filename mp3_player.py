from typing.io import BinaryIO
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

Gst.init(None)
GObject.threads_init()

class Player(object):
    def __init__(self) -> None:
        self.pipeline = Gst.Pipeline.new('pipeline')

        self.appsrc = Gst.ElementFactory.make('appsrc', 'source')
        self.pipeline.add(self.appsrc)

        self.decode = Gst.ElementFactory.make('mad', 'convert')
        self.pipeline.add(self.decode)

        self.sink = Gst.ElementFactory.make('autoaudiosink', 'sink')
        self.pipeline.add(self.sink)

        self.appsrc.link(self.decode)
        self.decode.link(self.sink)

        self.appsrc.connect('need-data', self.__need_data)

        self.bus = self.pipeline.get_bus()

        self.file = None  # type: BinaryIO

    def __need_data(self, appsrc, how_much):
        data = self.file.read(512)
        if len(data) == 0:
            self.file = None
            appsrc.emit('end-of-stream')
        else:
            buffer = Gst.Buffer.new_allocate(None, len(data), None)
            buffer.fill(0, data)
            appsrc.emit('push-buffer', buffer)

    def play(self, file: BinaryIO) -> None:
        self.file = file

        self.pipeline.set_state(Gst.State.PLAYING)

        while True:
            msg = self.bus.poll(Gst.MessageType.ANY, 100000000)
            if msg is None:
                continue
            if msg.type == Gst.MessageType.ERROR:
                raise Exception(msg.parse_error())
            elif msg.type == Gst.MessageType.EOS:
                break

        self.pipeline.set_state(Gst.State.READY)

if __name__ == "__main__":
    player = Player()
    for i in range(5):
        f = open('out.mp3', 'rb')
        player.play(f)
        f.close()
