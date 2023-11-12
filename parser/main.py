import glob
import sys

import gspread
import pandas as pd
from mapper.mapper_factory import MapperFactory
from parser.hsbc_bank_parser import HsbcBankParser
from parser.hsbc_credit_card_parser import HsbcCreditCardParser
from parser.lloyds_bank_parser import LloydsBankParser
from reporter.category_summary_reporter import CategorySummaryReporter
from reporter.monthly_average_reporter import MonthlyAverageReporter
from reporter.monthly_summary_reporter import MonthlySummaryReporter
from reporter.out_of_town_summary_reporter import OutOfTownSummaryReporter
from reporter.unknown_transaction_reporter import UnknownTransactionReporter

##############################
### main

def main():
  if len(sys.argv) != 2:
    print(sys.argv)
    return
  sheet_key = sys.argv[1]
  MapperFactory.set_sheet_key(sheet_key)
  process(sheet_key)

def process(sheet_key):
  dfs = [
    *process_hsbc_credit_card_pdfs(),
    *process_hsbc_bank_pdfs(),
    *process_lloyds_bank_pdfs(),
  ]
  df = pd.concat(dfs)

  if UnknownTransactionReporter(df).report():
    upload(df, sheet_key)
    for reporter in [
      CategorySummaryReporter(df),
      MonthlySummaryReporter(df),
      MonthlyAverageReporter(df),
      OutOfTownSummaryReporter(df),
    ]:
      reporter.report()

##############################
### process statements

def process_hsbc_credit_card_pdfs():
  parser = HsbcCreditCardParser()
  filepaths = glob.glob('/data/hsbc-uk-master-2*.pdf')
  dfs = [parser.parse(filepath) for filepath in filepaths]
  return dfs

def process_hsbc_bank_pdfs():
  parser = HsbcBankParser()
  filepaths = glob.glob('/data/hsbc-uk-2*.pdf')
  dfs = [parser.parse(filepath) for filepath in filepaths]
  return dfs

def process_lloyds_bank_pdfs():
  parser = LloydsBankParser()
  filepaths = glob.glob('/data/lloyds-2*.pdf')
  dfs = [parser.parse(filepath) for filepath in filepaths]
  return dfs

##############################
### upload result

def upload(df, sheet_key):
  df = df.copy()
  df['payment_period'] = df.payment_date.dt.strftime('%Y-%m')
  df['year'] = df.payment_date.dt.strftime('%Y')
  df['payment_date'] = df.payment_date.dt.strftime('%Y-%m-%d %H:%M:%S.%f')
  df = df.sort_values('payment_date')
  service_account = gspread.service_account()
  sheet = service_account.open_by_key(sheet_key)
  worksheet = sheet.worksheet('records')
  worksheet.update([df.columns.values.tolist()] + df.values.tolist())

if 'main' in __name__:
  main()