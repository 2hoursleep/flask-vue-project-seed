
# Base Database Driver

from abc import ABCMeta, abstractmethod


class BaseDriver(metaclass=ABCMeta):
	"""
	Provides interface for all proper database drivers.
	"""


	@abstractmethod
	def __init__(self, database_name):
		pass


	########## CRUD INTERFACE METHODS ##########

	@abstractmethod
	def insert(self, table_name, value_props={}):
		pass

	@abstractmethod
	def find_by_fields(self, table_name, where_props={}, limit=None):
		pass

	@abstractmethod
	def update_by_fields(self, table_name, value_props={}, where_props={}):
		pass

	@abstractmethod
	def delete_by_fields(self, table_name, where_props={}):
		pass


	########## DATABASE UTILITIES ##########

	@abstractmethod
	def create_table(self, table_name, column_props={}):
		pass

	@abstractmethod
	def delete_table_contents(self, table_name):
		pass

	@abstractmethod
	def delete_table(self, table_name):
		pass

	@abstractmethod
	def get_database_size(self):
		pass

	@abstractmethod
	def describe_table(self, table_name):
		pass

