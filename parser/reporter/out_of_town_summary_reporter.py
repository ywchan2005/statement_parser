import pandas as pd
from mapper.mapper_factory import MapperFactory
from reporter.abstract_reporter import AbstractReporter


class OutOfTownSummaryReporter(AbstractReporter):
  def report(self):
    print()
    classname = self.__class__.__name__
    print('===', classname, '=' * (50 - len(classname) - 5))
    town = MapperFactory.get(MapperFactory.Location).default_value
    df = self.df[(self.df.category.notnull()) & (self.df.location != town) & (self.df.amount > 0)].copy()
    df['payment_date'] = df.payment_date.dt.to_period('m')
    for location in df[df.location != town].location.unique():
      print('-' * (50 - 1 - len(location)), location)
      out_of_town_df = df[df.location == location]
      print(pd.pivot_table(out_of_town_df, values=['amount'], index='category', columns=['payment_date'], aggfunc='sum').fillna(0))
      print(f'total: {float(out_of_town_df.amount.sum())}')
