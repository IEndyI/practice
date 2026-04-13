import os

all_inputs = []

def 입력_받기_프롬프트(prompt):
    user_input = input(prompt)
    all_inputs.append(user_input)
    return user_input

map_data = [
    ["", "", "", "", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스병원"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", ""],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", ""],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", "", ""]
]

row = 6
col = 0
hp = 10
account_balance = 50000
inventory = []
quests = []
current_time = "11시"
settings_difficulty = "보통"
settings_gate_visited = False

종료신호가_없음 = True

def 초기_설정():
    global settings_difficulty
    while True:
        diff = 입력_받기_프롬프트("난이도를 선택하세요 (쉬움, 보통, 어려움): ")
        if diff == "쉬움" or diff == "보통" or diff == "어려움":
            settings_difficulty = diff
            break
        else:
            print("잘못된 입력입니다. '쉬움', '보통', '어려움' 중에서 입력해주세요.")

def 상태_출력_작업():
    print("● 계좌의 잔액: " + str(account_balance) + "원")
    print("● HP: " + str(hp))
    위치 = map_data[row][col]
    print("● 현재위치: " + 위치)
    
    print("● 동서남북 이웃 칸의 위치 이름:")
    if col + 1 < len(map_data[0]):
        if map_data[row][col+1] != "":
            print("  - 동: " + map_data[row][col+1])
    if col - 1 >= 0:
        if map_data[row][col-1] != "":
            print("  - 서: " + map_data[row][col-1])
    if row + 1 < len(map_data):
        if map_data[row+1][col] != "":
            print("  - 남: " + map_data[row+1][col])
    if row - 1 >= 0:
        if map_data[row-1][col] != "":
            print("  - 북: " + map_data[row-1][col])
    return None

def 임무_출력_작업():
    print("● 가지고 있는 임무 목록:")
    if len(quests) == 0:
        print("  없음")
    else:
        for q in quests:
            print("  - " + q)
    return None

def 이동_동_작업():
    return 이동_작업("동")

def 이동_서_작업():
    return 이동_작업("서")

def 이동_남_작업():
    return 이동_작업("남")

def 이동_북_작업():
    return 이동_작업("북")

def 이동_작업(방향):
    global row, col, hp, settings_gate_visited
    new_row = row
    new_col = col
    
    if 방향 == "북": 
        new_row = new_row - 1
    elif 방향 == "남": 
        new_row = new_row + 1
    elif 방향 == "동": 
        new_col = new_col + 1
    elif 방향 == "서": 
        new_col = new_col - 1
        
    갈수있음 = False
    if new_row >= 0 and new_row < len(map_data):
        if new_col >= 0 and new_col < len(map_data[0]):
            if map_data[new_row][new_col] != "":
                갈수있음 = True
                
    if 갈수있음 == True:
        row = new_row
        col = new_col
        hp = hp - 1
        curr_place = map_data[row][col]
        print("[" + curr_place + "](으)로 이동했습니다.")
        print("(HP 1 감소, 현재 HP: " + str(hp) + ")")
        
        if curr_place == "정문":
            퀘스트있음 = False
            for q in quests:
                if q == "독수리상에서 임무를 받고 이윤재관에 보고하기":
                    퀘스트있음 = True
                    
            if 퀘스트있음 == False and settings_gate_visited == False:
                quests.append("독수리상에서 임무를 받고 이윤재관에 보고하기")
                settings_gate_visited = True
                print("\n[임무 알림] 정문에 도착했습니다.")
                print("새로운 임무: 독수리상에서 임무를 받고 이윤재관에 보고하라.")
    else:
        print("그 방향은 막혔어.")
    return None

