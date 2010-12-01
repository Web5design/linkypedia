import logging
import time
import traceback
import urllib

from django.core.management.base import BaseCommand

from linkypedia.web import models as m

logging.basicConfig(
        filename="fetch_auth.log", 
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s")

class Command(BaseCommand):

    def handle(self, **options):
        errols = m.Link.objects.filter(target__contains='errol.oclc')
        errols = errols.filter(target__endswith='.html')
        for errol in errols:
            logging.info('fetching for link %s, %s' % (errol.id, errol.target))
            marcxml_url = errol.target.replace('.html', '.MarcXML')
            try:
                auth_record, created = m.AuthRecord.objects.get_or_create(link=errol)
                data = urllib.urlopen(marcxml_url).read()
                auth_record.marcxml = data
                auth_record.save()
            except:
                logging.error(traceback.print_exc())
            #time.sleep(1)
