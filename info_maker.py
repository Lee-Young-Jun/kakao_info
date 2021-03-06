#test 모듈
#단체 대화방에서 대화의 정도를 분석하도록 한다.
#카톡 데이터의 구조 : 0000년 0월 00일 오전 00:00, 000 : ~~~~

from dataclasses import dataclass
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
import sys

@dataclass(frozen=True)
class talk_data_type:
    num : int
    talk_date : datetime.date
    talk_time : datetime.time
    name: str
    talk_type : int # 0:메세지 1:이모티콘 2:사진 3:동영상 ## 여기까지 구현 4:도배 5:웃음
    msg : str

    # 예시
    # num : 11
    # talk_data : date(2020년 5월 5일)
    # name : 이영준
    # talk_type : 0(메세지)
    # msg : '아 배고프농'

def talk_data_making(talk_address) :


    f = open(talk_address,'r',encoding='UTF8') #인코딩을 변환해주지않으면 오류가 생긴다


    making_data = list()
    num = 0



    while True:


        line = f.readline()
        if not line : break


        try :
            is_msg = line.index(',')
        except :
            is_msg = None

        if  is_msg == None or is_msg >= 23:
            pass  # 정상대화가 아닌 날짜변경로그거나 저장한 날짜등을 표시하는 경우 카운팅하지않고 넘긴다


        # 비정상 대화 필터링
        elif not line[0:4].isdigit() :
            pass

        elif line[4] != '년' :
            pass

        elif line.count(':') == 1 :
            pass

        else :
            y_n = None
            m_n = None
            d_n = None
            ap_m = None #오전오후
            name_dot = None
            msg_spliter = list()




            # 년 월 일 오전or오후 ","  ":' 찾는다

            for i in range(len(line)) :
                if i <= 15 :  # 최대 23번째이전에 있는 값들로 사용
                    if line[i] == '년':
                        y_n = i
                    if line[i] == '월':
                        m_n = i
                    if line[i] == '일':
                        d_n = i
                    if line[i] == '오':
                        ap_m = i #ap_m은 보정이 끝나면 '오' 바로 앞의 ' '에서 끝이난다 주의

                elif i>15 and i<=23 :
                    if line[i] == ',':
                        name_dot = i


                if line[i] == ':':   # 여러개의 ':'표시가 나올 수 있으므로 2번째 값을 가지도록 한다.
                    msg_spliter.append(i)

            #날짜 시간 정렬 ( 1일 -> 01일 )  뒤의 찾은 값들도 전부 더해준다
            if m_n-y_n == 3 : # 월 앞에 0을 삽입시켜준다
                line = line[:y_n+2]+'0'+line[y_n+2:]
                m_n+=1
                d_n+=1
                ap_m+=1
                name_dot+=1
                msg_spliter[1]+=1

            if d_n-m_n == 3 : # 일 앞에 0을 삽입시켜준다
                line = line[:m_n+2]+'0'+line[m_n+2:]
                d_n += 1
                ap_m += 1
                name_dot += 1
                msg_spliter[1] += 1



            if name_dot - ap_m == 7:
                line = line[:ap_m+3]+'0'+line[ap_m+3:]
                name_dot +=1
                msg_spliter[1] += 1




            data_ing_talk_date = datetime.date(int(line[y_n-4:y_n]),int(line[m_n-3:m_n]),
                                     int(line[d_n-3:d_n]))


            # 시간 데이터 추출


            if line[ap_m:ap_m+2] == '오후' :
                if int(line[ap_m+3:ap_m+5]) != 12 : # 오후이면서 12시가 넘는 경우 시간 +12를 해서 24hr방식으로 표현
                    data_ing_talk_time = datetime.time(int(line[ap_m+3:ap_m+5])+12,int(line[ap_m+6:ap_m+8]),0)
                else :
                    data_ing_talk_time = datetime.time(int(line[ap_m+3:ap_m+5]),int(line[ap_m+6:ap_m+8]),0)

            else:
                data_ing_talk_time = datetime.time(int(line[ap_m + 3:ap_m + 5]), int(line[ap_m + 6:ap_m + 8]), 0)


    ##############             몇번째 대화인지
            num = num + 1
            data_ing_num = num


    ##############            이름 설정

            data_ing_name = line[name_dot+2:msg_spliter[1]]

    ##############           메세지 처리

            data_ing_talk_type = 0

            data_ing_msg = line[msg_spliter[1]+2:]

            if data_ing_msg == '이모티콘' :
                data_ing_talk_type = 1
            if data_ing_msg == '사진' :
                data_ing_talk_type = 2
            if data_ing_msg == '동영상' :
                data_ing_talk_type = 3


            making_data.append(talk_data_type(data_ing_num,data_ing_talk_date,data_ing_talk_time,data_ing_name,data_ing_talk_type,
                                              data_ing_msg))


    return making_data

    f.close()

# 지금까지 txt파일에서 대화 데이터를 읽는 부분##
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

def talk_rate(talk_maked_list) : #누가 톡을 얼마나 했는지 return

    name_dic = {} #딕셔너리 자료형


    for i in range(len(talk_maked_list)) :

        if not (talk_maked_list[i].name in name_dic): #딕셔너리 안에 이름이 없을 경우 이름을 추가해준다.
            name_dic.setdefault(talk_maked_list[i].name)

        num = name_dic.get(talk_maked_list[i].name)

        if num == None :
            num = 0

        name_dic.update({talk_maked_list[i].name : num+1}) #이전 값을 get 하고 1을 더해준다.

    counted_talk = list()

    for key, value in name_dic.items() :
        counted_talk.append([key, value])

    return sorted(counted_talk, key = lambda x : -x[1])