def 상호작용_작업():
    global account_balance, inventory, quests
    curr_place = map_data[row][col]
    
    if curr_place == "학생회관":
        print("학생회관에서는 물건을 구매할 수 있습니다.")
        while True:
            buy_choice = 입력_받기_프롬프트("무엇을 구매하시겠습니까? (1. 두쫀쿠(5000원), 2. 카페라떼(2500원), 3. 나가기): ")
            if buy_choice == "1" or buy_choice == "두쫀쿠":
                if account_balance >= 5000:
                    account_balance = account_balance - 5000
                    inventory.append("두쫀쿠")
                    print("두쫀쿠를 구매하여 가방에 넣었습니다.")
                else:
                    print("잔액이 부족합니다.")
            elif buy_choice == "2" or buy_choice == "카페라떼":
                if account_balance >= 2500:
                    account_balance = account_balance - 2500
                    inventory.append("카페라떼")
                    print("카페라떼를 구매하여 가방에 넣었습니다.")
                else:
                    print("잔액이 부족합니다.")
            elif buy_choice == "3" or buy_choice == "나가기":
                break
            else:
                print("잘못된 입력입니다.")
                
    elif curr_place == "독수리상":
        print("독수리상에서는 임무를 받을 수 있습니다.")
        while True:
            quest_choice = 입력_받기_프롬프트("어떤 임무를 받으시겠습니까? (1. 교내 부조리 수사, 2. 교내 위생사건 수사, 3. 나가기): ")
            if quest_choice == "1" or quest_choice == "교내 부조리 수사":
                퀘스트있음 = False
                for q in quests:
                    if q == "교내 부조리 수사":
                        퀘스트있음 = True
                
                if 퀘스트있음 == False:
                    quests.append("교내 부조리 수사")
                    print("임무 '교내 부조리 수사'를 받았습니다.")
                    print("  ● 교내 어딘가에서 부조리가 일어나고 있다.")
                    print("  ● 이동하고 상호작용을 해서 부조리를 찾아서 보고하라.")
                else:
                    print("이미 받은 임무입니다.")
                    
            elif quest_choice == "2" or quest_choice == "교내 위생사건 수사":
                퀘스트있음 = False
                for q in quests:
                    if q == "교내 위생사건 수사":
                        퀘스트있음 = True
                        
                if 퀘스트있음 == False:
                    quests.append("교내 위생사건 수사")
                    print("임무 '교내 위생사건 수사'를 받았습니다.")
                    print("  ● 학생들이 단체로 식중독에 걸렸다.")
                    print("  ● 이동하고 상호작용을 해서 위생사건의 원인을 찾아서 보고하라.")
                else:
                    print("이미 받은 임무입니다.")
                    
            elif quest_choice == "3" or quest_choice == "나가기":
                break
            else:
                print("잘못된 입력입니다.")
                
    elif curr_place == "이윤재관":
        보고할것있음 = False
        for q in quests:
            if q == "교내 부조리 수사 완료" or q == "교내 위생사건 수사 완료":
                보고할것있음 = True
                
        if 보고할것있음 == True:
            print("이윤재관에 사건의 원인을 훌륭하게 보고했습니다!")
            
            새로운_임무_목록 = []
            for q in quests:
                if q != "교내 부조리 수사 완료" and q != "교내 위생사건 수사 완료" and q != "독수리상에서 임무를 받고 이윤재관에 보고하기":
                    새로운_임무_목록.append(q)
            quests = 새로운_임무_목록
            
            print("보고 임무를 완수했습니다!")
        else:
            print("독수리상에서 임무를 받으세요.")
            
    elif curr_place == "공터1":
        부조리수사중 = False
        for q in quests:
            if q == "교내 부조리 수사":
                부조리수사중 = True
                
        if 부조리수사중 == True:
            print("이곳에서 누군가 부당한 거래를 하는 현장을 목격했습니다!")
            print("'교내 부조리 증거'를 발견했습니다. 이윤재관으로 돌아가 보고하세요.")
            quests.remove("교내 부조리 수사")
            quests.append("교내 부조리 수사 완료")
        else:
            print("상호작용할 수 없는 장소입니다.")
            
    elif curr_place == "공터2":
        위생수사중 = False
        for q in quests:
            if q == "교내 위생사건 수사":
                위생수사중 = True
                
        if 위생수사중 == True:
            print("버려진 상한 음식물 쓰레기통을 발견했습니다!")
            print("'위생사건 원인'을 찾아냈습니다. 이윤재관으로 돌아가 보고하세요.")
            quests.remove("교내 위생사건 수사")
            quests.append("교내 위생사건 수사 완료")
        else:
            print("상호작용할 수 없는 장소입니다.")
            
    else:
        print("상호작용할 수 없는 장소입니다.")
    return None

def 가방_작업():
    global hp, inventory
    if len(inventory) == 0:
        print("가방이 비어있습니다.")
    else:
        print("가방에 들어있는 물건들:")
        idx = 0
        for item in inventory:
            print(str(idx + 1) + ". " + item)
            idx = idx + 1
            
        choice = 입력_받기_프롬프트("사용할 물건의 이름 또는 번호를 입력하세요 (취소: 엔터): ")
        if choice != "":
            usable_item = ""
            if choice.isdigit() == True:
                번호 = int(choice)
                if 번호 >= 1 and 번호 <= len(inventory):
                    usable_item = inventory[번호 - 1]
            else:
                for item in inventory:
                    if choice == item:
                        usable_item = choice
            
            if usable_item != "":
                print("'" + usable_item + "'을(를) 사용했습니다.")
                inventory.remove(usable_item)
                if usable_item == "두쫀쿠":
                    hp = hp + 25
                    print("HP가 25 증가했습니다! (현재 HP: " + str(hp) + ")")
                elif usable_item == "카페라떼":
                    hp = hp + 25
                    print("HP가 25 증가했습니다! (현재 HP: " + str(hp) + ")")
            else:
                print("가방에 없는 물건이거나 잘못된 입력입니다.")
    return None

