from mapper.mapper import Mapper


class LocationMapper(Mapper):
  def __init__(self, sheet_key):
    super(LocationMapper, self).__init__(sheet_key, 'locations', 'London')
