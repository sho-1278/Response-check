from django.db import models

# Create your models here.
class Response_sheet(models.Model):
	Link = models.TextField(blank=False) 


class Masteranswer(models.Model):
	QUESTION_TYPE = [
		('NAT', 'NAT'),
		('MCQ', 'MCQ'),
		('MSQ','MSQ'),
	]
	ANSWER_CHOICES = [
		('A','A'),
		('B','B'),
		('C','C'),
		('D','D'),
		('AB','AB'),
		('AC','AC'),
		('AD','AD'),
		('BC','BC'),
		('BD','BD'),
		('CD','CD'),
		('ABC','ABC'),
		('ABD','ABD'),
		('ACD','ACD'),
		('BCD','BCD'),
		('ABCD','ABCD'),
	]
	COURSE_CHOICES = [
		('CS','CS'),
		('EC','EC'),
	]
	Course   = models.CharField(max_length=200, choices=COURSE_CHOICES, blank=False, default='CS')
	Ques     = models.IntegerField(blank=False)
	Type     = models.CharField(max_length=200, choices=QUESTION_TYPE, blank=False, default='MCQ')
	Ans_opt  = models.CharField(max_length=200, choices=ANSWER_CHOICES, blank=False, default='A')
	Ans_natl = models.DecimalField(max_digits=15, decimal_places=4, blank=False, default=0)
	Ans_nath = models.DecimalField(max_digits=15, decimal_places=4, blank=False,default=0)
	corr_mark= models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=2)
	neg_mark = models.DecimalField(max_digits=5, decimal_places=2, blank=False, default=0)
	mta      = models.BooleanField(blank=False, default=False)
