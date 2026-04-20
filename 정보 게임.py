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
account_balance = 10000
inventory = []
quests = []
주인공_상태 = "배고픔"
settings_difficulty = "보통"
settings_gate_visited = False

종료신호가_없음 = True

dynamic_events = {}
bujo_answers = []
food_answers = []
places_dict = {}

class Quest:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
    
    def __str__(self):
        return self.name

class Place:
    def __init__(self, name):
        self.name = name
        self.event_info = ""
        self.can_buy = False
        self.buy_prices = {}
        self.can_sell = False
        self.sell_prices = {}
        self.quest_interaction = None

    def 사건관련정보_가져오기(self):
        return self.event_info

    def 판매(self):
        global account_balance, inventory
        if not self.can_sell:
            print("여기서는 물건을 판매할 수 없습니다.")
            return

        if len(inventory) == 0:
            print("판매할 물건이 없습니다.")
            return
            
        print("어떤 물건을 판매하시겠습니까?")
        idx = 0
        for item in inventory:
            print(str(idx + 1) + ". " + item)
            idx = idx + 1
            
        choice = 입력_받기_프롬프트("판매할 물건의 이름 또는 번호를 입력하세요 (취소: 엔터): ")
        if choice != "":
            sell_item = ""
            if choice.isdigit() == True:
                번호 = int(choice)
                if 번호 >= 1 and 번호 <= len(inventory):
                    sell_item = inventory[번호 - 1]
            else:
                for item in inventory:
                    if choice == item:
                        sell_item = choice
                        
            if sell_item != "":
                if sell_item in self.sell_prices:
                    price = self.sell_prices[sell_item]
                else:
                    price = 1000 # default
                    
                account_balance = account_balance + price
                inventory.remove(sell_item)
                print("'" + sell_item + "'을(를) " + str(price) + "원에 판매했습니다. (현재 잔액: " + str(account_balance) + "원)")
            else:
                print("가방에 없는 물건이거나 잘못된 입력입니다.")

    def 구매(self):
        global account_balance, inventory
        if not self.can_buy:
            print("여기서는 물건을 구매할 수 없습니다.")
            return

        print(self.name + "에서는 물건을 구매할 수 있습니다.")
        while True:
            opts = []
            buy_list = list(self.buy_prices.keys())
            for i, item in enumerate(buy_list):
                opts.append(f"{i+1}. {item}({self.buy_prices[item]}원)")
            opts.append(f"{len(buy_list)+1}. 나가기")
            
            buy_choice = 입력_받기_프롬프트(f"무엇을 구매하시겠습니까? ({', '.join(opts)}): ")
            
            chosen_item = None
            if buy_choice.isdigit():
                idx = int(buy_choice)
                if 1 <= idx <= len(buy_list):
                    chosen_item = buy_list[idx - 1]
                elif idx == len(buy_list) + 1:
                    break
            else:
                if buy_choice in buy_list:
                    chosen_item = buy_choice
                elif buy_choice == "나가기":
                    break
            
            if chosen_item:
                price = self.buy_prices[chosen_item]
                if account_balance >= price:
                    account_balance = account_balance - price
                    inventory.append(chosen_item)
                    print(f"{chosen_item}를 구매하여 가방에 넣었습니다.")
                else:
                    print("잔액이 부족합니다.")
            else:
                print("잘못된 입력입니다.")

    def 임무(self):
        global quests, settings_gate_visited
        q_names = [q.name for q in quests]
        
        if self.quest_interaction == "정문":
            if "학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자." not in q_names and settings_gate_visited == False:
                quests.append(Quest("학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자.", "독수리상에 가보자."))
                settings_gate_visited = True
                print("학교에 들어가기 위해 정문에서 상호작용을 한다.")
                print("학교에서 어떤 일이 벌어지고 있을까?")
                print("\n[임무 알림] 새로운 임무: 학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자.")
            else:
                print("이미 정문에서 임무를 확인했습니다.")

        elif self.quest_interaction == "독수리상":
            if "학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자." in q_names:
                quests = [q for q in quests if q.name != "학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자."]
                q_names = [q.name for q in quests]
                print("정문에서 받은 임무를 해결했습니다.")

            print("독수리상에서는 임무를 받을 수 있습니다.")
            while True:
                quest_choice = 입력_받기_프롬프트("어떤 임무를 받으시겠습니까? (1. 교내 부조리 수사, 2. 교내 위생사건 수사, 3. 나가기): ")
                if quest_choice == "1" or quest_choice == "교내 부조리 수사":
                    if "교내 부조리 수사" not in q_names:
                        quests.append(Quest("교내 부조리 수사", "교내 어딘가에서 부조리가 일어나고 있다."))
                        q_names.append("교내 부조리 수사")
                        print("임무 '교내 부조리 수사'를 받았습니다.")
                        print("  ● 교내 어딘가에서 부조리가 일어나고 있다.")
                        print("  ● 이동하고 상호작용을 해서 부조리를 찾아서 본관에 보고하라.")
                    else:
                        print("이미 받은 임무입니다.")
                elif quest_choice == "2" or quest_choice == "교내 위생사건 수사":
                    if "교내 위생사건 수사" not in q_names:
                        quests.append(Quest("교내 위생사건 수사", "학생들이 단체로 식중독에 걸렸다."))
                        q_names.append("교내 위생사건 수사")
                        print("임무 '교내 위생사건 수사'를 받았습니다.")
                        print("  ● 학생들이 단체로 식중독에 걸렸다.")
                        print("  ● 이동하고 상호작용을 해서 위생사건의 원인을 찾아서 세브란스에 보고하라.")
                    else:
                        print("이미 받은 임무입니다.")
                elif quest_choice == "3" or quest_choice == "나가기":
                    break
                else:
                    print("잘못된 입력입니다.")

        elif self.quest_interaction == "본관":
            if "교내 부조리 수사" in q_names or "교내 부조리 수사 완료" in q_names:
                ans = 입력_받기_프롬프트("교내 어디에 부조리가 있나? ")
                if ans in bujo_answers:
                    quests = [q for q in quests if q.name != "교내 부조리 수사" and q.name != "교내 부조리 수사 완료"]
                    if "교내 부조리 수사 최종 완료" not in [q.name for q in quests]:
                        quests.append(Quest("교내 부조리 수사 최종 완료"))
                    print("해결후: 수업들으러 이윤재관 가야지!")
                else:
                    print("틀렸습니다.")
            else:
                print("진행 중인 관련 임무가 없습니다.")

        elif self.quest_interaction == "세브란스병원":
            if "교내 위생사건 수사" in q_names or "교내 위생사건 수사 완료" in q_names:
                ans = 입력_받기_프롬프트("교내 어디에 식중독 원인이 있나? ")
                if ans in food_answers:
                    quests = [q for q in quests if q.name != "교내 위생사건 수사" and q.name != "교내 위생사건 수사 완료"]
                    if "교내 위생사건 수사 최종 완료" not in [q.name for q in quests]:
                        quests.append(Quest("교내 위생사건 수사 최종 완료"))
                    print("해결후: 수업들으러 이윤재관 가야지!")
                else:
                    print("틀렸습니다.")
            else:
                print("진행 중인 관련 임무가 없습니다.")

        elif self.quest_interaction == "공터1":
            if "교내 부조리 수사" in q_names:
                print("이곳에서 누군가 부당한 거래를 하는 현장을 목격했습니다!")
                print("'교내 부조리 증거'를 발견했습니다. 본관으로 이동하여 보고하세요.")
                quests = [q for q in quests if q.name != "교내 부조리 수사"]
                quests.append(Quest("교내 부조리 수사 완료"))
            else:
                print("상호작용할 수 없는 장소입니다.")

        elif self.quest_interaction == "공터2":
            if "교내 위생사건 수사" in q_names:
                print("버려진 상한 음식물 쓰레기통을 발견했습니다!")
                print("'위생사건 원인'을 찾아냈습니다. 세브란스병원으로 이동하여 보고하세요.")
                quests = [q for q in quests if q.name != "교내 위생사건 수사"]
                quests.append(Quest("교내 위생사건 수사 완료"))
            else:
                print("상호작용할 수 없는 장소입니다.")

        elif self.quest_interaction == "이윤재관":
            부조리_최종_완료 = "교내 부조리 수사 최종 완료" in q_names
            위생_최종_완료 = "교내 위생사건 수사 최종 완료" in q_names
            if 부조리_최종_완료 and 위생_최종_완료:
                print("부조리와 식중독 수사를 완료했구나! 수업은 이걸로 끝입니다. 또 만나요~")
                종료_작업()
            elif 부조리_최종_완료 and not 위생_최종_완료:
                print("부조리 수사를 완료했구나! 식중독 원인도 찾아주세요~")
            elif not 부조리_최종_완료 and 위생_최종_완료:
                print("식중독 수사를 완료했구나! 부조리도 찾아주세요~")
            else:
                print("수업을 들을 수 있는 이윤재관입니다. (아직 임무를 해결하지 않았습니다.)")
        else:
            print("상호작용할 수 없는 장소입니다.")


