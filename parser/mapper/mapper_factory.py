from mapper.category_mapper import CategoryMapper
from mapper.location_mapper import LocationMapper


class MapperFactory:
  Category = 'category'
  Location = 'location'

  sheet_key = None
  categoryMapper = None
  locationMapper = None

  @classmethod
  def set_sheet_key(c, sheet_key):
    MapperFactory.sheet_key = sheet_key

  @classmethod
  def get(c, name):
    if name == MapperFactory.Category:
      if MapperFactory.categoryMapper is None:
        MapperFactory.categoryMapper = CategoryMapper(MapperFactory.sheet_key)
      return MapperFactory.categoryMapper
    elif name == MapperFactory.Location:
      if MapperFactory.locationMapper is None:
        MapperFactory.locationMapper = LocationMapper(MapperFactory.sheet_key)
      return MapperFactory.locationMapper
    else:
      raise ValueError(name)
