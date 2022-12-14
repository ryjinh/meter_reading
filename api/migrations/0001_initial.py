# Generated by Django 4.1.1 on 2022-09-20 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mpan',
            fields=[
                ('mpan_core', models.CharField(db_index=True, max_length=13, primary_key=True, serialize=False, unique=True)),
                ('validation_status', models.CharField(choices=[('VALIDATED', 'Validated'), ('NOT_VALIDATED', 'Not validated'), ('FAILED', 'Failed')], max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.CharField(db_index=True, max_length=10, primary_key=True, serialize=False, unique=True)),
                ('reading_type', models.CharField(choices=[('ACTUAL_CHANGE_OF_SUPPLIER_READ', 'Actual change of supplier read'), ('CUSTOMER_OWN_READ', 'Customer own read'), ('DEEMED_REGISTERS_OR_ESTIMATED_REGISTERS', 'Deemed registers or estimated registers'), ('FINAL', 'Final'), ('INITIAL', 'Initial'), ('MAR', 'MAR'), ('OLD_SUPPLIER_ESTIMATED_COS_READING', "Old supplier's estimated CoS reading"), ('ELECTRONICALLY_COLLECTED_VIA_PPMIP', 'Electronically collected via PPMIP'), ('METER_READING_MODIFIED_MANUALLY_BY_DC', 'Meter reading modified manually by DC'), ('ROUTINE', 'Routine'), ('SPECIAL', 'Special'), ('PROVING_TEST_READING', 'Proving test reading'), ('WITHDRAWN', 'Withdrawn'), ('ACTUAL_CHANGE_OF_TENANCY_READ', 'Actual change of tenancy read')], max_length=128, null=True)),
                ('mpan_core', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.mpan')),
            ],
        ),
        migrations.CreateModel(
            name='Reading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('register_id', models.CharField(max_length=128, null=True)),
                ('reading_value', models.DecimalField(decimal_places=1, max_digits=10)),
                ('reading_taken_at', models.DateTimeField(null=True)),
                ('reading_flag', models.CharField(choices=[('VALID', 'Valid'), ('SUSPECT', 'Suspect')], max_length=128, null=True)),
                ('reading_method', models.CharField(choices=[('NOT_VIEWED_BY_AN_AGENT_OR_NON_SITE_VISIT', 'Not viewed by an agent or non-site visit'), ('VIEWED_BY_AN_AGENT_OR_SITE_VISIT', 'Viewed by an agent or on-site visit')], max_length=128, null=True)),
                ('file_name', models.CharField(max_length=128, null=True)),
                ('meter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.meter')),
                ('mpan_core', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.mpan')),
            ],
            options={
                'unique_together': {('mpan_core', 'register_id', 'reading_taken_at')},
            },
        ),
    ]
