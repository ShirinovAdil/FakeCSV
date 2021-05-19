from schemas.models import *
from schemas.services.generate_data import *
from Planeks.celery import app
from django.conf import settings
from celery.result import AsyncResult

import csv
import uuid
import logging
import sys


@app.task(bind=True)
def make_csv_file(self, schema_id, rows):
    """
    A Task that performs csv file creation and stores it in media folder
    """
    schema = SchemaModel.objects.get(id=schema_id)
    salt = str(uuid.uuid4())
    logger = logging.getLogger(__name__)
    logger.info('Task was started from tasks')
    try:
        columns = [
            column for column in schema.column_in_schemas.all().order_by("order")
        ]
        filename = f"/schema-{schema.id}---{salt}.csv"
        path = settings.MEDIA_ROOT + filename
        f = open(path, "w")
        f.truncate()
        csv_writer = csv.writer(f, delimiter=schema.separator)
        csv_writer.writerow([column.name for column in columns]) # writerow?
        for x in range(rows):
            row_to_write = list()
            for column in columns:
                row_to_write.append(" ".join(generate_csv_data(column.id).split()))
            csv_writer.writerow(
                row_to_write
            )
            print(f'Row: {x}')
            self.update_state(state='PROGRESS', meta={'done': x, 'total': rows})
            print(f"state is {self.AsyncResult(self.request.id).state}")
        schema.files.create(file=filename, status=SchemaModelStatusChoices.READY)
    except Exception as exc:
        print(exc)
        logger = logging.getLogger('MYAPP')
        logger.info(exc)
        schema.files.create(file='', status=SchemaModelStatusChoices.FAILED)
    finally:
        schema.save()
        print("Finished. File created")
        return self.AsyncResult(self.request.id).state
