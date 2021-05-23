from django.core.management import BaseCommand
import requests
import csv
from datetime import datetime, timedelta
import json
import time
import os
from pathlib import Path

from trading.utils import NSE_CSV_PATH, QUANDL_FIN_DATA_JSON_PATH
from company.models import Company
from stock.models import Stock

NOW = datetime.now()

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("populating default data")
        self.isin_code_map = {}
        self.create_bse_code_map()
        self.addNifty50Companies()
        self.refresh_data(True)

    def create_bse_code_map(self):
        # get BSE security code from BSE_List.csv, downloaded from https://www.bseindia.com/corporates/List_Scrips.aspx
        with open(os.path.join(BASE_DIR,'BSE_list.csv'), 'r') as csvin:
            csv_reader = csv.DictReader(csvin)
            for row in csv_reader:
                self.isin_code_map[row['ISIN No']] = row['Security Code']
    
    def addNifty50Companies(self):
        response = requests.get(NSE_CSV_PATH)
        if  response.status_code == 200:
            csv_data = response.text
            csv_reader = csv.reader(csv_data.split('\r\n'), delimiter=",")
            row_num = 0
            for row in csv_reader:
                if row_num != 0 and len(row) == 5:
                    # non header row
                    company = {
                        'name': row[0],
                        'industry': row[1],
                        'symbol': row[2],
                        'series': row[3],
                        'isin': row[4]
                    }
                    if not Company.objects.filter(name=company['name']).exists():
                        print("Adding company: {} {}".format(row_num, company['name']))
                        try:
                            company['bse_code'] = self.isin_code_map[company['isin']]
                        except:
                            print("BSE Code not found for {} with ISIN {}".format(company['symbol'], company['isin']))
                            row_num += 1
                            continue
                        obj = Company.objects.create(**company)
                        obj.save()
                    # TODO: delete companies which are not a part of NIFTY50 now, maybe by a deleted flag
                row_num += 1

    def refresh_data(self, discard_all_stocks = False):
        companies = Company.objects.all()
        num_companies = len(companies)
        cur_idx = 0
        while cur_idx < num_companies:
            company = companies[cur_idx]
            if discard_all_stocks:
                company.price_updated_at = None
                num_records = Stock.objects.filter(company__name=company.name).delete()
                print("Deleted {} records of {}".format(num_records, company.name))
            if company.price_updated_at == None or company.price_updated_at < (NOW - timedelta(days=1)):
                stock_updated = False
                latest_stock = Stock.objects.filter(company__name=company.name).order_by("-record_date").first()
                latest_record_date = NOW - timedelta(days=100*365)
                if latest_stock:
                    latest_record_date = latest_stock.record_date
                print("{} : Processing {} of {} : {}".format(datetime.now(), cur_idx+1, num_companies, company.symbol))
                response = requests.get(QUANDL_FIN_DATA_JSON_PATH.format(company.bse_code))
                itr = 0
                if response.status_code == 200:
                    json_data = json.loads(response.text)
                    if 'dataset' in json_data.keys():
                        stocks_datas = json_data['dataset']['data']
                        for data in stocks_datas:
                            try:
                                cur_date = datetime.strptime(data[0], "%Y-%m-%d")
                                stock = {
                                    'record_date': datetime.isoformat(cur_date),
                                    'open': float(data[1]),
                                    'high': float(data[2]),
                                    'low': float(data[3]),
                                    'close': float(data[4]),
                                    'volume': float(data[6]),
                                    # 'adjusted_close': float(data['5. adjusted close']),
                                    # 'volume': float(data['6. volume']),
                                    # 'dividend': float(data['7. dividend amount']),
                                    # 'split': float(data['8. split coefficient'])
                                    'company': company
                                }
                                if stock['volume'] == 0:
                                    continue
                                if discard_all_stocks or \
                                    (not discard_all_stocks and cur_date > latest_record_date):
                                    # TODO: take into account the oldest_record_date as well
                                    obj = Stock.objects.create(**stock)
                                    obj.save()
                                    itr += 1
                            except Exception as e:
                                print("Exception encountered : {} \n with data: {} \n for URL {}".format(e, data, QUANDL_FIN_DATA_JSON_PATH.format(company.bse_code)))
                    else:
                        print("Dataset is blank for URL: {}".format(QUANDL_FIN_DATA_JSON_PATH.format(company.bse_code)))
                        continue
                else:
                    print("Response NOT OK for company: {} with URL: {}, {}".format(company.name, QUANDL_FIN_DATA_JSON_PATH.format(company.bse_code), response.status_code))
                if itr > 0:
                    print("Processed {} records for {} {}".format(itr, cur_idx, company.name))
                    company.price_updated_at = NOW
                    company.save()
            cur_idx += 1
        print("Refresh complete!")