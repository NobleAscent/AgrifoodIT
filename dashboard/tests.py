from datetime import datetime

from django.test import TestCase
from .models import PresenceFile, Presence, Pig
from django.core.files.uploadedfile import SimpleUploadedFile
from .tasks import process_presence_line


# Create your tests here.
class PresenceFileProcessTestCase(TestCase):
    def setUp(self):
        sample_file = PresenceFile(file_name='20200713_presence.txt')
        sample_file.processing_status = False

        # How to unittest a FileField because I don't want to save the
        # file on disk. It is better to have it in code.
        # https://stackoverflow.com/questions/4283933/what-is-the-clean-way-to-unittest-filefield-in-django
        # Use triple quotes to create a multiline string
        # note the b in front of the string [bytes]
        sample_file.upload = SimpleUploadedFile(
            '20200713_presence.txt',
            b"""+ 1 E2000019991100851580391E 2020-07-13T17:17:35.321
                - 1 E2000019991100851580391E 2020-07-13T17:17:40.325
                + 1 E2000019991100851580391E 2020-07-13T17:18:47.076
                - 1 E2000019991100851580391E 2020-07-13T17:18:52.078
                + 1 E2000019991100851580391E 2020-07-13T17:19:00.830
                + 1 E200001952060087146038EF 2020-07-13T17:19:01.134
                - 1 E2000019991100851580391E 2020-07-13T17:19:06.365
                - 1 E200001952060087146038EF 2020-07-13T17:19:09.367
                + 1 E2000019991100851580391E 2020-07-13T17:19:25.584
                + 1 E200001999130097264042CC 2020-07-13T17:19:30.548
                + 2 E2000019991100851580391E 2020-07-13T17:19:34.736
                - 1 E2000019991100851580391E 2020-07-13T17:19:37.406
                - 1 E200001999130097264042CC 2020-07-13T17:19:40.407
                - 2 E2000019991100851580391E 2020-07-13T17:19:40.408
                + 2 E2000019991100851580391E 2020-07-13T17:19:45.435
                - 2 E2000019991100851580391E 2020-07-13T17:19:50.436
                + 4 E20000195206009213503D52 2020-07-13T18:10:17.661
                - 4 E20000195206009213503D52 2020-07-13T18:10:22.663
                + 3 E2000019520600431420150D 2020-07-13T18:12:14.388
                - 3 E2000019520600431420150D 2020-07-13T18:12:21.228
                + 4 E20000199911008725303A93 2020-07-13T18:12:41.354
                - 4 E20000199911008725303A93 2020-07-13T18:12:46.355
                + 2 E2000019520600191460056D 2020-07-13T18:43:24.946
                - 2 E2000019520600191460056D 2020-07-13T18:43:29.947
                + 4 E20000195206018413509C34 2020-07-13T18:43:44.657
                - 4 E20000195206018413509C34 2020-07-13T18:43:51.722
                + 3 E2000019520600191460056D 2020-07-13T18:43:52.577
                - 3 E2000019520600191460056D 2020-07-13T18:44:00.489
                + 2 E2000019520600191460056D 2020-07-13T18:44:16.886
                - 2 E2000019520600191460056D 2020-07-13T18:44:21.887
                + 4 E2000019520602221340C59F 2020-07-13T19:21:13.724
                - 4 E2000019520602221340C59F 2020-07-13T19:21:18.725
                + 4 E2000019520602221340C59F 2020-07-13T19:21:28.810
                - 4 E2000019520602221340C59F 2020-07-13T19:21:35.536
                + 4 E20000195206006314302257 2020-07-13T19:39:00.997
                - 4 E20000195206006314302257 2020-07-13T19:39:05.998"""
        )

    def test_processing_single_presence_line(self):
        # Correct Input
        row = process_presence_line('- 4 E20000195206006314302257 2020-07-13T19:39:05.998')
        self.assertEqual(False, row.direction)
        self.assertEqual(4, row.reader)
        self.assertEqual(Pig.objects.get(pk=3), row.pig_rfid)
        self.assertEqual(datetime.fromisoformat('2020-07-13T19:39:05.998'), row.timestamp)