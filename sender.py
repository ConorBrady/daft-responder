import requests
import logging

def email_to(ident, logger):
    logger = logging.getLogger('daft_scraper')

    message = """
        Hey,

        Got in pretty quick on this one :P

        I'd love to check the place out as soon as is convenient. My lease is
        going to be up at the end of month so I'm eager to find somewhere new.

        I'm a 25 yo male, working in a tech company in the IFSC called HubSpot.
        Tend to spend a lot of time in the living room looking for someone to
        chat to, rock climbing or sitting in a cafe somewhere. Also burritos,
        I eat a lot of burritos.

        Anyway, I look forward to the chance to view the place and get to meet you.

        Cheers,
        Conor

        Facebook: http://fb.com/conorjbrady
        LinkedIn: http://lnkdin.me/conor
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
        logger.info("Email successfully sent to {0}".format(ident))
    else:
        logger.error(req.text)