def load_events():
    global dynamic_events, bujo_answers, food_answers
    file_path = "events.txt"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",", 2)
                if len(parts) == 3:
                    e_type, place, desc = parts
                    e_type = e_type.strip()
                    place = place.strip()
                    desc = desc.strip()
                    dynamic_events[place] = desc
                    if e_type == "부조리":
                        bujo_answers.append(place)
                    elif e_type == "식중독":
                        food_answers.append(place)

def init_places():
    global places_dict
    판매위치_1 = ["체육관", "공학관", "공학원", "재활병원", "어린이병원", "종합관", "노천극장"]
    판매위치_2 = ["중앙도서관", "백양관", "대강당", "백주년기념관", "안과병원", "암병원", "새천년관", "알렌관", "제중관", "의과대학", "치과대학", "세브란스", "세브란스병원", "본관", "경영관"]
    임무장소 = ["정문", "독수리상", "이윤재관", "공터1", "공터2", "본관", "세브란스병원"]

    for r in range(len(map_data)):
        for c in range(len(map_data[0])):
            p_name = map_data[r][c]
            if p_name != "" and p_name not in places_dict:
                p = Place(p_name)
                
                if p_name in dynamic_events:
                    p.event_info = dynamic_events[p_name]

                if p_name == "학생회관":
                    p.can_sell = True
                    p.sell_prices = {"두쫀쿠": 2500, "카페라떼": 1250}
                    p.can_buy = True
                    p.buy_prices = {"두쫀쿠": 5000, "카페라떼": 3000}
                elif p_name in ["스타벅스", "ABMRC"]:
                    p.can_buy = True
                    p.buy_prices = {"두쫀쿠": 4000, "카페라떼": 2000}
                
                if p_name in 판매위치_1:
                    p.can_sell = True
                    p.sell_prices = {"두쫀쿠": 7000, "카페라떼": 4000}
                elif p_name in 판매위치_2:
                    p.can_sell = True
                    p.sell_prices = {"두쫀쿠": 6000, "카페라떼": 3000}

                if p_name in 임무장소:
                    p.quest_interaction = p_name

                places_dict[p_name] = p

