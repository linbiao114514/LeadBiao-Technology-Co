from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty, NumericProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window


class FloatingMenuButton(Button):
    def __init__(self, text='', size_hint=(None, None), **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = size_hint
        self.font_size = '20sp'
        self.background_color = (0.2, 0.6, 0.9, 1)
        self.bind(pos=self.update_pos, size=self.update_pos)

    def update_pos(self, *args):
        pass


class FloatingWidget(FloatLayout):
    expanded = BooleanProperty(False)
    menu_items = []
    
    def __init__(self, app_instance=None, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.size_hint = (None, None)
        self.size = (60, 60)
        self.menu_open = False
        self.menu_buttons = []
        self._drag = False
        self._drag_touch = None
        
        self.main_button = FloatingMenuButton(
            text='🔍',
            size=(60, 60),
            pos_hint={'right': 1, 'top': 0.95},
            background_color=(0.2, 0.6, 0.9, 1),
            on_press=self.toggle_menu
        )
        self.add_widget(self.main_button)
        
        self.menu_items = [
            {'text': '📊', 'action': 'query', 'tooltip': '快速查询'},
            {'text': '📋', 'action': 'history', 'tooltip': '历史记录'},
            {'text': '📄', 'action': 'report', 'tooltip': '导出报告'},
            {'text': '⚙️', 'action': 'settings', 'tooltip': '设置'},
        ]
        
        for item in self.menu_items:
            btn = FloatingMenuButton(
                text=item['text'],
                size=(50, 50),
                pos_hint={'right': 1, 'top': 0.95},
                background_color=(0.3, 0.7, 0.5, 1),
                opacity=0
            )
            btn.bind(on_press=lambda x, a=item['action']: self.on_menu_action(a))
            btn.action = item['action']
            btn.tooltip = item['tooltip']
            self.menu_buttons.append(btn)
            self.add_widget(btn)
        
        self.label = Button(
            text='',
            font_size='10sp',
            size_hint=(None, None),
            size=(60, 20),
            pos_hint={'right': 1, 'top': 0.95},
            background_color=(0.1, 0.1, 0.1, 0.7),
            opacity=0
        )
        self.add_widget(self.label)
    
    def toggle_menu(self, instance):
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()
    
    def open_menu(self):
        self.menu_open = True
        anim = Animation(background_color=(0.9, 0.3, 0.3, 1), duration=0.2)
        anim.start(self.main_button)
        
        for i, btn in enumerate(self.menu_buttons):
            y_pos = 0.95 - (i + 1) * 0.1
            btn.pos_hint = {'right': 1, 'top': y_pos}
            anim = Animation(opacity=1, duration=0.2)
            anim.start(btn)
    
    def close_menu(self):
        self.menu_open = False
        anim = Animation(background_color=(0.2, 0.6, 0.9, 1), duration=0.2)
        anim.start(self.main_button)
        
        for btn in self.menu_buttons:
            anim = Animation(opacity=0, duration=0.2)
            anim.start(btn)
    
    def on_menu_action(self, action):
        self.close_menu()
        if hasattr(self.app, 'on_floating_action'):
            Clock.schedule_once(lambda dt: self.app.on_floating_action(action), 0.3)
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.menu_open:
                for btn in self.menu_buttons:
                    if btn.collide_point(*touch.pos):
                        return super().on_touch_down(touch)
            self._drag = True
            self._drag_touch = touch
            self._touch_start = touch.pos
            self._start_x = self.x
            self._start_y = self.y
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self._drag and touch == self._drag_touch:
            dx = touch.pos[0] - self._touch_start[0]
            dy = touch.pos[1] - self._touch_start[1]
            new_x = self._start_x + dx
            new_y = self._start_y + dy
            new_x = max(0, min(Window.width - 60, new_x))
            new_y = max(0, min(Window.height - 60, new_y))
            self.pos = (new_x, new_y)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self._drag and touch == self._drag_touch:
            self._drag = False
            self._drag_touch = None
            return True
        return super().on_touch_up(touch)
