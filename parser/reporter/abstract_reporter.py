import abc


class AbstractReporter(metaclass=abc.ABCMeta):
  def __init__(self, df):
    self.df = df

  @abc.abstractmethod
  def report(self):
    pass