def 저장_작업():
    with open("save_file.txt", "w", encoding="utf-8") as f:
        f.write("● 주인공의\n")
        f.write("  ○ 상태\n")
        f.write("    - HP: " + str(hp) + "\n")
        f.write("    - 계좌 잔액: " + str(account_balance) + "원\n")
        
        if len(inventory) > 0:
            가방_문자열 = ""
            for i in range(len(inventory)):
                if i == 0:
                    가방_문자열 = 가방_문자열 + inventory[i]
                else:
                    가방_문자열 = 가방_문자열 + ", " + inventory[i]
            f.write("    - 가방: " + 가방_문자열 + "\n")
        else:
            f.write("    - 가방: 비어있음\n")
            
        f.write("  ○ 위치: " + map_data[row][col] + "\n")
        
        if len(quests) > 0:
            임무_문자열 = ""
            for i in range(len(quests)):
                if i == 0:
                    임무_문자열 = 임무_문자열 + quests[i]
                else:
                    임무_문자열 = 임무_문자열 + ", " + quests[i]
            f.write("  ○ 임무: " + 임무_문자열 + "\n")
        else:
            f.write("  ○ 임무: 비어있음\n")
            
        f.write("● 현재 시각: " + current_time + "\n")
        f.write("● 난이도: " + settings_difficulty + "\n")
        
        입력_문자열 = ""
        for i in range(len(all_inputs)):
            if i == 0:
                입력_문자열 = 입력_문자열 + all_inputs[i]
            else:
                입력_문자열 = 입력_문자열 + ", " + all_inputs[i]
                
        f.write("● 현재까지의 모든 입력: [" + 입력_문자열 + "]\n")
        
    print("게임이 저장되었습니다.")
    return None

def 불러오기_작업():
    global hp, account_balance, inventory, quests, row, col, current_time, settings_difficulty
    
    files = []
    for f in os.listdir('.'):
        if os.path.isfile(f):
            files.append(f)
            
    print("현재 폴더의 파일 목록:")
    idx = 0
    for filename in files:
        print(str(idx + 1) + ". " + filename)
        idx = idx + 1
    
    load_inp = 입력_받기_프롬프트("불러올 파일의 번호를 선택하거나, 경로를 직접 입력하세요: ")
    
    target_file = ""
    if load_inp.isdigit() == True:
        번호 = int(load_inp)
        if 번호 >= 1 and 번호 <= len(files):
            target_file = files[번호 - 1]
    else:
        target_file = load_inp
        
    if os.path.exists(target_file) == True and os.path.isfile(target_file) == True:
        with open(target_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if "- HP:" in line:
                숫자만 = line.replace("- HP:", "").strip()
                hp = int(숫자만)
            elif "- 계좌 잔액:" in line:
                숫자만 = line.replace("- 계좌 잔액:", "").replace("원", "").strip()
                account_balance = int(숫자만)
            elif "- 가방:" in line:
                items_str = line.replace("- 가방:", "").strip()
                if items_str == "비어있음":
                    inventory = []
                else:
                    inventory = []
                    글자들 = items_str.split(",")
                    for 글자 in 글자들:
                        inventory.append(글자.strip())
            elif "○ 임무:" in line:
                quests_str = line.replace("○ 임무:", "").strip()
                if quests_str == "비어있음":
                    quests = []
                else:
                    quests = []
                    글자들 = quests_str.split(",")
                    for 글자 in 글자들:
                        quests.append(글자.strip())
            elif "○ 위치:" in line:
                loc = line.replace("○ 위치:", "").strip()
                for r in range(len(map_data)):
                    for c in range(len(map_data[r])):
                        if map_data[r][c] == loc:
                            row = r
                            col = c
            elif "● 현재 시각:" in line:
                current_time = line.replace("● 현재 시각:", "").strip()
            elif "● 난이도:" in line:
                settings_difficulty = line.replace("● 난이도:", "").strip()
                
        print("'" + target_file + "' 파일에서 데이터를 성공적으로 불러왔습니다.")
    else:
        print("파일을 찾을 수 없습니다.")
    return None

def 종료_작업():
    global 종료신호가_없음
    종료신호가_없음 = False
    print("게임을 종료합니다.")
    return None

def 무효_입력_작업():
    print("잘못된 명령어입니다.")
    return None

def 입력에_따른_작업을_설정하기(사용자의_입력):
    작업매핑 = {
        "상태": 상태_출력_작업,
        "임무": 임무_출력_작업,
        "동": 이동_동_작업,
        "서": 이동_서_작업,
        "남": 이동_남_작업,
        "북": 이동_북_작업,
        "상호작용": 상호작용_작업,
        "가방": 가방_작업,
        "저장": 저장_작업,
        "불러오기": 불러오기_작업,
        "종료": 종료_작업
    }
    
    작업 = 무효_입력_작업
    if 사용자의_입력 in 작업매핑:
        작업 = 작업매핑[사용자의_입력]
        
    return 작업

def 입력_받기():
    user_input = input("\n명령을 입력하세요 (상태, 임무, 동, 서, 남, 북, 상호작용, 가방, 저장, 불러오기, 종료): ")
    all_inputs.append(user_input)
    return user_input

def 결과를_상태에_반영하기(결과):
    pass

초기_설정()

while 종료신호가_없음 == True:
    사용자의_입력 = 입력_받기()
    작업 = 입력에_따른_작업을_설정하기(사용자의_입력)
    결과 = 작업()
    결과를_상태에_반영하기(결과)