import abc
import os
import pickle
import re

import numpy as np
import pandas as pd
import pdfquery
from mapper.mapper_factory import MapperFactory


class AbstractParser(metaclass=abc.ABCMeta):
  default_top = 685
  default_bottom = 56

  def __init__(self):
    self.pdf = None

  def parse(self, filepath):
    print(f'\tparsing ... {filepath}')
    cachepath = filepath.replace('/data', '/cache').replace('.pdf', '.pkl')
    df = self.load_cache(cachepath)
    if df is not None:
      return df
    
    self.load(filepath)

    rows = []
    for pageid in self.extract_pageids():
      header = self.extract_header(pageid)
      footer = self.extract_footer(pageid)
      top = np.ceil(min([AbstractParser.default_top] + [x.layout.y1 - 2 for x in header]))
      bottom = np.floor(max([AbstractParser.default_bottom] + [x.layout.y0 + 1 for x in footer]))
      amounts = self.extract_amounts(pageid, top, bottom)

      y = top
      for amount in amounts:
        items = self.extract_items(pageid, y + 1, amount.layout.y0 - 1)
        if items.count(None) < len(items):
          rows.append([*items, amount.text])
        y = amount.layout.y0

    df = pd.DataFrame(rows)
    df.columns = ['payment_date', 'remark', 'amount']
    df.payment_date.ffill(inplace=True)
    df = self.normalize(df)

    if df.category.isnull().sum() == 0:
      self.save_cache(cachepath, df)

    return df

  def load(self, filepath):
    self.pdf = pdfquery.PDFQuery(filepath)
    self.pdf.load()
    self.pdf.tree.write(filepath.replace('/data', '/tmp').replace('.pdf', '.xml'), pretty_print=True)
  
  def load_cache(self, cachepath):
    if os.path.exists(cachepath):
      with open(cachepath, 'rb') as f:
        return pickle.load(f)
    return None

  def save_cache(self, cachepath, df):
    with open(cachepath, 'wb') as f:
      pickle.dump(df, f)

  @abc.abstractmethod
  def extract_pageids(self):
    pass

  @abc.abstractmethod
  def extract_header(self, pageid):
    pass

  @abc.abstractmethod
  def extract_footer(self, pageid):
    pass

  @abc.abstractmethod
  def extract_amounts(self, pageid, top, bottom):
    pass

  @abc.abstractmethod
  def extract_items(self, pageid, top, bottom):
    pass

  def normalize(self, df):
    df['payment_date'] = df.payment_date.str.extract(r'(\d{2} [A-Z][a-z]{2} \d{2})', expand=False)
    df['payment_date'] = pd.to_datetime(df.payment_date.str.strip(), format='%d %b %y')
    df['remark'] = df.remark.str.upper() + ' | ' + df.payment_date.dt.strftime('%Y-%m-%d')
    df['category'] = df.remark.apply(MapperFactory.get(MapperFactory.Category).map_by_keyword)
    df['location'] = df.remark.apply(MapperFactory.get(MapperFactory.Location).map_by_keyword)
    df['amount'] = df.amount.str.replace(',', '').apply(lambda x: -float(re.findall('\d+', x)[0]) if 'CR' in x else float(x))
    df = self.exclude(df)
    return df

  @abc.abstractmethod
  def exclude(self, df):
    pass

  def extract_cell(self, pageid, bbox):
    items = self.extract_lines(pageid, bbox)
    texts = [item.text.strip() for item in items if len(item.text.strip()) > 0]
    if len(texts) == 0:
      return None
    content = ' | '.join(texts)
    return content

  def extract_lines(self, pageid, bbox):
    x0, y0, x1, y1 = bbox
    items = [item for container in ['LTTextLineHorizontal', 'LTTextBoxHorizontal'] for item in self.pdf.pq(f'LTPage[pageid="{pageid}"] {container}:in_bbox("{x0},{y0},{x1},{y1}")') if len(item.text) > 0]
    items = sorted(items, key=lambda item: (10000 - item.layout.y0) * 10000 + item.layout.x0)
    return items
  