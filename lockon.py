from bs4 import BeautifulSoup
import pandas as pd
import requests
import datetime
import re

def lockon(username, password) :
    # 계정 정보
    parameter = {'username': username, 'password': password}
    login_url = "https://myclass.ssu.ac.kr/login/index.php"  # 로그인 주소
    myclass_url = "http://myclass.ssu.ac.kr/"  # 스마트캠퍼스 주소

    # 주차 정보를 가져오기 위한 정보
    start_date = datetime.datetime(2021, 3, 1)  # 개강 일자
    today_date = datetime.datetime.today()  # 오늘 일자
    week = int((today_date - start_date).days / 7) + 1  # 오늘 주차

    # 로그인 세션 유지
    session = requests.session()
    session.post(login_url, data=parameter)

    # 과목 정보를 가져오기 위해 먼저 스마트캠퍼스를 접속
    res = session.get(myclass_url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    # 해당 주차 출석 정보를 가져오기 위한 셀렉터 정보
    # query = "#ubcompletion-progress-wrapper > div:nth-child(2) > table > tbody > tr:nth-child(" + str(week) + ") > td:nth-child(5)"
    # query2 = "#ubcompletion-progress-wrapper > div:nth-child(2) > table > tbody > tr:nth-child(" + str(week+1) + ") > td:nth-child(5)"
    query3 = "#ubcompletion-progress-wrapper > div:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(5)"
    # 위에 query3은 1주차만 가져오게 해놨음. 현재 금주차로 적용을 해야하는데, 과목마다 강의 올라오는 갯수가 달라 테이블 셀렉터가 비규칙적임.

    tmp_dict = {}
    res_list = []

    #과목 리스트 별 출석 정보 가져오기
    for href in soup.find("div", class_="course_lists").find_all("li"):
        id = re.findall("\d+", href.find("a")["href"])
        attendance_url = "http://myclass.ssu.ac.kr/report/ubcompletion/user_progress_a.php?id=" + str(id[0])
        res = session.get(attendance_url)
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')

        result = soup.select_one(query3)
        if result is None :
            continue
        result_title = soup.select_one("#page-header > nav > div > div.coursename > h1 > a")

        tmp_dict["result"] = result.get_text()
        tmp_dict["title"] = result_title.get_text()

        res_list.append(tmp_dict)
        tmp_dict = {}

    return res_list