def 초기_설정():
    global settings_difficulty
    load_events()
    init_places()
    
    print("송도 생활을 마치고 신촌에 처음 도착했다. 연대앞 버스정류장이다.")
    print("배가 고프다. == 처음의 배고픈 상태는 HP=10이다.")
    while True:
        diff = 입력_받기_프롬프트("난이도를 선택하세요 (쉬움, 보통, 어려움): ")
        if diff in ["쉬움", "보통", "어려움"]:
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
    if col + 1 < len(map_data[0]) and map_data[row][col+1] != "":
        print("  - 동: " + map_data[row][col+1])
    if col - 1 >= 0 and map_data[row][col-1] != "":
        print("  - 서: " + map_data[row][col-1])
    if row + 1 < len(map_data) and map_data[row+1][col] != "":
        print("  - 남: " + map_data[row+1][col])
    if row - 1 >= 0 and map_data[row-1][col] != "":
        print("  - 북: " + map_data[row-1][col])
    return None

def 임무목록_출력_작업():
    print("● 가지고 있는 임무 목록:")
    if len(quests) == 0:
        print("  없음")
    else:
        for q in quests:
            print("  - " + q.name)
    return None

def 이동_동_작업(): return 이동_작업("동")
def 이동_서_작업(): return 이동_작업("서")
def 이동_남_작업(): return 이동_작업("남")
def 이동_북_작업(): return 이동_작업("북")

