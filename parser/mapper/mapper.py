import collections

import gspread


class Mapper:
  def __init__(self, sheet_key, worksheet_name, default_value):
    self.sheet_key = sheet_key
    self.worksheet_name = worksheet_name
    self.default_value = default_value
    self.load()
  
  def load(self):
    self.mapping = collections.defaultdict(list)
    service_account = gspread.service_account()
    sheet = service_account.open_by_key(self.sheet_key)
    records = sheet.worksheet(self.worksheet_name).get_all_values()
    for record in records[1:]:
      category, keyword = record[:2]
      self.mapping[category].append(keyword)

  def map_by_keyword(self, x):
    x = x.upper()
    for k, values in self.mapping.items():
      for v in values:
        if v in x:
          return k
    return self.default_value
