import pygame
import sys
import random
import math


# ******************** 画像の読み込み ********************
img_piece = [
    pygame.image.load("image/mujirusi.png"),
    pygame.image.load("image/batsu.png"),
    pygame.image.load("image/maru.png")
]


# ******************** 変数／定数 ********************
# =============== COLOR ===============
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# =============== SIZE ===============
SCREEN_SIZE = 1000
KUHAKU = 250
IMAGE_SIZE = 100
# =============== MARK ===============
MUJIRUSI = 0
BATSU = 1
MARU = 2
mark = [BATSU, MARU]
# =============== GAME ===============
idx = 0
tmr = 0
loop = 100
win = 0
tunr = 0
player = 0
computer = 0
# =============== SELECT ===============
select_piece = False
choice_x = 0
choice_y = 0
put_x = 0
put_y = 0
# =============== BOARD ===============
board = []
back = []
for y in range(5):
    board.append([0]*5)
    back.append([0]*5)
blink = [False]*25

back_choice_x = 0
back_choice_y = 0
back_put_x = 0
back_put_y = 0



# ============================================================
#                           DRAW
# ============================================================

# ******************** 文字の描画 ********************
def draw_text(sc, txt, x, y, siz, col):
    fnt = pygame.font.Font(None, siz)
    sur = fnt.render(txt, True, col)
    
    x = x - sur.get_width()/2
    y = y - sur.get_height()/2

    sc.blit(sur, [x, y])


# ******************** ボードの描画 ********************
def draw_board(sc):
    # 図：円形の黒いボード
    pygame.draw.circle(sc, BLACK, [SCREEN_SIZE/2, SCREEN_SIZE/2], SCREEN_SIZE/2 - 100)
    
    for y in range(5):
        for x in range(5):
            # 画像中央の座標
            X = KUHAKU + x * IMAGE_SIZE
            Y = KUHAKU + y * IMAGE_SIZE
            
            if board[y][x] == MUJIRUSI: # 無印
                if blink[y*5 + x] == True:
                    blink[y*5 + x] = False
                else:
                    sc.blit(img_piece[MUJIRUSI], [X, Y])
            if board[y][x] == BATSU:    # バツ
                if blink[y*5 + x] == True:
                    blink[y*5 + x] = False
                else:
                    sc.blit(img_piece[BATSU], [X, Y])
            if board[y][x] == MARU:     # マル
                if blink[y*5 + x] == True:
                    blink[y*5 + x] = False
                else:
                    sc.blit(img_piece[MARU], [X, Y])


# ******************** タイトル画面の描画 ********************
def draw_title(sc, mx, my, mb):
    global idx, tmr, player, computer
    
    # 図：円形の黒いボード
    pygame.draw.circle(sc, BLACK, [SCREEN_SIZE/2, SCREEN_SIZE/2], SCREEN_SIZE/2 - 100)

    # 先攻／後攻の選択            
    # 画像：「X」の駒(先攻)
    img_batsu = pygame.transform.rotozoom(img_piece[BATSU], 0, 1.5)
    draw_text(sc, "FIRST ATTACK", SCREEN_SIZE/2 - 170, SCREEN_SIZE/2 + 120, 40, WHITE)
    if ((SCREEN_SIZE/2 - 170) - img_batsu.get_width()/2 <= mx  <= (SCREEN_SIZE/2 - 170) + img_batsu.get_width()/2) and \
        (SCREEN_SIZE/2 - img_batsu.get_height()/2 <= my <= SCREEN_SIZE/2 + img_batsu.get_height()/2):
        if tmr%30 < 20:
            sc.blit(img_batsu, [(SCREEN_SIZE/2 - 170) - img_batsu.get_width()/2, SCREEN_SIZE/2 - img_batsu.get_height()/2])
        if mb == True: #「X」を選択
            player = 0
            computer = 1
            idx = 1
            tmr = 0
    else:
        sc.blit(img_batsu, [(SCREEN_SIZE/2 - 170) - img_batsu.get_width()/2, SCREEN_SIZE/2 - img_batsu.get_height()/2])

    # 画像：「○」の駒(後攻)
    img_maru = pygame.transform.rotozoom(img_piece[MARU], 0, 1.5)
    draw_text(sc, "SECOND ATTACK", SCREEN_SIZE/2 + 170, SCREEN_SIZE/2 + 120, 40, WHITE)
    if ((SCREEN_SIZE/2 + 170) - img_maru.get_width()/2 <= mx <= (SCREEN_SIZE/2 + 170) + img_maru.get_width()/2) and \
        (SCREEN_SIZE/2 - img_maru.get_height()/2 <= my <= SCREEN_SIZE/2 + img_maru.get_height()/2):
        if tmr%30 < 20:
            sc.blit(img_maru, [(SCREEN_SIZE/2 + 170) - img_maru.get_width()/2, SCREEN_SIZE/2 - img_maru.get_height()/2])
        if mb == True: #「○」の選択
            player = 1
            computer = 0
            idx = 1
            tmr = 0
    else:
        sc.blit(img_maru, [(SCREEN_SIZE/2 + 170) - img_maru.get_width()/2, SCREEN_SIZE/2 - img_maru.get_height()/2])


