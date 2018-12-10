#encoding=utf8
import logging
from pyleus.storm import SimpleBolt
log = logging.getLogger('boltdemo')


class PrintBolt(SimpleBolt):

    OUTPUT_FIELDS = []

    def process_tuple(self, tup):
        word,length = tup.values
        log.debug(word,length)
        print(word,length)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='./printbolt.log',
        format="%(message)s",
        filemode='a',
    )
    PrintBolt().run()