def 이동_작업(방향):
    global row, col, hp, settings_gate_visited, settings_difficulty
    new_row = row
    new_col = col
    
    if 방향 == "북": new_row -= 1
    elif 방향 == "남": new_row += 1
    elif 방향 == "동": new_col += 1
    elif 방향 == "서": new_col -= 1
        
    갈수있음 = False
    if 0 <= new_row < len(map_data) and 0 <= new_col < len(map_data[0]):
        if map_data[new_row][new_col] != "":
            갈수있음 = True
                
    if 갈수있음:
        row = new_row
        col = new_col
        
        감소치 = 1
        if settings_difficulty == "쉬움": 감소치 = 0.5
        elif settings_difficulty == "보통": 감소치 = 1
        elif settings_difficulty == "어려움": 감소치 = 2
            
        hp -= 감소치
        curr_place = map_data[row][col]
        print("[" + curr_place + "](으)로 이동했습니다.")
        print("(HP " + str(감소치) + " 감소, 현재 HP: " + str(hp) + ")")
        
        if curr_place in places_dict:
            place_obj = places_dict[curr_place]
            사건관련정보 = place_obj.사건관련정보_가져오기()
            if 사건관련정보:
                print("[사건 정보] " + 사건관련정보)
                
            가능한_상호작용_목록 = []
            if place_obj.can_buy: 가능한_상호작용_목록.append("구매")
            if place_obj.can_sell: 가능한_상호작용_목록.append("판매")
            if place_obj.quest_interaction: 가능한_상호작용_목록.append("임무")
                
            if len(가능한_상호작용_목록) > 0:
                print("● 이곳에서 가능한 상호작용: " + ", ".join(가능한_상호작용_목록))
            else:
                print("● 이곳에서 가능한 상호작용: 없음")
    else:
        print("그 방향은 막혔어.")
    return None

def 판매_작업():
    curr_place = map_data[row][col]
    if curr_place in places_dict:
        places_dict[curr_place].판매()
    else:
        print("여기서는 물건을 판매할 수 없습니다.")
    return None

def 구매_작업():
    curr_place = map_data[row][col]
    if curr_place in places_dict:
        places_dict[curr_place].구매()
    else:
        print("여기서는 물건을 구매할 수 없습니다.")
    return None

def 임무_작업():
    curr_place = map_data[row][col]
    if curr_place in places_dict:
        places_dict[curr_place].임무()
    else:
        print("상호작용할 수 없는 장소입니다.")
    return None

def 난이도_설정_작업():
    global settings_difficulty
    print("현재 난이도: " + settings_difficulty)
    change = 입력_받기_프롬프트("난이도를 변경하시겠습니까? (쉬움, 보통, 어려움 / 취소: 엔터): ")
    if change in ["쉬움", "보통", "어려움"]:
        settings_difficulty = change
        print("난이도가 '" + settings_difficulty + "'(으)로 변경되었습니다.")
    elif change != "":
        print("잘못된 입력입니다.")
    return None

def 가방_작업():
    global hp, inventory
    if len(inventory) == 0:
        print("가방이 비어있습니다.")
    else:
        print("가방에 들어있는 물건들:")
        for idx, item in enumerate(inventory):
            print(f"{idx + 1}. {item}")
            
        choice = 입력_받기_프롬프트("사용할 물건의 이름 또는 번호를 입력하세요 (취소: 엔터): ")
        if choice != "":
            usable_item = ""
            if choice.isdigit() and 1 <= int(choice) <= len(inventory):
                usable_item = inventory[int(choice) - 1]
            elif choice in inventory:
                usable_item = choice
            
            if usable_item != "":
                print("'" + usable_item + "'을(를) 사용했습니다.")
                inventory.remove(usable_item)
                if usable_item == "두쫀쿠":
                    hp += 10
                    print("HP가 10 증가했습니다! (현재 HP: " + str(hp) + ")")
                elif usable_item == "카페라떼":
                    hp += 5
                    print("HP가 5 증가했습니다! (현재 HP: " + str(hp) + ")")
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
            f.write("    - 가방: " + ", ".join(inventory) + "\n")
        else:
            f.write("    - 가방: 비어있음\n")
            
        f.write("  ○ 위치: " + map_data[row][col] + "\n")
        
        if len(quests) > 0:
            q_strings = [str(q) for q in quests]
            f.write("  ○ 임무: " + ", ".join(q_strings) + "\n")
        else:
            f.write("  ○ 임무: 비어있음\n")
            
        f.write("● 난이도: " + settings_difficulty + "\n")
        f.write("● 현재까지의 모든 입력: [" + ", ".join(all_inputs) + "]\n")
        
    print("게임이 저장되었습니다.")
    return None

