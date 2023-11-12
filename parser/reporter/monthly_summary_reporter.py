from mapper.mapper_factory import MapperFactory
from reporter.abstract_reporter import AbstractReporter


class MonthlySummaryReporter(AbstractReporter):
  def report(self):
    print()
    classname = self.__class__.__name__
    print('===', classname, '=' * (50 - len(classname) - 5))
    town = MapperFactory.get(MapperFactory.Location).default_value
    print('-' * (50 - 1 - len(town)), town)
    summary = self.df[(self.df.category.notnull()) & (self.df.location == town) & (self.df.amount > 0)].copy()
    summary['payment_date'] = summary.payment_date.dt.to_period('m')
    summary = summary.groupby('payment_date').amount.sum().to_frame().T
    print(summary.shape)
    print(summary)
