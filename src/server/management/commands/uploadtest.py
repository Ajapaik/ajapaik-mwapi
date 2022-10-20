from django.core.management.base import BaseCommand, CommandError
import json
from webservice.models import User
from webservice.mediawiki import get_mediawiki_whoami, get_mediawiki_client, upload_file_to_commons, get_wikimediacommons_url
from webservice.wikimediacommonshelper import get_random_commons_image, download_tmp_file, delete_tmp_file

class Command(BaseCommand):
    help = 'Print wikimedia userinfo of first user'

    def handle(self, *args, **options):

        user = User.objects.first()
        print(user)

        image=get_random_commons_image(0)
        print(image)

        source_filename=download_tmp_file(image['image_url'])
        comment="Uploading image from https://commons.wikimedia.org/wiki/" + image['title'].replace(" ", "_") 

        client=get_mediawiki_client(user.id);
        r=upload_file_to_commons(
            client, 
            source_filename, 
            image['title'], 
            image['wikitext'] + "\n" + comment, 
            comment)

        print(r.json())
        target_url= get_wikimediacommons_url() + "/wiki/" + image["title"].replace(" ", "_")
        print("")
        print(target_url)
        delete_tmp_file(image['image_url'])