# ============================================================
#                           SELECT
# ============================================================

# ******************** マウスで選択している駒を点滅させる設定 ********************
def choice_piece(x, y, b, op):
    global tmr
    global select_piece, choice_x, choice_y

    # 端の駒以外は選択できない
    if 1 <= x <= 3 and 1 <= y <= 3:
        return

    # 無印の駒
    if board[y][x] == MUJIRUSI:
        if b == True:    # クリック時の処理
            select_piece = True
            choice_x = x
            choice_y = y
        if tmr%30 < 20: # 点滅の処理
            blink[y*5 + x] = True
            
    # オペレーター(プレイヤー／コンピュータ)の駒が「X」
    if mark[op] == BATSU and board[y][x] == BATSU:
        if b == True:    # クリック時の処理
            select_piece = True
            choice_x = x
            choice_y = y
        if tmr%30 < 20: # 点滅の処理
            blink[y*5 + x] = True
            
    # オペレーター(プレイヤー／コンピュータ)の駒が「○」
    if mark[op] == MARU and board[y][x] == MARU:
        if b == True:    # クリック時の処理
            select_piece = True
            choice_x = x
            choice_y = y
        if tmr%30 < 20: # 点滅の処理
            blink[y*5 + x] = True


# ******************** 駒を置く位置を選択 ********************
def put_piece(x, y, b, op):
    global tmr
    global select_piece, put_x, put_y

    if tmr%90 < 10:
        blink[choice_y*5 + choice_x] = True

    # 選んだ駒が四隅だった場合
    if (choice_x == 0 and choice_y == 0) or (choice_x == 4 and choice_y == 4):
        if b == True:     # クリック時の処理
            if (x == 0 and y == 4) or (x == 4 and y == 0): # 置ける駒の位置
                select_piece = True
                put_x = x
                put_y = y
        if tmr%90 < 10: # 点滅の処理
            blink[4*5 + 0] = True
            blink[0*5 + 4] = True
            
    elif (choice_x == 0 and choice_y == 4) or (choice_x == 4 and choice_y == 0):
        if b == True:     # クリック時の処理
            if (x == 0 and y == 0) or (x == 4 and y == 4): # 置ける駒の位置
                select_piece = True
                put_x = x
                put_y = y
        if tmr%90 < 10: # 点滅の処理
            blink[0*5 + 0] = True
            blink[4*5 + 4] = True
            
    # 選んだ駒が左右の端だった場合
    elif choice_x == 0 or choice_x == 4:
        if b == True:     # クリック時の処理
            if choice_x == 0 and ( (x == 0 and y == 0) or (x == 0 and y == 4) or (x == 4 and y == choice_y) ) or \
               choice_x == 4 and ( (x == 4 and y == 0) or (x == 4 and y == 4) or (x == 0 and y == choice_y) ): # 置ける駒の位置
                select_piece = True
                put_x = x
                put_y = y
        if tmr%90 < 10: # 点滅の処理
            blink[0*5 + choice_x] = True
            blink[4*5 + choice_x] = True
            blink[choice_y*5 + 4] = True
            blink[choice_y*5 + 0] = True
            
    # 選んだコマが上下の端だった場合
    elif choice_y == 0 or choice_y == 4:
        if b == True:     # クリック時の処理
            if choice_y == 0 and ( (x == 0 and y == 0) or (x == 4 and y == 0) or (x == choice_x and y == 4) ) or \
               choice_y == 4 and ( (x == 0 and y == 4) or (x == 4 and y == 4) or (x == choice_x and y == 0) ): # 置ける駒の位置
                select_piece = True
                put_x = x
                put_y = y
        if tmr%90 < 10: # 点滅の処理
            blink[choice_y*5 + 0] = True
            blink[choice_y*5 + 4] = True
            blink[4*5 + choice_x] = True
            blink[0*5 + choice_x] = True


# ============================================================
#                           PIECE
# ============================================================

