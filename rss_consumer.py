import feedparser
import urlparse
from time import sleep
import dateutil.parser
import datetime
import pytz
import random
import logging

import sender

def start():
    logger = logging.getLogger('daft_scraper')

    observedIds = set([])
    startUpTime = pytz.UTC.localize(datetime.datetime.now())
    logger.info("Program started")

    while True:

        logger.info("Requesting feed")

        f = feedparser.parse("http://www.daft.ie/rss.daft?uid=1059539&id=602926&xk=158993")

        logger.info("{0} entries recieved".format(len(f['entries'])))
        for entry in f['entries']:
            url = urlparse.urlparse(entry['link'])
            ident = urlparse.parse_qs(url.query)['id'][0]
            pub_date = dateutil.parser.parse(entry['published'])

            if pub_date < startUpTime:
                continue

            if ident in observedIds:
                continue

            observedIds.add(ident)
            sender.email_to(ident)

        if datetime.datetime.now().hour < 8:
            sleep(15*60)
        else:
            sleep(random.randint(5*60,10*60))
