import requests
import logging
import yaml

def email_to(ident, logger):
    logger = logging.getLogger('daft_scraper')

    with open('input.yaml') as f:
        req = requests.post("http://www.daft.ie/ajax_endpoint.php", data={
            'action': 'daft_contact_advertiser',
            'type': 'sharing',
            'id': ident,
            'self_copy': '1',
            'agent_id': ''
        }.update(yaml.self_load(f)))

        if req.text == u'"Email successfully sent to advertiser"':
            logger.info("Email successfully sent to {0}".format(ident))
        else:
            logger.error(req.text)