# ******************** 駒のスライド ********************
def slide_piece():
    global choice_x, choice_y, put_x, put_y

    # 選んだ駒
    choice_koma = board[choice_y][choice_x]

    # 選んだ駒の位置と置く駒の位置 -> 左右端のどちらか
    if choice_x == put_x:
        # 選んだ駒と置く駒の位置関係で分類 -> スライド
        if choice_y < put_y:
            for i in range(choice_y, put_y):
                board[i][choice_x] = board[i+1][choice_x]
        elif put_y < choice_y:
            for i in range(choice_y, put_y, -1):
                board[i][choice_x] = board[i-1][choice_x]
        # 選んだ駒の置く位置を一度、無印にする
        board[put_y][put_x] = MUJIRUSI
        # 揃った列がないか調べる -> 揃った場合、勝敗が決まる
        judge()
        if win > 0:
            idx = 4
            tmr = 0
            return
        # 選んだ駒を置く位置へ
        board[put_y][put_x] = choice_koma
            
    # 選んだ駒の位置と置く駒の位置 -> 上下端のどちらか
    elif choice_y == put_y:
        # 選んだ駒と置く駒の位置関係で分類 -> スライド
        if choice_x < put_x:
            for i in range(choice_x, put_x):
                board[choice_y][i] = board[choice_y][i+1]
        elif put_x < choice_x:
            for i in range(choice_x, put_x, -1):
                board[choice_y][i] = board[choice_y][i-1]
        # 選んだ駒の置く位置を一度、無印にする
        board[put_y][put_x] = MUJIRUSI
        # 揃った列がないか調べる -> 揃った場合、勝敗が決まる
        judge()
        if win > 0:
            idx = 4
            tmr = 0
            return
        # 選んだ駒を置く位置
        board[put_y][put_x] = choice_koma


# ============================================================
#                           COMPUTER
# ============================================================

# ******************** ボードの状態を保存 ********************
def save():
    for y in range(5):
        for x in range(5):
            back[y][x] = board[y][x]


# ******************** ボードの状態をロード ********************
def load():
    for y in range(5):
        for x in range(5):
            board[y][x] = back[y][x]


# ******************** 駒を選ぶシミュレーション ********************
def choice_simulation(op):
    global select_piece
    
    while True:
        sx = random.randint(0, 4)
        sy = random.randint(0, 4)
        choice_piece(sx, sy, True, op)

        if select_piece == True:
            select_piece = False
            board[choice_x][choice_y] = mark[turn]
            break


# ******************** 駒を置くシミュレーション ********************
def put_simulation(op):
    global select_piece
    
    while True:
        # 駒を置ける位置を取得
        put_pos = put_position_random()
        put_piece(put_pos[0], put_pos[1], True, op)

        if select_piece == True:
            select_piece = False
            break


# ******************** 駒を置ける位置 ********************
def put_position():
    # 選んだ駒が四隅だった場合
    if (choice_x == 0 and choice_y == 0) or (choice_x == 4 and choice_y == 4):
        return [0, 4, 4, 0]

    elif (choice_x == 0 and choice_y == 4) or (choice_x == 4 and choice_y == 0):
        return [0, 0, 4, 4]

    # 選んだ駒が左の端だった場合
    elif choice_x == 0:
        return [0, 0, 0, 4, 4, choice_y]
    
    # 選んだ駒が右の端だった場合
    elif choice_x == 4:
        return [4, 0, 4, 4, 0, choice_y]

    # 選んだ駒が上の端だった場合
    elif choice_y == 0:
        return [0, 0, 4, 0, choice_x, 4]

    # 選んだ駒が下の端だった場合
    elif choice_y == 4:
        return [0, 4, 4, 4, choice_x, 0]


# ******************** 駒を置ける位置(ランダムに選択) ********************
def put_position_random():
    # 2択 or 3択
    rand_num2 = random.randint(0, 1)
    rand_num3 = random.randint(0, 2)
    
    # 選んだ駒が四隅だった場合
    if (choice_x == 0 and choice_y == 0) or (choice_x == 4 and choice_y == 4):
        if rand_num2 == 0:
            return 0, 4
        elif rand_num2 == 1:
            return 4, 0

    elif (choice_x == 0 and choice_y == 4) or (choice_x == 4 and choice_y == 0):
        if rand_num2 == 0:
            return 0, 0
        elif rand_num2 == 1:
            return 4, 4

    # 選んだ駒が左の端だった場合
    elif choice_x == 0:
        if rand_num3 == 0:
            return 0, 0
        elif rand_num3 == 1:
            return 0, 4
        elif rand_num3 == 2:
            return 4, choice_y

    # 選んだ駒が右の端だった場合
    elif choice_x == 4:
        if rand_num3 == 0:
            return 4, 0
        elif rand_num3 == 1:
            return 4, 4
        elif rand_num3 == 2:
            return 0, choice_y

    # 選んだ駒が上の端だった場合
    elif choice_y == 0:
        if rand_num3 == 0:
            return 0, 0
        elif rand_num3 == 1:
            return 4, 0
        elif rand_num3 == 2:
            return choice_x, 4

    # 選んだ駒が下の端だった場合
    elif choice_y == 4:
        if rand_num3 == 0:
            return 0, 4
        elif rand_num3 == 1:
            return 4, 4
        elif rand_num3 == 2:
            return choice_x, 0

    return 0, 0

