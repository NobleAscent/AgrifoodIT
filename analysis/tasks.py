from celery import shared_task

from analysis.models import FPMining
from analysis.rohit.presence_FPmining import generate_dataframe_for_FPGrowth, FPGrowth
from dashboard.models import PresenceFile, WeatherFile, Presence
from dashboard.processing.presence import process_presence_file

# celery -A AgrifoodIT worker -l info --pool=solo
from dashboard.processing.weather import process_weather_file


@shared_task()
def processFPGrowthForWholeDataset():
    pigs_in_data = Presence.objects.order_by('pig_rfid_id').distinct('pig_rfid_id')

    # Delete previous entries in the table
    FPMining.objects.all().delete()

    for pig in pigs_in_data:
        df = generate_dataframe_for_FPGrowth(pig.pig_rfid)
        processed_data_df = FPGrowth(dataset=df, min_support=0.1, min_length=3, min_support_of_custom_itemsets=0.1)

        print('Printing Row')
        for index, row in processed_data_df.iterrows():
            print(round(row["support"] * 100, 2), ', '.join(row["itemsets"]))
            db_row = FPMining()
            db_row.pig_id = pig.pig_rfid_id
            db_row.support = round(row["support"] * 100, 2)
            db_row.itemset = ', '.join(row["itemsets"])
            db_row.save()

    return {"status": True}
