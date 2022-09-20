"""
Module containing all business logic for processing D0010 flow files
"""
import os
import sys
import pytz
import logging
from datetime import datetime
import re
from django.core.management import base

import api.models


# regex to match a file name rather than a directory
FILE_REGEX = r"(\.[a-z]{3})$"


class InvalidFileFormat(Exception):
    pass


class Command(base.BaseCommand):
    help = "Process a flow file into the database"

    def add_arguments(self, parser) -> None:
        parser.add_argument("path", nargs=1, type=str)

    def handle(self, **options):
        """executes management command"""
        path = options["path"][0]
        if not re.search(FILE_REGEX, path):
            for f in os.listdir(path):
                file = os.path.join("meter_reading/resources/flow_files/", f)
                try:
                    self._process_file(file)
                except InvalidFileFormat:
                    logging.warning(
                        f"{file} was found to be invalid, but continuing..."
                    )
                    pass
            sys.exit(0)
        try:
            self._process_file(path)
            sys.exit(0)
        except InvalidFileFormat:
            logging.error("could not parse the file contents.")
            sys.exit(1)

    def _process_file(self, path: str) -> None:
        """
        Parses a flow file (or directory of flow files) and creates records in the databases.
        """
        with open(path) as f:
            if not f.readline().startswith("ZHV"):
                raise InvalidFileFormat(
                    "File format appears to be incorrect. "
                    "Please check that it is not corrupted"
                )
            for line in f.readlines():
                match line.split("|"):
                    case ["026", *mpan_data]:
                        mpan_core, validation_status, *_ = mpan_data
                        mpan_obj, _ = api.models.Mpan.objects.get_or_create(
                            mpan_core=mpan_core,
                            validation_status=api.models.VALIDATION_STATUS_MAP[
                                validation_status
                            ],
                        )
                    case ["028", *meter_data]:
                        meter_id, reading_type, *_ = meter_data
                        meter_obj, _ = api.models.Meter.objects.get_or_create(
                            mpan_core=mpan_obj,
                            id=meter_id,
                            reading_type=api.models.READING_TYPE_MAP[reading_type],
                        )
                    case ["030", *reading_data]:
                        (
                            meter_register_id,
                            read_at,
                            reading_value,
                            *_,
                            reading_flag,
                            reading_method,
                            _,
                        ) = reading_data
                        api.models.Reading.objects.create(
                            register_id=meter_register_id,
                            reading_taken_at=datetime.strptime(
                                read_at, "%Y%m%d%H%M%S"
                            ).astimezone(tz=pytz.UTC),
                            mpan_core=mpan_obj,
                            meter_id=meter_obj,
                            reading_value=reading_value,
                            reading_flag=api.models.READING_FLAG_MAP[reading_flag],
                            reading_method=api.models.READING_METHOD_MAP[
                                reading_method
                            ],
                            file_name=f.name
                        )
                    case _:
                        pass