def choice_com(loop):
    global win, turn
    global select_piece, choice_x, choice_y, back_choice_x, back_choice_y

    # 現状のボードの状態を保存
    save()
    win_simulation = [0]*25
    
    for y in range(5):
        load()
        for x in range(5):
            load()
            
            # 端以外の駒は選択できない
            if (1 <= x <=3 and 1 <= y <= 3):
                continue
            # プレイヤーのマークの駒は選択できない
            if (board[y][x] == mark[player]):
                continue

            win_simulation[y*5 + x] = 1

            # 勝敗がつくまで繰り返す回数
            for i in range(loop):
                # 変更前のボードの状態
                load()
                win = 0

                # 選んだ駒の指定
                choice_x = x
                choice_y = y
                board[choice_x][choice_y] = mark[turn]
                
                # 勝敗がつくまで繰り返す
                while True:
                    put_simulation(turn)
                    slide_piece()
                    judge()
                    # 勝敗が決まればループを抜ける
                    if win > 0:
                        break
                    turn = abs(turn - 1)
                    choice_simulation(turn)

                # 最初に選んだ駒の位置で勝った場合
                if win == mark[computer]:
                    win_simulation[y*5 + x] += 1

    # 勝ち数が最大の位置
    m = 0
    n = 0
    print("choice_com")
    for i in range(5*5):
        if win_simulation[i] > m:
            m = win_simulation[i]
            n = i

    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[0],win_simulation[1],win_simulation[2],win_simulation[3],win_simulation[4]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[5],win_simulation[6],win_simulation[7],win_simulation[8],win_simulation[9]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[10],win_simulation[11],win_simulation[12],win_simulation[13],win_simulation[14]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[15],win_simulation[16],win_simulation[17],win_simulation[18],win_simulation[19]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[20],win_simulation[21],win_simulation[22],win_simulation[23],win_simulation[24]))
    print()
    
    # シミュレーションで得られた位置
    select_piece = True
    choice_x = n%5
    choice_y = int(n/5)
    back_choice_x = choice_x
    back_choice_y = choice_y    

    # シミュレーション前の状態
    turn = computer
    win = 0
    load()




def put_com(loop):
    global win, turn
    global select_piece, choice_x, choice_y, back_choice_x, back_choice_y, put_x, put_y

    # 現場のボードの状態を保存
    save()
    win_simulation = [0]*25
    # 駒の置ける位置を取得
    put_pos= put_position()
    count = int(len(put_pos)/2)
    
    # 繰り返し：駒の置ける位置の回数分
    for i in range(count):
        load()
        # 最初に置く駒の位置
        x = put_pos[i*2]
        y = put_pos[i*2 + 1]
        put_x = x
        put_y = y

        # 繰り返し：勝敗の決着をつける回数
        for j in range(loop):
            load()
            win = 0
            # choice_com()で選んだ駒
            choice_x = back_choice_x
            choice_y = back_choice_x

            # 決着がつくまで繰り返す
            while True:
                slide_piece()
                judge()
                if win > 0:
                    break
                turn = abs(turn - 1)
                choice_simulation(turn)
                put_simulation(turn)

            # 最初に選んだ駒の位置で勝った場合
            if win == mark[computer]:
                win_simulation[y*5 + x] += 1

    # 勝ち数が最大の位置
    m = 0
    n = 0
    print("put_com")
    for i in range(25):
        if win_simulation[i] > m:
            m = win_simulation[i]
            n = i

    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[0],win_simulation[1],win_simulation[2],win_simulation[3],win_simulation[4]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[5],win_simulation[6],win_simulation[7],win_simulation[8],win_simulation[9]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[10],win_simulation[11],win_simulation[12],win_simulation[13],win_simulation[14]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[15],win_simulation[16],win_simulation[17],win_simulation[18],win_simulation[19]))
    print("{:3d} {:3d} {:3d} {:3d} {:3d}".format(win_simulation[20],win_simulation[21],win_simulation[22],win_simulation[23],win_simulation[24]))
    print()
    print()
            
    # シミュレーションで得られた位置
    select_piece = True
    put_x = n%5
    put_y = int(n/5)
    choice_x = back_choice_x
    choice_y = back_choice_y

    # シミュレーション前の状態
    turn = computer
    win = 0
    load()



        
