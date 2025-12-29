from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty

try:
    from mobile_app.widgets.floating import FloatingWidget
except ImportError:
    FloatingWidget = None


Window.size = (360, 640)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(
            text='领飚渗透助手',
            font_size='28sp',
            halign='center',
            size_hint_y=None,
            height=60
        ))
        layout.add_widget(Label(
            text='手机轻量版',
            font_size='16sp',
            halign='center',
            size_hint_y=None,
            height=30
        ))
        self.target_input = TextInput(
            hint_text='输入URL/账号/手机号/关键词',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.target_input)
        query_btn = Button(
            text='🔍 一键查询',
            font_size='18sp',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        query_btn.bind(on_press=self.start_query)
        layout.add_widget(query_btn)
        history_btn = Button(
            text='📋 历史记录',
            font_size='18sp',
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.7, 0.4, 1)
        )
        history_btn.bind(on_press=self.show_history)
        layout.add_widget(history_btn)
        status_label = Label(
            text='就绪 | 悬浮窗已开启',
            font_size='14sp',
            halign='center',
            size_hint_y=None,
            height=30
        )
        self.status_label = status_label
        layout.add_widget(status_label)
        layout.add_widget(Label())
        layout.add_widget(Label())
        self.add_widget(layout)

    def start_query(self, instance):
        target = self.target_input.text.strip()
        if not target:
            self.status_label.text = '请输入查询目标'
            return
        self.status_label.text = '查询中...'
        app = App.get_running_app()
        app.query_target = target
        Clock.schedule_once(self._do_query, 0.5)

    def _do_query(self, dt):
        self.manager.current = 'query'

    def show_history(self, instance):
        self.status_label.text = '历史记录功能开发中'
        app = App.get_running_app()
        app.show_toast('历史记录功能开发中')


class QueryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(
            text='← 返回',
            font_size='16sp',
            size_hint_x=None,
            width=80,
            background_color=(0.3, 0.3, 0.3, 1)
        )
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(
            text='查询结果',
            font_size='20sp',
            halign='center'
        ))
        layout.add_widget(header)
        self.result_area = ScrollView(size_hint=(1, 1))
        self.result_content = Label(
            text='正在查询...\n',
            font_size='14sp',
            halign='left',
            valign='top'
        )
        self.result_content.bind(size=self.result_content.setter('text_size'))
        self.result_area.add_widget(self.result_content)
        layout.add_widget(self.result_area)
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        export_btn = Button(
            text='📄 导出',
            font_size='16sp',
            background_color=(0.2, 0.7, 0.5, 1)
        )
        export_btn.bind(on_press=self.export_report)
        btn_layout.add_widget(export_btn)
        share_btn = Button(
            text='📤 分享',
            font_size='16sp',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        share_btn.bind(on_press=self.share_report)
        btn_layout.add_widget(share_btn)
        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

    def export_report(self, instance):
        self.result_content.text += '\n\n📄 报告已导出到: /sdcard/Download/'

    def share_report(self, instance):
        app = App.get_running_app()
        app.show_toast('分享功能开发中')


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        header = BoxLayout(size_hint_y=None, height=50)
        back_btn = Button(
            text='← 返回',
            font_size='16sp',
            size_hint_x=None,
            width=80,
            background_color=(0.3, 0.3, 0.3, 1)
        )
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        header.add_widget(Label(
            text='设置',
            font_size='20sp',
            halign='center'
        ))
        layout.add_widget(header)
        layout.add_widget(Label(
            text='悬浮窗设置',
            font_size='18sp',
            size_hint_y=None,
            height=40
        ))
        switch_layout = BoxLayout(size_hint_y=None, height=50)
        switch_layout.add_widget(Label(text='显示悬浮窗', font_size='16sp'))
        self.floating_switch = Button(
            text='开',
            font_size='14sp',
            size_hint_x=None,
            width=60,
            background_color=(0.2, 0.7, 0.5, 1)
        )
        self.floating_switch.bind(on_press=self.toggle_floating)
        switch_layout.add_widget(self.floating_switch)
        layout.add_widget(switch_layout)
        layout.add_widget(Label(
            text='拖动悬浮窗可调整位置',
            font_size='14sp',
            halign='center'
        ))
        layout.add_widget(Label())
        layout.add_widget(Label())
        self.add_widget(layout)

    def go_back(self, instance):
        self.manager.current = 'home'

    def toggle_floating(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'floating_widget'):
            app.floating_widget.opacity = 1 - app.floating_widget.opacity
            if app.floating_widget.opacity > 0.5:
                self.floating_switch.text = '开'
                self.floating_switch.background_color = (0.2, 0.7, 0.5, 1)
            else:
                self.floating_switch.text = '关'
                self.floating_switch.background_color = (0.7, 0.3, 0.3, 1)


class LingbiaoMobileApp(App):
    query_target = StringProperty('')
    toast_message = StringProperty('')
    
    def build(self):
        self.query_target = ''
        self._floating = None
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(QueryScreen(name='query'))
        sm.add_widget(SettingsScreen(name='settings'))
        self.sm = sm
        return sm

    def on_start(self):
        try:
            from android.permissions import request_permissions, Permission
            from android import android_api_level
            request_permissions([
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE
            ])
            if android_api_level() >= 23:
                request_permissions([
                    Permission.SYSTEM_ALERT_WINDOW
                ])
        except ImportError:
            pass
        Clock.schedule_once(self._add_floating_widget, 1)

    def _add_floating_widget(self, dt):
        if not self._floating and FloatingWidget:
            try:
                self._floating = FloatingWidget(app_instance=self)
                Window.add_widget(self._floating)
                self.floating_widget = self._floating
            except Exception as e:
                pass

    def on_floating_action(self, action):
        if action == 'query':
            self.sm.current = 'query'
        elif action == 'history':
            self.show_toast('历史记录功能开发中')
        elif action == 'report':
            self.show_toast('请先执行查询')
        elif action == 'settings':
            self.sm.current = 'settings'

    def show_toast(self, message):
        self.toast_message = message
        Clock.schedule_once(self._hide_toast, 2)

    def _hide_toast(self, dt):
        self.toast_message = ''

    def on_pause(self):
        return True

    def on_resume(self):
        pass


if __name__ == '__main__':
    LingbiaoMobileApp().run()