def talk_rate_graph(talk_rate_list) :
    name = []
    num = []

    for i in range(len(talk_rate_list)) :
        name.append(talk_rate_list[i][0])
        num.append(talk_rate_list[i][1])

    #정수의 가장 높은 자릿수를 기준으로 반올림한다
    max_rate = talk_rate_list[0][1]
    max_range = (int(str(max_rate)[0]) + 1) * (10 ** (len(str(max_rate)) - 1))

    df = pd.DataFrame({'이름': name, '채팅횟수': num})


    # 그래프 그리는 부분

    trace = go.Bar(x=df['이름'], y=df['채팅횟수'])
    layout = {}
    layout.update({'xaxis':{'type': 'category'}})
    layout.update({'yaxis':{'range' : [0,max_range]}})
    fig = {'data' : [trace], 'layout' : layout}
    plot(fig)





def talk_time(talk_maked_list) : #언제 톡을 많이하는지 시간대 분석 return
    print('start')

    all_name = []
    name_list = []
    name_for_time = []

    for i in range(len(talk_maked_list)) :
        #print(i)

        all_name.append(datetime.datetime.combine(talk_maked_list[i].talk_date,talk_maked_list[i].talk_time))
        #print(talk_maked_list[i].name)
        #print(datetime.datetime.combine(talk_maked_list[i].talk_date,talk_maked_list[i].talk_time))

        if not talk_maked_list[i].name in name_list : #이름들을 중복을 막으며 리스트를 만든다
            name_list.append(talk_maked_list[i].name)
            name_for_time.append([])                #이중리스트를 제작시켜두고 시작

        if talk_maked_list[i].name in name_list :    #추가된 이름안에서 이중리스트 내에 시간을 추가해준다.
            name_for_time[name_list.index(talk_maked_list[i].name)].append(datetime.datetime.combine(talk_maked_list[i].talk_date,
                                                                                                    talk_maked_list[i].talk_time))

    # 1day graph
    one_day_counter = {} # '%Y,%m,%d,%H,%M'
    one_day_personal_counter = []
    one_day_personal_values = []


    for i in range(len(all_name)) :

        try :
            if all_name[i].strftime('%Y,%m,%d') in one_day_counter :
                one_day_counter[all_name[i].strftime('%Y,%m,%d')] += 1

            else :
                one_day_counter[all_name[i].strftime('%Y,%m,%d')] = 1

        except :
            print('error one day counter')
            one_day_counter[all_name[i].strftime('%Y,%m,%d')] = 1


    for i in range(len(name_list)) :

        one_day_personal_counter.append({})
        one_day_personal_values.append([])

        for j in range(len(name_for_time[i])) :


            try :
                if name_for_time[i][j].strftime('%Y,%m,%d') in one_day_personal_counter[i] :
                    one_day_personal_counter[i][name_for_time[i][j].strftime('%Y,%m,%d')] += 1

                else :
                    one_day_personal_counter[i][name_for_time[i][j].strftime('%Y,%m,%d')] = 1

            except :
                print('one day personal counter error occurrend')
        #그래프 그리기 부분

    one_day_keys = list(one_day_counter.keys())  #2~3일정도 톡을 한 날이 없다면 어떻게 되는가?
    one_day_values = list(one_day_counter.values())

    one_day_max_rate = max(one_day_values)
    one_day_max_range = (int(str(one_day_max_rate)[0])+1)*(10**(len(str(one_day_max_rate))-1))



    for i in range(len(name_list)) :
        for j in range(len(one_day_keys)) :
            if one_day_keys[j] in one_day_personal_counter[i] :
                one_day_personal_values[i].append(one_day_personal_counter[i][one_day_keys[j]])

            else :  #그 날짜에 한 말이 없다면
                one_day_personal_values[i].append(0)


    one_day_df = pd.DataFrame({'일' : one_day_keys, '채팅횟수' : one_day_values})

    for i in range(len(name_list)) : #동적 변수생성으로 dataframe을 생성해낸다.
        globals()['one_day_personal_df_{}'.format(i)] = pd.DataFrame({'일' : one_day_keys, '채팅횟수' : one_day_personal_values[i]})
    #print(one_day_personal_df_1)
    #print(type(one_day_personal_df_16))

    trace_all = go.Scatter(x=one_day_df['일'],y=one_day_df['채팅횟수'],name='전체인원대화수')

    for i in range(len(name_list)) : #17명일경우 16까지 생성됨
        globals()['trace{}'.format(i)] = go.Scatter(x=getattr(sys.modules[__name__],'one_day_personal_df_{}'.format(i))['일'],
                                                    y=getattr(sys.modules[__name__],'one_day_personal_df_{}'.format(i))['채팅횟수'],
                                                    name=name_list[i])

    one_day_layout = {}
    one_day_layout.update({'xaxis' : {'type' : 'category'}})
    one_day_layout.update({'yaxis' : {'range' : [0,one_day_max_range]}})

    datas = [trace_all]

    fig = {'data' : datas, 'layout' : one_day_layout}

    for i in range(len(name_list)) :
        datas.append(getattr(sys.modules[__name__],'trace{}'.format(i)))

    plot(fig)






    # 1hour graph

    # 10min graph






def talk_first_rate(talk_maked_list) : #선톡 비중에 대한 return
    pass

#### main
if __name__ == "__main__" :

    talk_maked_list = talk_data_making("C:/Users/이영준/Desktop/kakao_info/all_talk.txt")


    print(talk_rate(talk_maked_list))

    #talk_rate_graph(talk_rate(talk_maked_list))

    talk_time(talk_maked_list)

