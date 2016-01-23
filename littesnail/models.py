# -*- coding: utf-8 -*-

from django.db import models

class UserQuery(models.Model):
	user_id = models.CharField(max_length=100)
	query_str = models.CharField(max_length=100)
	query_date = models.DateTimeField('query date')
	query_result_date = models.DateTimeField('query result date')
	query_msg_id = models.CharField(max_length=100)
	query_result = models.CharField(max_length=1000)

	def __str__(self):
		return self.user_id + " " + query_str