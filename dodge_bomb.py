import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = { #移動用辞書
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0),
}


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：横方向，縦方向の画面内外判定結果
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True  # 初期値：画面内
    if rct.left < 0 or WIDTH < rct.right:  # 横方向の画面外判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向の画面外判定
        tate = False
    return yoko, tate  # 横方向，縦方向の画面内判定結果を返す


def gameover(screen: pg.Surface) -> None:#ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数
       #画面をブラックアウト
       bo_img = pg.Surface((WIDTH, HEIGHT))
       pg.draw.rect(bo_img, (0,0,0), pg.Rect(0,0,WIDTH,HEIGHT))
       bo_img.set_alpha(50)
       screen.blit(bo_img, [0, 0])
       #泣いているこうかとん画像
       kk_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
       screen.blit(kk_img2, [320,250])
       screen.blit(kk_img2, [700,250])
       #「Game Over」の文字列
       fonto = pg.font.Font(None, 80)
       txt = fonto.render("Game Over", True, (255,255,255))
       screen.blit(txt, [380, 250])
       # display.update()する関数を実装
       pg.display.update()
       #5秒間表示
       time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    #サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す関数の定義
    bb_accs = [a for a in range(1, 11)]
    bb_imgs =[]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img.set_colorkey((0,0,0))
        bb_imgs.append(bb_img)
    return bb_imgs,bb_accs


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    for key1 in DELTA2.items():
        if sum_mv == key1:
            kk_img2 = DELTA2[key1]
    return kk_img2


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))# 空のSurfaceを作る（爆弾用）
    pg.draw.circle(bb_img, (255, 0, 0),(10,10),10) # 赤い円を描く
    bb_img.set_colorkey((0,0,0)) # 黒を透明色に設定
    bb_rct = bb_img.get_rect()# 爆弾Rectを取得
    bb_rct.centerx = random.randint(0,WIDTH) # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)# 縦座標用の乱数
    vx, vy = +5 ,+5# 爆弾の移動速度
    clock = pg.time.Clock()
    tmr = 0
    DELTA2 ={
    (+5,0):pg.transform.rotozoom(kk_img, 0, 1.0),
    (+5,-5):pg.transform.rotozoom(kk_img, 45, 1.0),
    (0,-5):pg.transform.rotozoom(kk_img, 90, 1.0),
    (-5,-5):pg.transform.rotozoom(kk_img, 135, 1.0),
    (-5,0):pg.transform.rotozoom(kk_img, 180, 1.0),
    (-5,+5):pg.transform.rotozoom(kk_img, 225, 1.0),
    (0,+5):pg.transform.rotozoom(kk_img, 270, 1.0),
    (+5,+5):pg.transform.rotozoom(kk_img, 315, 1.0),
}
    bb_imgs, bb_accs = init_bb_imgs()
    kk_img = get_kk_img((0, 0)) 
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            #ゲームオーバー時に，半透明の黒い画面上に「Game Over」と表示し，泣いているこうかとん画像を貼り付ける関数の呼び出し
            gameover(screen)
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        kk_img = get_kk_img(tuple(sum_mv))
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 移動をなかったことにする
        #サイズの異なる爆弾Surfaceを要素としたリストと加速度リストを返す関数の呼び出し
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(avx, avy)# 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            vx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)# 爆弾の描画
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
