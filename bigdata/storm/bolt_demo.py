#encoding=utf8
import logging
from pyleus.storm import SimpleBolt
log = logging.getLogger('boltdemo')


class BoltDemo(SimpleBolt):

    OUTPUT_FIELDS = ['word','lenth']

    def process_tuple(self, tup):
        line, = tup.values
        log.debug(line)
        self.emit(line,(len(line)), anchors=[tup])


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./BoltDemo.log',
        format="%(message)s",
        filemode='a',
    )
    BoltDemo().run()
