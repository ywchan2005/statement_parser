from reporter.abstract_reporter import AbstractReporter


class UnknownTransactionReporter(AbstractReporter):
  def report(self):
    print()
    classname = self.__class__.__name__
    print('===', classname, '=' * (50 - len(classname) - 5))
    unknowns = self.df[self.df.category.isnull()]
    print(unknowns.shape)
    if len(unknowns) == 0:
      return True
    print(unknowns.sort_values('payment_date'))
    return False