def 불러오기_작업():
    global hp, account_balance, inventory, quests, row, col, settings_difficulty
    
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    print("현재 폴더의 파일 목록:")
    for idx, filename in enumerate(files):
        print(f"{idx + 1}. {filename}")
    
    load_inp = 입력_받기_프롬프트("불러올 파일의 번호를 선택하거나, 경로를 직접 입력하세요: ")
    target_file = ""
    if load_inp.isdigit() and 1 <= int(load_inp) <= len(files):
        target_file = files[int(load_inp) - 1]
    else:
        target_file = load_inp
        
    if os.path.exists(target_file) and os.path.isfile(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        for line in lines:
            line = line.strip()
            if "- HP:" in line:
                hp = float(line.replace("- HP:", "").strip())
            elif "- 계좌 잔액:" in line:
                account_balance = int(line.replace("- 계좌 잔액:", "").replace("원", "").strip())
            elif "- 가방:" in line:
                items_str = line.replace("- 가방:", "").strip()
                inventory = [] if items_str == "비어있음" else [item.strip() for item in items_str.split(",")]
            elif "○ 임무:" in line:
                quests_str = line.replace("○ 임무:", "").strip()
                quests = []
                if quests_str != "비어있음":
                    for name in quests_str.split(","):
                        quests.append(Quest(name.strip()))
            elif "○ 위치:" in line:
                loc = line.replace("○ 위치:", "").strip()
                for r in range(len(map_data)):
                    for c in range(len(map_data[r])):
                        if map_data[r][c] == loc:
                            row, col = r, c
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

def 지도_출력_작업():
    print("\n[현재 지도]")
    for r in range(len(map_data)):
        line_str = []
        for c in range(len(map_data[r])):
            if row == r and col == c:
                line_str.append("[ ★ ]")
            elif map_data[r][c] == "":
                line_str.append("     ")
            else:
                line_str.append("[ O ]")
        print(" ".join(line_str))
    print("★: 현재 위치, O: 이동 가능\n")
    return None

def 무효_입력_작업():
    print("잘못된 명령어입니다.")
    return None

def 입력에_따른_작업을_설정하기(사용자의_입력):
    작업매핑 = {
        "상태": 상태_출력_작업,
        "지도": 지도_출력_작업,
        "동": 이동_동_작업,
        "서": 이동_서_작업,
        "남": 이동_남_작업,
        "북": 이동_북_작업,
        "구매": 구매_작업,
        "판매": 판매_작업,
        "임무": 임무_작업,
        "임무목록": 임무목록_출력_작업,
        "가방": 가방_작업,
        "저장": 저장_작업,
        "불러오기": 불러오기_작업,
        "난이도": 난이도_설정_작업,
        "종료": 종료_작업
    }
    return 작업매핑.get(사용자의_입력, 무효_입력_작업)

def 입력_받기():
    user_input = input("\n명령을 입력하세요 (상태, 지도, 동, 서, 남, 북, 구매, 판매, 임무, 임무목록, 가방, 저장, 불러오기, 난이도, 종료): ")
    all_inputs.append(user_input)
    return user_input

def 결과를_상태에_반영하기(결과):
    pass

초기_설정()

while 종료신호가_없음:
    사용자의_입력 = 입력_받기()
    작업 = 입력에_따른_작업을_설정하기(사용자의_입력)
    결과 = 작업()
    결과를_상태에_반영하기(결과)