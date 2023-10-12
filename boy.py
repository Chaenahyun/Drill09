from pico2d import load_image, get_time


from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDL_KEYUP, SDLK_RIGHT, SDLK_LEFT

class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = None
        self.transitions = {
            None: {space_down: Idle},
            Idle: {right_down: Run, left_down: Run},
            Run: {right_up: Idle, left_up: Idle}
        }
        self.cur_state = None

    def start(self):
        self.change_state(None)

    def change_state(self, state):
        if self.cur_state is not None:
            self.cur_state.exit(self.boy)
        self.cur_state = state
        self.cur_state.enter(self.boy)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.change_state(next_state)
                return True
        return False

class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.state_machine.handle_event(('INPUT', {'type': SDL_KEYDOWN, 'key': SDLK_SPACE}))

    def update(self):
        self.state_machine.handle_event(('TIME_OUT',))
        self.state_machine.handle_event(('INPUT', {'type': SDL_KEYDOWN, 'key': SDLK_SPACE}))

    def handle_event(self, event):
        pass

    def draw(self):
        self.state_machine.cur_state.draw(self)

class Idle:
    @staticmethod
    def enter(boy):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time()

    @staticmethod
    def exit(boy):
        pass

    @staticmethod
    def do(boy):
        if get_time() - boy.wait_time > 2.0:  # 2 seconds
            boy.frame = (boy.frame + 1) % 8
            boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

def right_down(e):
    return e[0] == 'INPUT' and e[1]['type'] == SDL_KEYDOWN and e[1]['key'] == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1]['type'] == SDL_KEYUP and e[1]['key'] == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1]['type'] == SDL_KEYDOWN and e[1]['key'] == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1]['type'] == SDL_KEYUP and e[1]['key'] == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1]['type'] == SDL_KEYDOWN and e[1]['key'] == SDLK_SPACE

def time_out_3(e):
    return e[0] == 'TIME_OUT'
