from mapper.mapper import Mapper


class CategoryMapper(Mapper):
  def __init__(self, sheet_key):
    super(CategoryMapper, self).__init__(sheet_key, 'categories', 'Misc')