# ============================================================
#                           GAME
# ============================================================

# ******************** ボード(駒)の初期化 ********************
def init_game():
    global win, turn, player, computer
    global select_piece, choice_x, choice_y, put_x, put_y
    
    # ボードの駒を全て無印に
    for y in range(5):
        for x in range(5):
            board[y][x] = MUJIRUSI
    win = 0
    turn = 0
    player = 0
    computer = 0
    select_piece = False
    choice_x = 0
    choice_y = 0
    put_x = 0
    put_y = 0


# ******************** 揃ったか判定 ********************
def judge():
    global win

    for mark in range(1, 3):
        # 横方向
        for y in range(5):
            same_mark = 0
            for x in range(5):
                if mark == board[y][x]:
                    same_mark += 1
                if same_mark == 5:
                    win = mark
        # 縦方向
        for x in range(5):
            same_mark = 0
            for y in range(5):
                if mark == board[y][x]:
                    same_mark += 1
                if same_mark == 5:
                    win = mark
        # 右斜め方向
        same_mark = 0
        for n in range(5):
            if mark == board[n][n]:
                same_mark += 1
            if same_mark == 5:
                win = mark
        # 左斜め方向
        same_mark = 0
        for n in range(5):
            if mark == board[n][4-n]:
                same_mark += 1
            if same_mark == 5:
                win = mark


# ============================================================
#                           MAIN
# ============================================================

# ******************** メインループ ********************
def main():
    global idx, tmr, win
    global turn
    global select_piece
    
    pygame.init()
    pygame.display.set_caption("QUIXO GAME")

    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()

    while True:
        tmr += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # マウスのクリック
        mBtn_1, mBtn_2, mBtn_3 = pygame.mouse.get_pressed()
        mb = mBtn_1
        # マウスのx,y座標 -> 配列の位置
        mouseX, mouseY = pygame.mouse.get_pos()
        mx = int( (mouseX - KUHAKU) / IMAGE_SIZE )
        my = int( (mouseY - KUHAKU) / IMAGE_SIZE )
        # 配列の範囲外の調整
        if mx < 0:  mx = 0
        if mx > 4:  mx = 4
        if my < 0:  my = 0
        if my > 4:  my = 4

        # タイトル画面：先攻／後攻の選択
        if idx == 0:
            if tmr == 1:
                # ゲームの初期化
                init_game()

            # タイトル画面の表示
            draw_title(screen, mouseX, mouseY, mb)


        # 移動させる駒を選ぶ
        elif idx == 1:
            if tmr > 10:
                # ターン：プレイヤー
                if turn == player:                    
                    choice_piece(mx, my, mb, player)

                # ターン：コンピュータ
                elif turn == computer:
                    choice_com(loop)

                # 駒を選んだ場合
                if select_piece == True:
                    select_piece = False
                    board[choice_y][choice_x] = mark[turn]
                    idx = 2
                    tmr = 0

        # 選んだ駒の置く位置を選択
        elif idx == 2:
            if tmr > 10:
                # ターン：プレイヤー
                if turn == player:
                    put_piece(mx, my, mb, player)

                # ターン：コンピュータ
                elif turn == computer:
                    put_com(loop)
                    
                # 駒を選んだ場合
                if select_piece == True:
                    select_piece = False
                    idx = 3
                    tmr = 0

        # 駒をスライドさせる
        elif idx == 3:
            slide_piece()

            # どこかの列が揃った場合 -> 勝敗が決まる
            judge()
            if win > 0:
                idx = 4
                tmr = 0
            else: # 決まらなければ、ターンを交代
                turn = abs(turn - 1)
                idx = 1
                tmr = 0

        # 勝敗決定
        elif idx == 4:
            if win == mark[player]:
                draw_text(screen, "PLAYER WIN!", SCREEN_SIZE/2, SCREEN_SIZE/2, 100, RED)
            elif win == mark[computer]:
                draw_text(screen, "COMPUTER WIN!", SCREEN_SIZE/2, SCREEN_SIZE/2, 100, BLUE)
            
            if tmr == 100:
                idx = 0
                tmr = 0

        # ボードの描画(タイトル画面を除く)
        if idx != 0:
            draw_board(screen)



    
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
