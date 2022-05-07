from django.shortcuts import render, redirect
from .models import Response_sheet, Masteranswer
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlsplit
# Create your views here.
answer_data    = []
def index(request):
	if request.method == "POST":
		link = request.POST['link']
		link_data = isvalidlink(link)
		if link_data == True:
			Response_sheet.objects.create(Link=link)
			return redirect('results')
		else:
			return redirect("errors")
	return render(request, 'rpspgate/index.html')

def isvalidlink(link):
	global answer_data
	url = requests.get(link)
	if url.status_code == 200 and urlparse(link).netloc == "g26.tcsion.com":
		course  = link.split('/')[-1][:2]
		all_ans = Masteranswer.objects.filter(Course=course)
		if len(all_ans) == 0:
			return False
		soup = BeautifulSoup(url.content, 'lxml')
		try:
			all_questions = soup.find_all('table', class_='questionPnlTbl')
		if len(all_questions) != 65:
			return False
		for i in range(len(all_questions)):
			ans_set    = []
			ans_set.append(i+1)
			question   = all_questions[i]
			ques_panel = question.find('table', class_='questionRowTbl')
			opt_panel  = question.find('table', class_='menu-tbl')
			menu_rows  = opt_panel.find_all('tr')
			qid        = menu_rows[0].find('td', class_="bold").text[-3:]
			status     = menu_rows[1].find('td', class_="bold").text
			if status == "Answered" or  status == "Marked For Review":
				ques_obj = all_ans.get(Ques=int(qid))
				if ques_obj.Type == 'NAT':
					giv_ans = ques_panel.find_all('td',class_="bold")[-1].text
					ans_set.append(giv_ans)
					ans_set.append(str(ques_obj.Ans_natl)+ " - " + str(ques_obj.Ans_nath))
					if ques_obj.neg_mark == 0:
						ans_set.append(str(ques_obj.corr_mark)+"/0")
					else:
						ans_set.append(str(ques_obj.corr_mark)+"/-"+str(ques_obj.neg_mark))
					if float(giv_ans) >= ques_obj.Ans_natl and float(giv_ans)<= ques_obj.Ans_nath:
						ans_set.append(ques_obj.corr_mark)
					else:
						if ques_obj.neg_mark == 0:
							ans_set.append(0)
						else:
						    ans_set.append(-1*ques_obj.neg_mark)
				elif ques_obj.Type == 'MCQ':
					chosen = opt_panel.find_all('td', class_="bold")[-1].text
					ans_set.append(chosen)
					ans_set.append(ques_obj.Ans_opt)
					if ques_obj.neg_mark == 0:
						ans_set.append(str(ques_obj.corr_mark)+"/0")
					else:
						ans_set.append(str(ques_obj.corr_mark)+"/-"+str(ques_obj.neg_mark))
					if chosen == ques_obj.Ans_opt:
						ans_set.append(ques_obj.corr_mark)
					else:
						if ques_obj.neg_mark ==0:
							ans_set.append(0)
						else:
							ans_set.append(float(-1*ques_obj.neg_mark))
				else:
					chosen = ''.join((opt_panel.find_all('td',class_="bold")[-1].text).split(','))
					ans_set.append(opt_panel.find_all('td',class_="bold")[-1].text)
					ans_set.append(','.join(ques_obj.Ans_opt))
					if ques_obj.neg_mark == 0:
						ans_set.append(str(ques_obj.corr_mark)+"/0")
					else:
						ans_set.append(str(ques_obj.corr_mark)+"/-"+str(ques_obj.neg_mark))
					if chosen == ques_obj.Ans_opt:
						ans_set.append(ques_obj.corr_mark)
					else:
						if ques_obj.neg_mark ==0:
							ans_set.append(0)
						else:
						    ans_set.append(float(-1*ques_obj.neg_mark))
			else:
				ans_set.append('NA')
				ques_obj = all_ans.get(Ques=int(qid))
				if ques_obj.Type == 'NAT':
					ans_set.append(str(ques_obj.Ans_natl)+ " - " + str(ques_obj.Ans_nath))
				elif ques_obj.Type == 'MCQ':
					ans_set.append(ques_obj.Ans_opt)
				else:
					ans_set.append(','.join(ques_obj.Ans_opt))
				if ques_obj.neg_mark == 0:
					ans_set.append(str(ques_obj.corr_mark)+"/0")
				else:
					ans_set.append(str(ques_obj.corr_mark)+"/-"+str(ques_obj.neg_mark))
				ans_set.append(0)
			answer_data.append(ans_set)
		return True

	else:
		return False

def results(request):
	global answer_data
	if len(answer_data) == 0:
		return redirect("index")
	context = {'context': answer_data,
	'Total_pos': round(sum(float(l[-1]) for l in answer_data if float(l[-1]) > 0), 3),
	'Total_neg': round(sum(float(l[-1]) for l in answer_data if float(l[-1]) < 0), 3),
	'Total_marks': round(sum(float(l[-1]) for l in answer_data),3)}
	answer_data = []
	return render(request, 'rpspgate/results.html', context)

def errors(request):
	global answer_data 
	answer_data = []
	if request.method == "POST":
		link = request.POST['link']
		Response_sheet.objects.create(Link=link)
		return redirect("index")
	return render(request, 'rpspgate/error.html')