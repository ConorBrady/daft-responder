import feedparser
import urlparse
from time import sleep
import dateutil.parser
import datetime
import pytz
import requests
import logging
import random

logger = logging.getLogger('daft_scraper')
hdlr = logging.FileHandler('scraper.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

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

        message = """
            Hey,

            Got in pretty quick on this one :P

            I'd love to check the place out as soon as is convenient. My lease is
            going to be up at the end of month so I'm eager to find somewhere new.

            I'm a 25 yo male, working in a tech company in the IFSC called HubSpot.
            Tend to spend a lot of time in the living room looking for someone to
            chat to, rock climbing or sitting in a cafe somewhere.

            Anyway, I look forward to the chance to view the place and get to meet you.

            Cheers,
            Conor

            Facebook: fb.com/conorjbrady
            LinkedIn: lnkdin.me/conor
        """

        req = requests.post("http://www.daft.ie/ajax_endpoint.php", data={
            'action': 'daft_contact_advertiser',
            'from': 'Conor Brady',
            'email': 'conorjbrady1@gmail.com',
            'message': message,
            'contact_number': '0863500626',
            'type': 'sharing',
            'id': ident,
            'self_copy': '1',
            'agent_id': ''
            })

        if req.text == u'"Email successfully sent to advertiser"':
            logger.info("Email successfully sent to {0}".format(entry['link']))
        else:
            logger.error(req.text)

    if datetime.datetime.now().hour < 8:
        sleep(15*60)
    else:
        sleep(random.randint(5*60,10*60))
