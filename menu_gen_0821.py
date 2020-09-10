"""
Virtual recipe Generator for program running test(TUI running only_This file have no connected GUI code).

메인 프로그램의 정상 구동여부를 확인하기 위해, 메뉴디렉터리와 해당 디렉터리 하위의 레시피 txt파일들을 자동 생성한다.
추후 크롤링으로 진짜 레시피를 가져올 수도 있겠지만, 일단은 랜덤 모듈을 사용하여 메뉴명(=파일명), 재료, 요리절차를 모두 무작위로 생성하려 한다.
무작위 생성 중 중복 발생시에는 덮어씌우기를 허용한다(기본 "w" 모드).

$ python menu_gen_(date).py
작성자 : hekim
작성기록 : 2020-08-17 (ver.1), (ver.1.1_재료들 중복제거)
         2020-08-18 (ver2_menu디렉터리 생성코드 추가, 메뉴명을 알파벳이 아닌 한글로 무작위 생성하도록 변경)
         2020-08-18 (ver2.1_주석 수정 작업) _ 최종
         2020-08-21 (ver3_주석 수정)
"""
#!/usr/bin/env python3

import random, sys, os
# sys모듈은 오류 발생시 강제종료를 위해 사용하였음
# 디렉터리 생성 명령을 위해 os 모듈 추가함

#####################################▼   함 수 (functions)   ▼#########################################################

# 영어 알파벳으로 이루어진 메뉴명(이자 텍스트 파일 제목) 생성 함수 _ 한글로 생성시에는 gen_fname_v2()를 써야함
# English recipe name generating code (if want Korean menu name, use gen_fname_v2())
def gen_fname():
    alpha = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    f = ""
    for i in range(random.randrange(3,8)):
        f = f + random.choice(alpha)
    return f

# 무작위 한글로 이루어진 메뉴명 생성 함수
# Random Korean recipe name generating code
def gen_fname_v2():
    f = ""
    suffix = ["국", "볶음", "찌게", "탕", "나물", "무침", ""]
    for i in range(random.randrange(1,4)):
        f = f + chr(random.choice(range(44032, 55203))) #ord('가')~ord('힣')가 44032~55203임
    f = f + random.choice(suffix)
    return f

# 정해진 pool(리스트)에서 무작위 재료들을 선택하여 한 줄의 재료 리스트를 생성하는 함수.
# Randomly generate 'ingredient list(variable name = ingred)' from the ingredients.
def gen_ingrd():
    ingredients = ["파", "우유", "양파", "오이", "두부", "계란", "당근", "시금치", "콩나물", "감자", "무", "가지", "양배추", "어묵", "대파"]
    ingred = []
    for i in range(random.randrange(1, 14)):
        temp = random.choice(ingredients)
        if temp not in ingred:
            ingred.append(temp)
        else:
            pass
    return ingred

# 레시피 문장을 무작위로 생성하는 함수. 띄어쓰기 서식을 포함한 strings 타입으로 저장된다
# Randomly generate lines of recipe sentence, return one 'strings' type variable(name = proced_r) contain '\n'
def gen_recip(ingred):
    """
    :param ingred: 위 무작위 재료 리스트 생성 함수인 gen_ingred()의 return값이 전달되어야 한다.
    :return:
    """
    proced = ["를 깨끗이 세척한다", "를 잘게 썬다", "를 슬라이스 친다", "의 껍질을 벗겨낸다", "를 무친다", "를 섞는다", "를 데친다", "를 볶는다", "를 끓인다", "를 부친다",
              "를 졸인다", "를 냄비에 넣는다", "를 후라이팬에 넣는다"]
    proced_r = ""
    for i in range(0, len(ingred)):
        proced_r = proced_r + random.choice(ingred) + random.choice(proced) + "\n"
    return "\n"+proced_r

# 무작위로 생성된 재료 '리스트'를 문자열 형태로 텍스트 파일에 저장하기 전 가공을 위한 함수이다.
# 본 함수를 적용하지 않는다면 "["양파", "계란"]"과 같은 형태로 기록 되나, 본 함수를 적용 시, "양파, 계란" 과 같이 깔끔한 형태로 기록 된다.
# Convert List type variable into Strings type so that eliminate '[' and ']' character for easy usage of data.
# for example, f.readline().split(",")
def list_into_str(ingred):
    """
    :param ingred: gen_recip(ingred)함수와 같이, gen_ingred()의 return값이 전달되어야 한다.
    :return:
    """
    ing = ""
    for i in ingred:
        ing = ing + "," + i
    return ing[1:]

# 랜덤하게 생성한 메뉴명, 재료목록, 레시피들을 활용하여 파일을 생성하고 데이터를 기록하는 함수이다.
# Generate text file and write ingredients and recipe in that file.
def gen_file(ing, rec):
    fname = gen_fname_v2()  #영문 메뉴 생성은 gen_fname()
    with open(".\\menu\\{}.txt".format(fname), "w") as f:
        f.write(list_into_str(ing))
        f.write(rec)


#####################################▼      메 인 코 드 (main code)     ▼##############################################

# 'menu'디렉터리 생성 코드 (사용자 텍스트 인터페이스 전에 배치하여 프로그램 구동 시 사전 실행되도록 한다)
# 다음을 참조함 _ https://cinema4dr12.tistory.com/1296
# Generate 'menu' directory.
try:
    if not(os.path.isdir(".\\menu")):
        os.makedirs(os.path.join(".\\menu"))
except OSError as e:
    if e.errno != errno.EEXIST:
        print("디렉터리 생성에 실패하였습니다.\nmenu폴더를 삭제 후 프로그램을 다시 실행해 주세요.")
        raise

# 사용자가 접하는 텍스트 인터페이스에 해당하는 코드이다.
# 몇 개의 레시피 텍스트 파일들을 생성할지 물어본 뒤, 파일들을 생성해 낸다(숫자 외 키 입력, 0이하의 수 입력 시 오류메시지 출력).
# TUI Code for get data(Number of recipes will generate) from user.
# Only can input number(1~∞), and if not, return error message.
try:
    print("몇 개의 랜덤 레시피를 생성하시겠습니까?")
    n = int(input("숫자만 입력해 주세요: "))
    if n <= 0:
        print("0 또는 마이너스 갯수를 희망하셨으므로 아무것도 생성하지 않습니다.\n프로그램을 종료합니다.")
        sys.exit()
    else:
        for i in range(n):
            ingredients = gen_ingrd()
            recipe = gen_recip(ingredients)
            gen_file(ingredients, recipe)
        print("생성 완료! menu 폴더 안을 확인해보세요~")
except ValueError:
    print("숫자만 입력해야 합니다. 프로그램을 종료합니다.")
    sys.exit()

######################################  end of program  ################################################################

signal = "a"
while signal != "q":
    signal = input("끝내시려면 q를 입력하세요: ")

print("종료")