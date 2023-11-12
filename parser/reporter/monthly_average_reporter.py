import pandas as pd
from mapper.mapper_factory import MapperFactory
from reporter.abstract_reporter import AbstractReporter


class MonthlyAverageReporter(AbstractReporter):
  def report(self):
    print()
    classname = self.__class__.__name__
    print('===', classname, '=' * (50 - len(classname) - 5))
    town = MapperFactory.get(MapperFactory.Location).default_value
    print('-' * (50 - 1 - len(town)), town)
    df = self.df[(self.df.category.notnull()) & (self.df.location == town) & (self.df.amount > 0)].copy()
    days = (df.payment_date.max() - df.payment_date.min()).days
    df['payment_date'] = df.payment_date.dt.to_period('m')
    print(pd.DataFrame([
      ['total', df.amount.sum()],
      ['days', days],
      ['monthly', df.amount.sum() * 365 / 12 / days],
    ]))
