from PIL import Image
import pytesseract as tess
import re
import pandas as pd
import os

date_path = os.getcwd()
image_path = os.getcwd()+'\\image'

def accuracy(x, y):
    if len(x) == len(y):
        cnt = 0
        for i in range(len(x)):
            if x[i]==y[i]:
                cnt += 1
                
        per = cnt/len(x)
        per = per*100
        per = round(per, 1)
                
    else:
        print('문자의 길이를 맞춰주세요!')
        
    return per

def for_number(x,y):

    n = len(x)
    lst=[]
    
    for i in range(len(y)): 
        if len(y[i:i+n]) == len(x):
            lst.append(y[i:i+n])
    
    
    y = lst
    acc_list = []
    
    for i in y:                           # accuracy x와 y를 비교해서 반환
        acc_list.append(accuracy(x,i))
        
    maximum = max(acc_list)   
    
    return y[acc_list.index(maximum)], maximum   # 일치율이 가장 높은 애와 일치율을 반환


#############################송성곤 정의 함수#######################################
##################################문자용############################################
####################################################################################

def only_text(text):
    a1 = re.compile('\D')
    b1 = a1.findall(text)
    str1 = ''
    for i in b1:
        str1 += i

    a2 = re.compile('\w')
    b2 = a2.findall(str1)
    str2=''
    for i in b2:
        str2 += i
    return str2

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = [' ','ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = [' ','ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

def kte(x, y):
    
    x1 = only_text(x)
    y1 = only_text(y)
    
    r_lst_1 = []
    for w in list(x1.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst_1.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst_1.append([w])
    
    
    
    
    r_lst_2 = []
    for w in list(y1.strip()):
        ## 영어인 경우 구분해서 작성함. 
        if '가'<=w<='힣':
            ## 588개 마다 초성이 바뀜. 
            ch1 = (ord(w) - ord('가'))//588
            ## 중성은 총 28가지 종류
            ch2 = ((ord(w) - ord('가')) - (588*ch1)) // 28
            ch3 = (ord(w) - ord('가')) - (588*ch1) - 28*ch2
            r_lst_2.append([CHOSUNG_LIST[ch1], JUNGSUNG_LIST[ch2], JONGSUNG_LIST[ch3]])
        else:
            r_lst_2.append([w])
            
    
    fx = ''
    fy = ''
    for i in r_lst_1:
        for j in i:
            fx += j
            
    for i in r_lst_2:
        for j in i:
            fy += j
        

        
    # fx의 길이만큼 fy를 자른 fy_list

    n = len(fx)
    fy_list=[]
    for i in range(len(fy)): 
        if len(fy[i:i+n]) == len(fx):
            fy_list.append(fy[i:i+n])
    
    
    
    # 그럼 fx랑 fy_list가 나왔음
    acc_list = []
    
    
    for i in fy_list:
        cnt = 0
        per = 0
        if len(fx) == len(i):
            for j in range(len(i)):
                if fx[j] == i[j]:

                    cnt += 1
                    per = cnt / len(fx)
                    per = per * 100
                    per = round(per, 1)
                
            
        acc_list.append(per)
    
    if not acc_list:
        acc_list=[0]
    maximum = max(acc_list)             # 일치율
    
    idx = acc_list.index(maximum)       # 일치율이 가장 높은 애의 fy_list에서의 인덱스값
    

    try:
        acc_word = fy_list[idx]
    except: # 맞는 애가 str로 늘어져있는 거
        acc_word = ' '
#     return maximum, idx, fy_list[idx], r_lst_2   #  r_lst_2 는 원래 토막나있는 그거

    str_cnt = 0
    temp1 = []
    temp2 = []
    for i in acc_word:
        temp1.append(i)
        str_cnt += 1
        if str_cnt == 3:
            temp2.append(temp1)
            temp1=[]
            str_cnt = 0
    
  
    acc_list2 = []
    for i in temp2:
        
        ac_idx = r_lst_2.index(i)
        acc_list2.append(ac_idx)
        
        
    final = ''
    
    for i in acc_list2:
        final += y1[i]

    return final, maximum

df = pd.read_csv(date_path+'/result.csv', encoding='cp949')

## 찐
app_list1 = []
app_list2 = []
name_list = []
num_list = []
class_list = []
ind_list = []
rep_list = []

rname_list = []
rnum_list = []
rclass_list = []
rind_list = []
rrep_list = []

cnt_list = []


for i in range(len(df)):
    print(i)
    img = Image.open(image_path + '/' + str(i) + '_2.jpg')
    text = tess.image_to_string(img,lang='kor')

    
    
    app_num = df.iloc[i,0]
    
    
    
    realName = df.iloc[i,1]
    rname_list.append(realName)
    
    realNum = df.iloc[i,2]
    realNum = str(realNum)
    realNum = realNum[:3] + '-' +realNum[3:5] + '-' +realNum[5:10]
    rnum_list.append(realNum)
    
    realClass = df.iloc[i,3]
    rclass_list.append(realClass) 
    
    realIndust = df.iloc[i,4][4:].replace(' ','')
    rind_list.append(realIndust)
    
    realRep = df.iloc[i,5]
    rrep_list.append(realRep)
    
    
    
    if text == '\x0c':
        app_list1.append(app_num)
        app_list2.append(' ')
        name_list.append('미제출')
        num_list.append(' ')
        class_list.append(' ')
        ind_list.append(' ')
        rep_list.append(' ')
        cnt_list.append(0)
    else:
        cnt = 0
        
        # 접수번호
        app_list1.append(app_num)
        app_list2.append(' ')
        
        
        
        # 기업명
        simName, percent = kte(realName, text)
        name_list.append(simName)
#         print(simName, percent)
        if percent >= 75:
            cnt += 1        
        
        # 사업자번호
        simNum, percent = for_number(realNum, text)
#         print(simNum, percent)
        num_list.append(simNum)
        if percent >= 75:
            cnt += 1        


        #기업구분
        simClass, percent = kte(realClass, text)
        class_list.append(simClass)
#         print(simClass, percent)
        if percent >= 75:
            cnt += 1



        # 산업구분
        simInd, percent = kte(realIndust, text)
        ind_list.append(simInd)
#         print(simInd, percent)
        if percent >= 75:
            cnt += 1


        # 대표자명
        simRep, percent = kte(realRep, text)
        rep_list.append(simRep)
#         print(simRep, percent)
        if percent >= 75:
            cnt += 1





        cnt_list.append(cnt)
        
data = pd.DataFrame(columns=['접수번호','기업명','사업자번호','기업구분','업종구분','대표자명','일치개수'])

for i in range(0, len(df)):
    c = i*2
    data.loc[c] = [app_list1[i], rname_list[i],rnum_list[i],rclass_list[i],rind_list[i],rrep_list[i],cnt_list[i]]
    data.loc[c+1] = [app_list2[i], name_list[i],num_list[i],class_list[i],ind_list[i],rep_list[i],'']
    
data.to_excel(date_path+'/final.xlsx', header=True, index=False, encoding='cp949')

print('대조 완료')