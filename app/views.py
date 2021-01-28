import os
import random
import winsound
import pyglet
from PIL import Image
from fileinput import filename
from io import BytesIO
from playsound import playsound
import pandas as pd
from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect, StreamingHttpResponse
from django.shortcuts import render
from django.templatetags.static import static
import xlwt
from xlsxwriter import Workbook

from django.http import HttpResponse
from django.contrib.auth.models import User
from app.models import Result, Verylucky

from django.contrib.staticfiles import finders
from django.urls import reverse

# Create your views here.

prizes = []
people = []
rest = []
# prizes_n = {'王國維':'金元寶一枚'}
prizes_n = {}
# 中獎人
w = []
# 獎品
w_p = []

path = os.path.dirname(os.path.abspath(__file__))


def index(request):
    winsound.PlaySound(path + '/static/app/welcome.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
    return render(request, "app/index.html", {
        "output": prizes_n
    })

def draw(request):
    # winsound.PlaySound(path + '/static/app/bigwinBgm.mp3', winsound.SND_ASYNC | winsound.SND_ALIAS)
    result = finders.find('app/PEOPLE_LIST.txt')
    result2 = finders.find('app/PRIZE_LIST.txt')
    searched_locations = finders.searched_locations
    with open(result, 'r', encoding='utf-8') as in_file:
        for line in in_file.readlines():
            line = line.strip('\n\r')
            line = line.strip('\ufeff')
            people.append(line)
    with open(result2, 'r', encoding='utf-8') as in_file:
        for line in in_file.readlines():
            line = line.strip('\n\r')
            line = line.strip('\ufeff')
            prizes.append(line)
    random.shuffle(prizes)
    random.shuffle(people)
    while len(prizes) > 0 and len(people) > 0:
        win_prize = random.choice(prizes)
        w_p.append(win_prize)
        winner = random.choice(people)
        w.append(winner)
        prizes_n[winner] = win_prize
        prizes.remove(win_prize)
        people.remove(winner)
        rest = people

    # 把資料存入DB(model: Result)
    for i in prizes_n:
        r = Result()
        # print(i, prizes_n[i])
        r.prize = i
        r.winner = prizes_n[i]
        r.save()

    # 把資料存入DB(model: Verylucky)
    for j in people:
        v = Verylucky()
        v.luckymen = j
        v.save()

    # 人配獎品
    print(prizes_n)
    # 還沒被抽的(剩下的獎)
    # print(prizes)
    # 還沒被抽的(剩下的人)
    print(rest)
    if not prizes:
        print("第一波抽獎結束!")
        # messages.info(request, "抽獎結束囉")
    return HttpResponseRedirect(reverse('list'))
    # return render(request, "app/list.html", {
    #     "luckymen": rest,
    #     "output": prizes_n
    # })

def list(request):
    playsound(path + '/static/app/roll.mp3')
    # winsound.PlaySound(path + '/static/app/roll.wav', winsound.SND_ASYNC | winsound.SND_ALIAS)
    winsound.PlaySound(path + '/static/app/tolist.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
    return render(request, "app/list.html", {
        "luckymen": people,
        "output": prizes_n
    })

def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="result.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('中獎名單')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['中獎人', '贊助獎品', '中獎人簽收欄']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Result.objects.all().values_list('prize', 'winner')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

def export_users_xls_verylucky(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="verylucky.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('未中獎名單')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['未中獎人', '贊助獎品', '中獎人簽收欄']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    rows = Verylucky.objects.all().values_list('luckymen')
    # print(rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response
