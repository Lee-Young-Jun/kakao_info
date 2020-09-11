#test 모듈
#단체 대화방에서 대화의 정도를 분석하도록 한다.
#카톡 데이터의 구조 : 0000년 0월 00일 오전 00:00, 000 : ~~~~

from dataclasses import dataclass
import datetime

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
    print('open')

    maked_data = list()
    num = 0

    while True:

        line = f.readline()
        if not line : break


        data_ing = talk_data_type

        try :
            is_msg = line.index(',')
        except :
            is_msg = None

        if  is_msg == None or is_msg >= 23:
            pass  # 정상대화가 아닌 날짜변경로그거나 저장한 날짜등을 표시하는 경우 카운팅하지않고 넘긴다

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
                print('0넣엇다')



            data_ing.talk_date = datetime.date(int(line[y_n-4:y_n]),int(line[m_n-3:m_n]),
                                     int(line[d_n-3:d_n]))


            # 시간 데이터 추출


            if line[ap_m:ap_m+2] == '오후' :
                if int(line[ap_m+3:ap_m+5]) != 12 : # 오후이면서 12시가 넘는 경우 시간 +12를 해서 24hr방식으로 표현
                    data_ing.talk_time = datetime.time(int(line[ap_m+3:ap_m+5])+12,int(line[ap_m+6:ap_m+8]),0)
                else :
                    data_ing.talk_time = datetime.time(int(line[ap_m+3:ap_m+5]),int(line[ap_m+6:ap_m+8]),0)

            else:
                data_ing.talk_time = datetime.time(int(line[ap_m + 3:ap_m + 5]), int(line[ap_m + 6:ap_m + 8]), 0)


    ##############             몇번째 대화인지
            num = num + 1
            data_ing.num = num


    ##############            이름 설정

            data_ing.name = line[name_dot+2:msg_spliter[1]]

    ##############           메세지 처리

            data_ing.talk_type = 0

            data_ing.msg = line[msg_spliter[1]+2:]

            if data_ing.msg == '이모티콘' :
                data_ing.talk_type = 1
            if data_ing.msg == '사진' :
                data_ing.talk_type = 2
            if data_ing.msg == '동영상' :
                data_ing.talk_type = 3


            maked_data.append(data_ing)


    f.close()

# 지금까지 txt파일에서 대화 데이터를 읽는 부분##
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################

