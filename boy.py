import math

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

def time_out_5(e):
    return e[0] == 'TIME_OUT' and e[1] == 5.0


class Sleep:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        print('눕다')

    @staticmethod
    def exit(boy):
        print('일어서기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                      math.pi / 2, '', boy.x - 25, boy.y - 25, 100, 100)
        pass


class Idle:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.start_time = get_time()  # 경과시간
        print('Idle Entry Action')

    @staticmethod
    def exit(boy):
        print('Idle Exit Action')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))
        print('Idle Do')

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class AutoRun:
    @staticmethod
    def enter(boy):
        boy.frame = 0
        boy.dir = 1
        boy.action = 1
        boy.scale = 2  # 크기를 2배로 설정
        print('AutoRun Entry Action')

    @staticmethod
    def exit(boy):
        print('AutoRun Exit Action')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5
        if boy.x > 800:
            boy.x = 800
            boy.dir = -1
            boy.action = 0
        elif boy.x < 0:
            boy.x = 0
            boy.dir = 1
            boy.action = 1
        print('AutoRun Do')

    @staticmethod
    def draw(boy):
        # 크기
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y, 100 * boy.scale, 100 * boy.scale)




class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Sleep
        self.table = {
            Sleep: {space_down: Idle, time_out: AutoRun},
            Idle: {space_down: Sleep, time_out: AutoRun},
            AutoRun: {space_down: Sleep, time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy)
                self.cur_state = next_state
                self.cur_state.enter(self.boy)
                return True

        return False

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)



class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        print(event)
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
