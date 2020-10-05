from django.db import models


class Visitor(models.Model):
	city       = models.CharField(max_length=85)
	region     = models.CharField(max_length=85)
	country    = models.CharField(max_length=2)
	year	   = models.CharField(max_length=4)
	month      = models.CharField(max_length=2)
	day        = models.CharField(max_length=2)
	time       = models.CharField(max_length=8)  # Format is %H:%M:%S

	def csv(self):
		return (
        	f"{ self.city }, { self.region }, "
    		f"{ self.country }, { self.year }, { self.month }, "
    		f"{ self.day }, { self.time }"
    	)

	def json(self):
		return(
			f"{{\"city\": \"{ self.city }\", "
			f"\"region\": \"{ self.region }\", \"country\": \"{ self.country }\", "
			f"\"year\": \"{ self.year }\", \"month\": \"{ self.month }\", "
			f"\"day\": \"{ self.day }\", \"time\": \"{ self.time }\" }}"
		)

	def sql(self):
		return (
			f"'{ self.city }', '{ self.region }', "
			f"'{ self.country }', '{ self.year }', '{ self.month }', "
			f"'{ self.day }', '{ self.time }'"
		)


	def __str__(self):
		return (
			f"\n{ self.city }, { self.region }, { self.country }"
			f"\n Time: { self.time }"
			f"\nDate: { self.month }/{ self.day }/{ self.year }"
		)

	class Meta:
		verbose_name_plural = 'visitors'


class Page(models.Model):
	page_name = models.CharField(max_length=50)
	year      = models.CharField(max_length=4)
	month     = models.CharField(max_length=2)
	day       = models.CharField(max_length=2)
	time      = models.CharField(max_length=8)  # Format is %H:%M:%S

	def csv(self):
		return (
			f"{ self.page_name }, { self.year }, { self.month }, "
			f"{ self.day }, { self.time }"
		)

	def json(self):
		return (
			f"{{\"page_name\": \"{ self.page_name }\", \"year\": "
			f"\"{ self.year }\", \"month\": \"{ self.month }\", \"day\": "
			f"\"{ self.day }\", \"time\": \"{ self.time }\" }}"
		)

	def sql(self):
		return (
			f"'{ self.page_name }', '{ self.year }', '{ self.month }', "
			f"'{ self.day }', '{ self.time }'"
		)

	def __str__(self):
		return (
			f"\n{self.page_name} accessed at {self.time}"
			f"\nDate: {self.month}/{self.day}/{self.year}"
		)

	class Meta:
		verbose_name_plural = 'pages'