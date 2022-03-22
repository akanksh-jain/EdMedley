from pydoc import render_doc
import pygame as pg
import os
pg.font.init()

WIN = pg.display.set_mode((1280,720))
WIDTH, HEIGHT = WIN.get_width(),WIN.get_height()
pg.display.set_caption("EDMEDLEY")

CAR_IMAGE_PNG = pg.image.load(os.path.join('Assets','car.png'))
CACTUS_SHORT_IMAGE_JPG = pg.image.load(os.path.join('Assets','Cactus_Short.jpg'))
CACTUS_TALL_IMAGE_PNG = pg.image.load(os.path.join('Assets','Cactus_Tall.png'))

SCALE = .2
CAR_IMAGE = pg.transform.scale(CAR_IMAGE_PNG, ((int)(WIDTH*SCALE*0.9),(int)(HEIGHT*SCALE)))
CACTUS_SHORT_IMAGE = pg.transform.scale(CACTUS_SHORT_IMAGE_JPG, ((int)(WIDTH*SCALE//2),(int)(HEIGHT*SCALE//2)))
CACTUS_TALL_IMAGE = pg.transform.scale(CACTUS_TALL_IMAGE_PNG, ((int)(WIDTH*SCALE),(int)(HEIGHT*SCALE*2)))

MOVE_LEFT = pg.USEREVENT + 1
MOVE_RIGHT = pg.USEREVENT + 2

CURRENT_POS = 0;

def draw_window(car, ground, sky, cactus_short, cactus_tall, sign_1, sign_1_border, sign_1_text, sign_1_text_rect):
    WIN.fill((155,155,155))
    pg.draw.rect(WIN, (255, 200, 50), ground)
    pg.draw.rect(WIN, (100, 175, 255), sky)

    pg.draw.rect(WIN, (0, 175, 0), sign_1)
    pg.draw.rect(WIN, (255,255,255), sign_1_border, 4, border_radius= 15)
    WIN.blit(sign_1_text, sign_1_text_rect)

    WIN.blit(CACTUS_SHORT_IMAGE,(cactus_short.x,cactus_short.y))
    WIN.blit(CACTUS_TALL_IMAGE,(cactus_tall.x,cactus_tall.y))
    WIN.blit(CAR_IMAGE,(car.x,car.y))

    pg.display.update()



def handle_car_movement(keys_pressed, car):
    #Changed coordinate based system with discrete position, -1 left, 0 center, 1 right
    global CURRENT_POS;
    if keys_pressed[pg.K_LEFT] and CURRENT_POS != -1:
        pg.event.post(pg.event.Event(MOVE_LEFT))
        pg.time.delay(100)
        CURRENT_POS = CURRENT_POS - 1;
        # car.x-=CAR_IMAGE.get_width()

    if keys_pressed[pg.K_RIGHT] and CURRENT_POS != 1:
        pg.event.post(pg.event.Event(MOVE_RIGHT))
        pg.time.delay(100)
        CURRENT_POS = CURRENT_POS + 1;
        #car.x+=CAR_IMAGE.get_width()

def handle_cactus_movements(cactus_short, cactus_long):
    if(cactus_short.y >= HEIGHT):
        cactus_short.y = int(HEIGHT * .75) - CACTUS_SHORT_IMAGE.get_height()
    cactus_short.y = cactus_short.y + 15;

    if(cactus_long.y >= HEIGHT):
        cactus_long.y = int(HEIGHT * .75) - CACTUS_TALL_IMAGE.get_height()
    cactus_long.y = cactus_long.y + 15;

def main():

    #Meant to simulate car rumbling as driving
    rumbleUp = True;
    rumbleDistance = 2;

    car = pg.Rect( WIDTH // 2 - CAR_IMAGE.get_width() // 2,(int)(HEIGHT * .75) - CAR_IMAGE.get_height() // 2 - rumbleDistance // 2, CAR_IMAGE.get_width(), CAR_IMAGE.get_height())
    ground = pg.Rect(0, int(HEIGHT * .75), WIDTH, HEIGHT - int(HEIGHT * .75))
    sky = pg.Rect(0, 0, WIDTH, int(HEIGHT * .75))

    if(not pg.font.get_init):
        pg.font.init;
    font = pg.font.Font('freesansbold.ttf', 150);

    sign_1 = pg.Rect(30, 100, 300, 250);
    sign_1_border = pg.Rect(30, 100, 300, 250);
    sign_1_text = font.render('50', True, (255, 255, 255));
    sign_1_text_rect = sign_1_text.get_rect();
    sign_1_text_rect.center = (165, 175);

    cactus_short = pg.Rect(60, int(HEIGHT * .75) - CACTUS_SHORT_IMAGE.get_height(), CACTUS_SHORT_IMAGE.get_width(), CACTUS_SHORT_IMAGE.get_height())
    cactus_tall = pg.Rect(950, int(HEIGHT * .75) - CACTUS_TALL_IMAGE.get_height(), CACTUS_TALL_IMAGE.get_width(), CACTUS_TALL_IMAGE.get_height())


    clock = pg.time.Clock()
    run = True
    while run:
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            
            if pg.key.get_focused and event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False

            if event.type == MOVE_LEFT:
                car.x -= CAR_IMAGE.get_width()
            if event.type == MOVE_RIGHT:
                car.x+=CAR_IMAGE.get_width()

        if(rumbleUp):
            car.y -= rumbleDistance
        else:
            car.y += rumbleDistance
        rumbleUp = not rumbleUp;

        keys_pressed = pg.key.get_pressed()
        handle_car_movement(keys_pressed,car)
        handle_cactus_movements(cactus_short, cactus_tall);
        draw_window(car, ground, sky, cactus_short, cactus_tall, sign_1, sign_1_border, sign_1_text, sign_1_text_rect)
    pg.quit()

if __name__ == "__main__":
    main()