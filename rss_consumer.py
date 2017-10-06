import feedparser
import urlparse
from time import sleep
import dateutil.parser
import datetime
import pytz
import random
import sys
import logging
import yaml
import requests

logger = logging.getLogger('daft_scraper')
hdlr = logging.FileHandler('scraper.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

observedIds = set([])
startUpTime = pytz.UTC.localize(datetime.datetime.now())
logger.info("Program started")

feed = sys.argv[1]
ad_type = sys.argv[2]

logger.info("Feed: {0}, Ad type: {1}".format(feed, ad_type))

with open('input.yaml') as f:

    payload = {
        'action': 'daft_contact_advertiser',
        'type': ad_type,
        'self_copy': '1',
        'agent_id': ''
    }

    payload.update(yaml.safe_load(f))

    logger.info("Has payload {0}".format(payload))

    while True:

        logger.info("Requesting feed")

        f = feedparser.parse(feed)

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
            payload["id"] = ident
	    
            logger.info("Sending payload {0}".format(payload))
            
            req = requests.post("http://www.daft.ie/ajax_endpoint.php", data=payload, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
            })
            
            logger.info("Sent with response {0}".format(req))

            if req.text == u'"Email successfully sent to advertiser"':
                logger.info("Email successfully sent to {0}".format(ident))
            else:
                logger.info(req.text)

        if datetime.datetime.now().hour < 8:
            sleep(15*60)
        else:
            sleep(random.randint(5*60,10*60))

