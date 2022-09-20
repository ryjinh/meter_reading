from django.db import models
from datetime import datetime
import json
from django.db import models
from django.core import serializers


VALIDATION_STATUS_CHOICES = [
    ("VALIDATED", "Validated"),
    ("NOT_VALIDATED", "Not validated"),
    ("FAILED", "Failed"),
]

VALIDATION_STATUS_MAP = {
    "V": "VALIDATED",
    "U": "NOT_VALIDATED",
    "F": "FAILED",
}

READING_TYPE_CHOICES = [
    ("ACTUAL_CHANGE_OF_SUPPLIER_READ", "Actual change of supplier read"),
    ("CUSTOMER_OWN_READ", "Customer own read"),
    (
        "DEEMED_REGISTERS_OR_ESTIMATED_REGISTERS",
        "Deemed registers or estimated registers",
    ),
    ("FINAL", "Final"),
    ("INITIAL", "Initial"),
    ("MAR", "MAR"),
    ("OLD_SUPPLIER_ESTIMATED_COS_READING", "Old supplier's estimated CoS reading"),
    ("ELECTRONICALLY_COLLECTED_VIA_PPMIP", "Electronically collected via PPMIP"),
    ("METER_READING_MODIFIED_MANUALLY_BY_DC", "Meter reading modified manually by DC"),
    ("ROUTINE", "Routine"),
    ("SPECIAL", "Special"),
    ("PROVING_TEST_READING", "Proving test reading"),
    ("WITHDRAWN", "Withdrawn"),
    ("ACTUAL_CHANGE_OF_TENANCY_READ", "Actual change of tenancy read"),
]

READING_TYPE_MAP = {
    "A": "ACTUAL_CHANGE_OF_SUPPLIER_READ",
    "C": "CUSTOMER_OWN_READ",
    "D": "DEEMED_REGISTERS_OR_ESTIMATED_REGISTERS",
    "F": "FINAL",
    "I": "INITIAL",
    "M": "MAR",
    "O": "OLD_SUPPLIER_ESTIMATED_COS_READING",
    "P": "ELECTRONICALLY_COLLECTED_VIA_PPMIP",
    "Q": "METER_READING_MODIFIED_MANUALLY_BY_DC",
    "R": "ROUTINE",
    "S": "SPECIAL",
    "T": "PROVING_TEST_READING",
    "W": "WITHDRAWN",
    "Z": "ACTUAL_CHANGE_OF_TENANCY_READ",
}

READING_METHOD_CHOICES = [
    (
        "NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT",
        "Not viewed by an agent or non-site visit",
    ),
    ("VIEWED_BY_AN_AGENT_OR_SITE_VISIT", "Viewed by an agent or on-site visit"),
]

READING_METHOD_MAP = {
    "N": "NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT",
    "P": "VIEWED_BY_AN_AGENT_OR_SITE_VISIT",
}

READING_FLAG_CHOICES = [("VALID", "Valid"), ("SUSPECT", "Suspect")]

READING_FLAG_MAP = {
    "T": "VALID",
    "F": "SUSPECT",
}


class Mpan(models.Model):
    mpan_core = models.CharField(
        max_length=13, unique=True, db_index=True, primary_key=True
    )
    validation_status = models.CharField(
        max_length=128, null=True, choices=VALIDATION_STATUS_CHOICES
    )

    def __str__(self) -> str:
        return f"{self.mpan_core}"


class Meter(models.Model):
    mpan_core = models.ForeignKey(to=Mpan, on_delete=models.CASCADE)
    id = models.CharField(max_length=10, unique=True, primary_key=True, db_index=True)
    reading_type = models.CharField(max_length=128, null=True, choices=READING_TYPE_CHOICES)

    def __str__(self) -> str:
        return f"{self.id}"


class ReadingJson(models.QuerySet):
    """JSON serialization logic for Reading model"""

    def get_all_readings(self) -> list:
        return [
            i["fields"] for i in json.loads(serializers.serialize("json", self.all()))
        ]

    def get_for_mpan(self, mpan_core: str) -> list:
        return [
            i["fields"]
            for i in json.loads(
                serializers.serialize("json", self.filter(mpan_core=mpan_core))
            )
        ]

    def get_for_mpan_after(self, mpan_core: str, start_date: datetime) -> list:
        return [
            i["fields"]
            for i in json.loads(
                serializers.serialize(
                    "json",
                    self.filter(mpan_core=mpan_core, reading_taken_at__gte=start_date),
                )
            )
        ]

    def get_for_mpan_before(self, mpan_core: str, end_date: datetime) -> list:
        return [
            i["fields"]
            for i in json.loads(
                serializers.serialize(
                    "json",
                    self.filter(mpan_core=mpan_core, reading_taken_at__lte=end_date),
                )
            )
        ]

    def get_for_mpan_between(
        self, mpan_core: str, start_date: datetime, end_date: datetime
    ) -> list:
        return [
            i["fields"]
            for i in json.loads(
                serializers.serialize(
                    "json",
                    self.filter(
                        mpan_core=mpan_core,
                        reading_taken_at__gte=start_date,
                        reading_taken_at__lte=end_date,
                    ),
                )
            )
        ]


class Reading(models.Model):
    objects = ReadingJson.as_manager()
    register_id = models.CharField(max_length=128, null=True)
    mpan_core = models.ForeignKey(to=Mpan, on_delete=models.CASCADE)
    meter_id = models.ForeignKey(to=Meter, on_delete=models.CASCADE)
    reading_value = models.DecimalField(decimal_places=1, max_digits=10)
    reading_taken_at = models.DateTimeField(null=True, auto_now=False)
    reading_flag = models.CharField(max_length=128, null=True, choices=READING_FLAG_CHOICES)
    reading_method = models.CharField(
        max_length=128, null=True, choices=READING_METHOD_CHOICES
    )
    file_name = models.CharField(max_length=128, null=True)

    class Meta:
        # avoids creating duplicate reading entries in database
        # when files are processed by management command.
        unique_together=("mpan_core", "register_id", "reading_taken_at")

    def __str__(self) -> str:
        return f"{self.register_id}"
