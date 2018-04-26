
# Base Data Object

import sys
import config.config as config

from abc import ABCMeta, abstractmethod
import json


class BaseDataObject(metaclass=ABCMeta):
	"""
	Provides base methods and interface for all proper data objects.

	TODO:
		X test
		- add caching
		- write docstrings for all methods
	"""


	def __init__(self, prop_dict, db_driver_class, cache_driver_class):
		db_driver, cache_driver = self.__get_drivers(
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)
		self.db_driver = db_driver
		self.cache_driver = cache_driver
		self.state = prop_dict


	########## BASE METHODS ##########


	@classmethod
	def create(
		cls,
		prop_dict={},
		db_driver_class=None,
		cache_driver_class=None
	):

		return cls(
			prop_dict=prop_dict,
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)


	@classmethod
	def find_many(
		cls,
		prop_dict={},
		limit=None,
		db_driver_class=None,
		cache_driver_class=None
	):

		db_driver, cache_driver = cls.__get_drivers(
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)

		# TODO: before making trip to DB, try cache for data object here

		records = db_driver.find_by_fields(
			table_name=cls.TABLE_NAME,
			where_props=prop_dict,
			limit=limit
		)

		instances = [
			cls(
				prop_dict=record,
				db_driver_class=db_driver_class,
				cache_driver_class=cache_driver_class
			)
			for record in records
		]

		return instances


	@classmethod
	def find_one(
		cls,
		prop_dict={},
		db_driver_class=None,
		cache_driver_class=None
	):

		instance_list = cls.find_many(
			prop_dict=prop_dict,
			limit=1,
			db_driver_class=db_driver_class,
			cache_driver_class=cache_driver_class
		)

		if len(instance_list) > 0:
			return instance_list[0]
		else:
			return None


	def get_prop(self, prop_name):
		return self.state[prop_name]


	def set_prop(self, prop_name, prop_value):
		if prop_name in self.state:
			self.state[prop_name] = prop_value
			return True
		else:
			return False


	def save(self):

		# TODO: add caching of data object upon save here..

		# existing record
		if 'id' in self.state:
			record_update_count = self.db_driver.update_by_fields(
				table_name=self.TABLE_NAME,
				value_props=self.state,
				where_props={
					'id': self.get_prop('id')
				}
			)
			return self if record_update_count == 1 else None
		# new record
		else:
			new_record_id = self.db_driver.insert(
				table_name=self.TABLE_NAME,
				value_props=self.state
			)
			if new_record_id > 0:
				self = self.find_one(prop_dict={ 'id': new_record_id })
				return self
			else:
				return None


	def delete(self):
		record_delete_count = self.db_driver.delete_by_fields(
			table_name=self.TABLE_NAME,
			where_props={
				'id': self.get_prop('id')
			}
		)
		return True if record_delete_count > 0 else False


	########## UTILITY METHODS ##########


	def to_dict(self):
		return self.state


	def to_json(self, pretty=False):
		if pretty:
			return json.dumps(self.state, sort_keys=True, indent=2)
		else:
			return json.dumps(self.state)


	########## INTERFACE METHODS ##########


	# ...


	########## PRIVATE HELPERS ##########


	@classmethod
	def __get_drivers(cls, db_driver_class=None, cache_driver_class=None):

		db_driver_class = db_driver_class \
		if db_driver_class is not None \
		else cls.DEFAULT_DB_DRIVER_CLASS

		cache_driver_class = cache_driver_class \
		if cache_driver_class is not None \
		else cls.DEFAULT_CACHE_DRIVER_CLASS

		db_driver = None
		cache_driver = None

		if db_driver_class is not None:
			db_driver = db_driver_class(
				database_name=config.MYSQL_DB_NAME
			)

		if cache_driver_class is not None:
			cache_driver = cache_driver_class(
				database_name=config.MYSQL_DB_NAME
			)

		return db_driver, cache_driver


	def __get_prop_names(self):
		return self.db_driver.get_table_field_names(self.TABLE_NAME)

