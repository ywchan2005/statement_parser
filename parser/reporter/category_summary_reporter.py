import pandas as pd
from mapper.mapper_factory import MapperFactory
from reporter.abstract_reporter import AbstractReporter


class CategorySummaryReporter(AbstractReporter):
  def report(self):
    print()
    classname = self.__class__.__name__
    print('===', classname, '=' * (50 - len(classname) - 5))
    town = MapperFactory.get(MapperFactory.Location).default_value
    print('-' * (50 - 1 - len(town)), town)
    summary = self.df[(self.df.category.notnull()) & (self.df.location == town) & (self.df.amount > 0)].copy()
    summary['payment_date'] = summary.payment_date.dt.to_period('m')
    summary = pd.pivot_table(summary, values=['amount'], index='category', columns=['payment_date'], aggfunc='sum').fillna(0)
    print(summary.shape)
    print(summary)
