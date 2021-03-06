 파이썬 가상환경 설정 시 실수로 py_kakako_info 로 설정

# 카톡분석기 (talk_info)

-처음은 개인 대 개인의 대화를 분석하는 버전으로 제작

파이썬으로 기본적인 코드를 짠 뒤 실행해보고 이를 코틀린으로 변환 한 뒤

ui디자인을 하여 앱으로 만들고자 함이 최종목표

예상제작기간 약 1달 이내

readme는 사실 log와 비슷한 느낌으로 작성하고 있다...

---

## 만들고자 하는 것

### 1. 선톡 비율 : 조건 n시간 이상 대화가 없던 다음 톡을 했을 때 누가 먼저 톡을 보냈는가에 따라

###2. 대화량 비교 : 이모티콘, "ㅋㅋㅋ", "ㅎㅎㅎ" 을 제외한 대화 중에서 누가 더 많은 말을 하였는가

### 3. 대화 시간대 분석 : 일주일 평균적으로 몇시 쯤에 대화를 많이 나누었는지

### 4. 대화 요일 분석 : 하루를 오전 6시로 나누며 무슨 요일 대화가 자주했는지 

### 5. 특별한 대화 분석 : 시간대를 기준으로 평소와 다른 패턴의 대화가 있었던 날을 검색 후 출력

### 6. 단어 사용량 분석 : 어떤 단어를 누가 더 많이 썼는지, 가장많이 사용한 단어는 무엇인지 분석

---

#개발일지

>2020 9월 4일

>>1. 단체대화방을 기준으로 대화량을 분석해 누가 말을 많이하는지에 대해 나타내고자함

>>하지만 readlines()에서 에러가 발생하여 파일 내용이읽어지지 않는 문제발생

>>cp949코덱으로 인코딩 된 파일(카톡 내보내기를 통해서 나온 파일이였다.)을 utf-8로 변환해줘야했다


>>2. 날짜 데이터를 추출하는 부분을 만듬 빠른 추출을 위해서는 index를 적게쓰는 것이 좋지만 일단은
>>     나름의 범용성 추구를 위해서 이런 식으로 구상


---

#구조도

대화  "0000년 0월 00일 00 00:00, 000(이름) : ~~~~\n"

readline으로 읽기로 결정, 이후 dataclass 라이브러리, date 라이브러리를 이용

talk_data 저장 

num : (몇번째 대화인지)
date : 날짜
name : 이름
talk_type : (사진,동영상,이모티콘,도배,웃음반응,메세지)
massage : 메세지가 아닐경우 None을 입력, 메세지일경우 메세지 넣기

talk_data_making() :
1. 첫 시작부분이 0000년이 아닐경우 ->(넘김)
2. 날짜 이름 등 입력, talk_type = 0으로 설정
3.msg가 사진,이모티콘,동영상일 경우 msg를 none으로 변경하고 talk_type을 해당과 맞게 수정
4.위의 repeat_msg_num번의 대화에서(초기에 설정해둔다) msg가 같을경우 talk_type을 도배로 설정
   이때 msg내용은 남겨둔다
5.추후 웃음에 대한 반응 추가하기 (ㅋ,ㅎ 등에 대한 판별)

---

#9월 10일

index의 잦은 사용은 속도를 감소시키는 요인이 되므로 처음 한번에 필요한 값을 전부 찾는다

찾아야하는 값 23번째 이내에 '년','월','일','오전'or'오후',  ','  , ':'

---

#9월 11일

어제의 문제점을 고치면서 (보통 슬라이싱을 하면서 생기는 번호? 문제) 진행중

반복물을 잘 돌다가 어느 순간 별로 다르지 않은데 갑자기 '0'을 더 넣어주는 구문 (97줄)에서

작동이 안된다 (약 1000번째 라인에서) 이유를 모르겠다.

, 부분을 기준으로 이름과 날짜를 구분하는 기준을 세우는데 이때의 조건문이 i>15 or i<= 23으로 되어있어서

15번째 이후의 쉼표 중 제일 마지막의 쉼표를 인식하기에 이런 일이 발생하였다

print 문을 이용해 테스트 해본 결과 알 수 있었다.


---

#9월 14일

talk_rate 제작중

talk_maked_list를 완성한 줄 알았으나 모든 대화내역을 제일 마지막 대화로 바꾸어버리는 오류가 발생

원인을 찾고 있다.

---

#9월 15일

pandas와 plotly를 이용한 시각화.

pandas의 자료구조를 활용하여 데이터를 표현해보려고 한다.


---

#9월 16일

시간대별로 누가 얼마나 톡을 하였나 정리하려고 한다.
dictionary자료형을 쓰려고 생각해보았으나 중복되는 값이 있을 수 있을 것같아서 안된다고 생각

인원수가 가변형이라는 것이 생각을 복잡하게 만든다

talk_time에 대한 시간이 비정상적으로 길어지고 있다. 원인을 찾아낼 필요가 있다. (약 3년 이상의 자료를 분석한다면 
굉장히 오랜 시간이 걸릴 것이다)

모든 이름을 새로운 함수로 생각하고 있다 (디버그 결과) 수정요망ㄱ

#9월 17일

개개인의 데이터를 날짜로 변환한 뒤 그래프에 적용 식키기 위한 작업으 하였으며

이제 trace를 각각 생성하여 표에 적용시키는 작업을 하면된다.

추후 만들것은 1시간단위, 10분단위의 그래프를 그려내려고 한다.

#9월 18일

변수 동적할당과 호출을 통해서 하루동안 채팅한 개개인의 그래프를 그려내기 성공했다.

추가로 1시간단위, 10분단위, 지정날짜만 보는 기능과 pyqt를 이용해 gui로 능동적으로 데이터를

생성해내는 기능을 만들고자한다.