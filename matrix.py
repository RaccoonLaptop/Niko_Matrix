# -*- coding: utf-8 -*-
"""
Matrix Rain Effect - Надпись из падающих символов.
Измените TEXT_MASK ниже: # = рисуем, пробел = пусто.
Управление: ESC - выход, F11 - полноэкранный режим
"""

import pygame
import random
import sys
import os
import subprocess
import math
import webbrowser

# ========== РЕЖИМ ОКНА ==========
START_FULLSCREEN = False   # True = запуск в полноэкранном, False = в окне
PANEL_WIDTH = 220         # ширина боковой панели
HOVER_ZONE = 2            # только самый край окна (1-2 пикселя)
BUTTON_HEIGHT = 56        # высота кнопки
STRIP_WIDTH = 4           # полоска статуса у кнопок (лайм=вкл, красный=выкл)
DOCK_WIDTH = 180          # ширина левой панели приложений
DOCK_ICON_SIZE = 44       # размер иконки приложения
DOCK_PADDING = 14         # отступ в панели

CDPI_GITHUB = 'https://github.com/Storik4pro/cdpiui'
VPN_URL = 'https://t.me/Aero_Tunnel'
DNS_URL = 'https://www.comss.ru/list.php?c=securedns'

# ========== ВРЕМЯ — настраивайте здесь ==========
ALWAYS_VISIBLE = False   # True = надпись всегда видна, False = цикл появление/исчезновение
APPEAR_SEC = 2          # появление (если ALWAYS_VISIBLE=False)
VISIBLE_SEC = 10        # надпись видна (если ALWAYS_VISIBLE=False)
DISAPPEAR_SEC = 2       # исчезновение (если ALWAYS_VISIBLE=False)
PAUSE_SEC = 2           # пауза (если ALWAYS_VISIBLE=False)
FPS = 20                # кадров в секунду
PERSIST_FRAMES = 200     # сколько кадров символ держится после попадания в надпись

# ========== НАДПИСЬ — редактируйте здесь ==========
# # = рисуем символ, пробел = пусто

TEXT_MASK = """
##   ##        ##           
###  ##   ##   ##  ##    #### 
#### ##        ## ##    ##  ##
## ####   ##   ####     ##  ##
##  ###   ##   ## ##    ##  ##
##   ##   ##   ##  ##    #### 
"""

CHARS = list("ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")

BRIGHT_GREEN = (0, 255, 0)
TRAIL_GREEN = (0, 180, 80)

LANG = {
    'ru': {
        'exit': 'Выход', 'exit_key': '(ESC)',
        'text': 'Текст', 'text_key': '(Alt+T)', 'text_on': 'Вкл', 'text_off': 'Выкл',
        'fullscreen': 'Полный экран', 'fullscreen_key': '(Alt+Enter)',
        'refresh': 'Обновить окно', 'refresh_key': '(Alt+O)',
        'lang': 'Язык', 'lang_key': '(L)', 'lang_ru': 'RU', 'lang_en': 'EN',
        'inscription': 'Надпись', 'inscription_key': '(N)',
        'mask_hint': '# = символ, пробел = пусто',
        'always_visible': 'Всегда видна',
        'appear_sec': 'Появление (с)', 'visible_sec': 'Видна (с)', 'disappear_sec': 'Исчезновение (с)',
        'pause_sec': 'Пауза (с)', 'persist_frames': 'Держать кадров',
        'ok': 'ОК', 'cancel': 'Отмена',
        'timing': 'Настройки времени',
        'reset_inet': 'Сброс интернета',
        'reset_full': 'Полный сброс', 'reset_winsock': 'Winsock',
        'reset_ip': 'Сброс IP', 'reset_dns': 'Очистка DNS',
        'close': 'Закрыть',
        'about': 'О программе', 'about_key': '(A)',
        'author': 'Автор программы', 'fio': 'ФИО:', 'email': 'Почта:',
        'nick': 'Псевдоним:', 'github': 'GitHub:',
        'dock_desc': 'Утилиты', 'cdpi': 'CDPI — обход DPI',
        'dock_reset_inet': 'Сброс интернета', 'dock_cdpi': 'Обход DPI',
        'dock_vpn': 'VPN', 'dock_dns': 'DNS',
    },
    'en': {
        'exit': 'Exit', 'exit_key': '(ESC)',
        'text': 'Text', 'text_key': '(Alt+T)', 'text_on': 'On', 'text_off': 'Off',
        'fullscreen': 'Fullscreen', 'fullscreen_key': '(Alt+Enter)',
        'refresh': 'Refresh window', 'refresh_key': '(Alt+O)',
        'lang': 'Language', 'lang_key': '(L)', 'lang_ru': 'RU', 'lang_en': 'EN',
        'inscription': 'Inscription', 'inscription_key': '(N)',
        'mask_hint': '# = char, space = empty',
        'always_visible': 'Always visible',
        'appear_sec': 'Appear (s)', 'visible_sec': 'Visible (s)', 'disappear_sec': 'Disappear (s)',
        'pause_sec': 'Pause (s)', 'persist_frames': 'Persist frames',
        'ok': 'OK', 'cancel': 'Cancel',
        'timing': 'Timing settings',
        'reset_inet': 'Internet Reset',
        'reset_full': 'Full Reset', 'reset_winsock': 'Winsock',
        'reset_ip': 'IP Reset', 'reset_dns': 'Clear DNS',
        'close': 'Close',
        'about': 'About', 'about_key': '(A)',
        'author': 'Program author', 'fio': 'Name:', 'email': 'Email:',
        'nick': 'Nickname:', 'github': 'GitHub:',
        'dock_desc': 'Utilities', 'cdpi': 'CDPI — DPI bypass',
        'dock_reset_inet': 'Internet Reset', 'dock_cdpi': 'DPI bypass',
        'dock_vpn': 'VPN', 'dock_dns': 'DNS',
    }
}

ABOUT_NICK = 'Niko'
ABOUT_FIO = 'Хасбатуллин Ильшат'
ABOUT_EMAIL = '1998ilshat@mail.ru'
ABOUT_GITHUB = 'https://github.com/RaccoonLaptop'


class MatrixRainNiko:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Niko_Matrix")
        self.font_size = 14
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        try:
            self.font = pygame.font.SysFont("consolas", self.font_size)
        except:
            pass
        self.clock = pygame.time.Clock()
        self.frame = 0
        self.persistent_hits = []
        self._fullscreen = START_FULLSCREEN
        self.show_text = True
        self.panel_font = None
        self.lang = 'ru'
        self.panel_visible = False
        self.text_mask = TEXT_MASK
        self.always_visible = ALWAYS_VISIBLE
        self.appear_sec = APPEAR_SEC
        self.visible_sec = VISIBLE_SEC
        self.disappear_sec = DISAPPEAR_SEC
        self.pause_sec = PAUSE_SEC
        self.persist_frames = PERSIST_FRAMES
        self._edit_mode = False
        self._edit_lines = []
        self._edit_cursor_row = 0
        self._edit_cursor_col = 0
        self._edit_scroll = 0
        self._edit_focus = None
        self._edit_num_buffers = {}
        self._panel_buttons = []
        self._refresh_pressed = False
        self._reset_app_open = False
        self._reset_console_lines = []
        self._reset_console_scroll = 0
        self._dock_buttons = []
        self._dock_visible = False
        self._about_open = False
        self._cdpi_icon = None
        self._cdpi_from_file = False
        self._dock_icon_cache = {}
        self._init_display()
        
    def _init_display(self, preserve_size=False):
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        if self._fullscreen:
            self.screen = pygame.display.set_mode((0, 0), flags | pygame.FULLSCREEN)
        else:
            if preserve_size and hasattr(self, 'width') and self.width and self.height:
                size = (self.width, self.height)
            else:
                size = (1280, 720)
            self.screen = pygame.display.set_mode(size, flags | pygame.RESIZABLE)
        self._set_window_icon()
        self._on_resize()
        
    def _set_window_icon(self):
        """Устанавливает иконку окна и панели задач"""
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        for name in ('Niko_Matrix.png', 'icon.ico', 'icon.png'):
            path = os.path.join(base, 'images', name)
            if os.path.isfile(path):
                try:
                    icon = pygame.image.load(path)
                    pygame.display.set_icon(icon)
                    break
                except Exception:
                    pass

    def _on_resize(self):
        self.width, self.height = self.screen.get_size()
        try:
            self.panel_font = pygame.font.SysFont("consolas", 14)
        except:
            self.panel_font = pygame.font.Font(None, 18)
        self.fade_surface = pygame.Surface((self.width, self.height))
        self.fade_surface.set_alpha(13)
        self.fade_surface.fill((0, 0, 0))
        self.columns = self.width // self.font_size
        self.drops = [1] * self.columns
        self.niko_cells = []
        self.niko_cells_set = set()
        self._build_niko_mask()
        
    def _build_niko_mask(self):
        """Маска из text_mask — область где символы дольше видны"""
        lines = self.text_mask.strip('\n').split('\n')
        lines = [l for l in lines if l]
        if not lines:
            return
        cols = max(len(l) for l in lines)
        for i, line in enumerate(lines):
            if len(line) < cols:
                lines[i] = line + ' ' * (cols - len(line))
        rows = len(lines)
        mask_w = cols * self.font_size
        mask_h = rows * self.font_size
        start_x = ((self.width - mask_w) // 2 // self.font_size) * self.font_size
        start_y = ((self.height - mask_h) // 2 // self.font_size) * self.font_size
        
        for row, line in enumerate(lines):
            for col in range(cols):
                ch = line[col] if col < len(line) else ' '
                if ch not in (' ', '\t'):
                    x = start_x + col * self.font_size
                    y = start_y + row * self.font_size
                    if 0 <= x < self.width and 0 <= y < self.height:
                        self.niko_cells.append((x, y))
                        self.niko_cells_set.add((x, y))
        
    def draw_niko(self, niko_hits, visible):
        """Попавшие символы держатся PERSIST_FRAMES кадров"""
        for (x, y, char, color, frames_left) in self.persistent_hits:
            c = (color[0], int(color[1] * visible), color[2])
            self.screen.blit(self.font.render(char, True, c), (x, y))
        still_alive = [(x, y, char, col, n - 1) for (x, y, char, col, n) in self.persistent_hits if n > 1]
        new_with_frames = [(x, y, char, col, self.persist_frames) for (x, y, char, col) in niko_hits]
        seen = set()
        self.persistent_hits = []
        for item in new_with_frames + still_alive:
            key = (item[0], item[1])
            if key not in seen:
                seen.add(key)
                self.persistent_hits.append(item)
    
    def _draw_button(self, surf, rect, label, key, is_hover, strip_color=None):
        """Кнопка в стиле About"""
        fill_col = (30, 70, 45) if is_hover else (18, 45, 28)
        border_col = (0, 200, 120) if is_hover else (0, 160, 90)
        pygame.draw.rect(surf, fill_col, rect)
        pygame.draw.rect(surf, border_col, rect, 1)
        if strip_color is not None:
            pygame.draw.rect(surf, strip_color, (rect.x, rect.y, STRIP_WIDTH, rect.h))
            pygame.draw.rect(surf, strip_color, (rect.right - STRIP_WIDTH, rect.y, STRIP_WIDTH, rect.h))
        pf = self.panel_font or self.font
        lbl = (label[:16] if len(label) > 16 else label)
        txt1 = pf.render(lbl, True, (0, 255, 160))
        txt2 = pf.render(key, True, (0, 220, 140))
        cx = rect.x + rect.w // 2
        surf.blit(txt1, (cx - txt1.get_width() // 2, rect.y + 8))
        surf.blit(txt2, (cx - txt2.get_width() // 2, rect.y + 26))
    
    def _draw_panel(self):
        """Панель: появляется у стенки окна (край), не пропадает пока мышь в панели"""
        mx, my = pygame.mouse.get_pos()
        pw = min(PANEL_WIDTH, self.width // 3)
        px = self.width - pw
        panel_rect = pygame.Rect(px, 0, pw, self.height)
        at_edge = mx >= self.width - HOVER_ZONE  # только стенка окна (самый край)
        in_panel = panel_rect.collidepoint(mx, my)
        if self.panel_visible:
            self.panel_visible = in_panel or at_edge  # скрыть только когда ушли
        else:
            self.panel_visible = at_edge  # показать ТОЛЬКО при наведении на стенку
        if not self.panel_visible:
            return None
        panel = pygame.Surface((pw, self.height))
        panel.set_alpha(235)
        panel.fill((12, 22, 18))
        pygame.draw.rect(panel, (0, 100, 60), (0, 0, pw, self.height), 1)
        pygame.draw.rect(panel, (0, 200, 120), (1, 1, pw - 2, self.height - 2), 1)
        pf = self.panel_font or self.font
        ld = LANG[self.lang]
        btn_margin = 10
        btn_w = pw - 2 * btn_margin
        buttons = []
        y = 15
        btns = [
            ('exit', ld['exit'], ld['exit_key'], 'exit'),
            ('text', ld['text'] + ': ' + (ld['text_on'] if self.show_text else ld['text_off']), ld['text_key'], 'text'),
            ('inscription', ld['inscription'], ld['inscription_key'], 'inscription'),
            ('fullscreen', ld['fullscreen'], ld['fullscreen_key'], 'fullscreen'),
            ('refresh', ld['refresh'], ld['refresh_key'], 'refresh'),
            ('about', ld['about'], ld['about_key'], 'about'),
            ('lang', ld['lang'] + ': ' + self.lang.upper(), ld['lang_key'], 'lang'),
        ]
        for bid, label, key, action in btns:
            br = pygame.Rect(btn_margin, y, btn_w, BUTTON_HEIGHT)
            br_global = pygame.Rect(px + btn_margin, y, btn_w, BUTTON_HEIGHT)
            is_hover = br_global.collidepoint(mx, my)
            if action == 'exit':
                strip_color = (255, 0, 0)  # всегда красный
            elif action == 'text':
                strip_color = (0, 255, 0) if self.show_text else (255, 0, 0)
            elif action == 'fullscreen':
                strip_color = (0, 255, 0) if self._fullscreen else (255, 0, 0)
            elif action == 'refresh':
                strip_color = (255, 0, 0) if self._refresh_pressed else (0, 255, 0)
            elif action == 'inscription':
                strip_color = (0, 255, 0) if self.always_visible else (255, 0, 0)
            elif action == 'about':
                strip_color = None
            else:
                strip_color = None
            self._draw_button(panel, br, label[:16], key, is_hover, strip_color)
            buttons.append((action, br_global))
            y += BUTTON_HEIGHT + 8
        self.screen.blit(panel, (px, 0))
        return buttons
    
    def _load_dock_png(self, filename):
        """Загружает PNG для dock, кэширует. Возвращает Surface или None."""
        if filename in self._dock_icon_cache:
            return self._dock_icon_cache[filename]
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(base, 'images', filename)
        if os.path.isfile(path):
            try:
                img = pygame.image.load(path)
                s = pygame.transform.smoothscale(img, (DOCK_ICON_SIZE, DOCK_ICON_SIZE))
                self._dock_icon_cache[filename] = s
                return s
            except Exception:
                pass
        self._dock_icon_cache[filename] = None
        return None
    
    def _draw_reset_icon(self, surf, rect, color=(0, 255, 0)):
        """Иконка сброса сети: круговые стрелки обновления + wifi-дуги"""
        cx, cy = rect.centerx, rect.centery
        r = min(rect.w, rect.h) // 2 - 5
        arc_rect = (cx - r, cy - r, r * 2, r * 2)
        pygame.draw.arc(surf, color, arc_rect, math.pi * 0.2, math.pi * 1.5, 2)
        pygame.draw.arc(surf, color, arc_rect, math.pi * 1.5, math.pi * 2.8, 2)
        for rr in [r * 2 // 3, r // 3]:
            sr = (cx - rr, cy - rr - 2, rr * 2, rr * 2)
            pygame.draw.arc(surf, color, sr, math.pi * 0.5, math.pi * 1.1, 2)
    
    def _draw_cdpi_icon(self, surf, rect, color=(0, 255, 0)):
        """Иконка обхода DPI: щит + изогнутая стрелка обхода (как у reset_inet — рисуется, без файла)"""
        cx, cy = rect.centerx, rect.centery
        r = min(rect.w, rect.h) // 2 - 5
        # Щит (треугольник/ромб) — символ обхода
        pts = [(cx, cy - r), (cx + r * 0.8, cy + r * 0.4), (cx, cy + r * 0.6), (cx - r * 0.8, cy + r * 0.4)]
        pygame.draw.polygon(surf, color, pts, 2)
        # Стрелка обхода — дуга вокруг
        arc_r = r + 2
        arc_rect = (cx - arc_r, cy - arc_r, arc_r * 2, arc_r * 2)
        pygame.draw.arc(surf, color, arc_rect, math.pi * 0.3, math.pi * 1.7, 2)
    
    def _get_cdpi_icon(self):
        """Загружает CDPIUI.ico/.png если есть, иначе рисует иконку. Возвращает (surface, from_file)."""
        if self._cdpi_icon is not None:
            return self._cdpi_icon, self._cdpi_from_file
        base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        img_dir = os.path.join(base, 'images')
        for name in ('CDPIUI.ico', 'CDPIUI.png'):
            path = os.path.join(img_dir, name)
            if os.path.isfile(path):
                try:
                    img = pygame.image.load(path)
                    self._cdpi_icon = pygame.transform.smoothscale(img, (DOCK_ICON_SIZE, DOCK_ICON_SIZE))
                    self._cdpi_from_file = True
                    return self._cdpi_icon, True
                except Exception:
                    pass
        s = pygame.Surface((DOCK_ICON_SIZE, DOCK_ICON_SIZE))
        s.fill((18, 45, 28))
        r = pygame.Rect(2, 2, DOCK_ICON_SIZE - 4, DOCK_ICON_SIZE - 4)
        self._draw_cdpi_icon(s, r, (0, 220, 140))
        self._cdpi_icon = s
        self._cdpi_from_file = False
        return self._cdpi_icon, False
    
    def _draw_dock(self):
        """Левая панель, появляется при наведении на левый край"""
        mx, my = pygame.mouse.get_pos()
        at_edge_left = mx <= HOVER_ZONE
        dock_rect = pygame.Rect(0, 0, DOCK_WIDTH, self.height)
        in_dock = dock_rect.collidepoint(mx, my)
        if self._dock_visible:
            self._dock_visible = in_dock or at_edge_left
        else:
            self._dock_visible = at_edge_left
        if not self._dock_visible:
            return []
        apps = [('vpn', 'dock_vpn'), ('dns', 'dock_dns'), ('reset_inet', 'dock_reset_inet'), ('cdpi', 'dock_cdpi')]
        dock = pygame.Surface((DOCK_WIDTH, self.height))
        dock.set_alpha(235)
        dock.fill((12, 22, 18))
        pygame.draw.rect(dock, (0, 100, 60), (0, 0, DOCK_WIDTH, self.height), 1)
        pygame.draw.rect(dock, (0, 200, 120), (1, 1, DOCK_WIDTH - 2, self.height - 2), 1)
        pf = self.panel_font or self.font
        desc = LANG[self.lang].get('dock_desc', 'Utilities')
        desc_txt = pf.render(desc, True, (0, 255, 150))
        desc_rect = desc_txt.get_rect(midtop=(DOCK_WIDTH // 2, DOCK_PADDING))
        dock.blit(desc_txt, desc_rect)
        block_h = DOCK_ICON_SIZE + 18
        y0 = desc_rect.bottom + DOCK_PADDING * 2
        buttons = []
        for i, (aid, label_key) in enumerate(apps):
            iy = y0 + i * (block_h + DOCK_PADDING)
            ix = (DOCK_WIDTH - DOCK_ICON_SIZE) // 2
            rect = pygame.Rect(ix, iy, DOCK_ICON_SIZE, DOCK_ICON_SIZE)
            rect_global = pygame.Rect(ix, iy, DOCK_ICON_SIZE, DOCK_ICON_SIZE)
            hov = rect_global.collidepoint(mx, my)
            fill_col = (30, 70, 45) if hov else (18, 45, 28)
            border_col = (0, 200, 120) if hov else (0, 160, 90)
            pygame.draw.rect(dock, fill_col, rect)
            pygame.draw.rect(dock, border_col, rect, 1)
            icon_color = (0, 255, 150) if hov else (0, 200, 120)
            if aid == 'vpn':
                ic = self._load_dock_png('VPN.png')
                if ic:
                    dock.blit(ic, rect)
                    if hov:
                        ov = pygame.Surface((rect.w, rect.h)); ov.fill((0, 255, 150)); ov.set_alpha(50); dock.blit(ov, rect)
                else:
                    self._draw_cdpi_icon(dock, rect, icon_color)
            elif aid == 'dns':
                ic = self._load_dock_png('DNS.png')
                if ic:
                    dock.blit(ic, rect)
                    if hov:
                        ov = pygame.Surface((rect.w, rect.h)); ov.fill((0, 255, 150)); ov.set_alpha(50); dock.blit(ov, rect)
                else:
                    self._draw_cdpi_icon(dock, rect, icon_color)
            elif aid == 'reset_inet':
                ic = self._load_dock_png('Reset_Ethernet.png')
                if ic:
                    dock.blit(ic, rect)
                    if hov:
                        ov = pygame.Surface((rect.w, rect.h)); ov.fill((0, 255, 150)); ov.set_alpha(50); dock.blit(ov, rect)
                else:
                    self._draw_reset_icon(dock, rect, icon_color)
            else:
                ic, from_file = self._get_cdpi_icon()
                if from_file:
                    dock.blit(ic, rect)
                    if hov:
                        ov = pygame.Surface((rect.w, rect.h)); ov.fill((0, 255, 150)); ov.set_alpha(50); dock.blit(ov, rect)
                else:
                    self._draw_cdpi_icon(dock, rect, icon_color)
            lbl = LANG[self.lang].get(label_key, aid)
            if len(lbl) > 14:
                lbl = lbl[:13] + '…'
            lbl_txt = pf.render(lbl, True, (0, 220, 140))
            lbl_rect = lbl_txt.get_rect(midtop=(DOCK_WIDTH // 2, rect.bottom + 4))
            dock.blit(lbl_txt, lbl_rect)
            buttons.append((aid, rect_global))
        self.screen.blit(dock, (0, 0))
        return buttons
    
    def _open_reset_app(self):
        self._reset_app_open = True
        self._reset_console_lines = []
        self._reset_console_scroll = 0
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
    
    def _close_reset_app(self):
        self._reset_app_open = False
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
    
    def _open_about(self):
        self._about_open = True
    
    def _close_about(self):
        self._about_open = False
    
    def _handle_about_events(self, event):
        pad = 24
        ew, eh = min(420, self.width - 48), min(300, self.height - 48)
        ex, ey = (self.width - ew) // 2, (self.height - eh) // 2
        close_rect = pygame.Rect(ex + ew - pad - 70, ey + pad - 2, 68, 28)
        gh_y = ey + 58 + 26 + 24 + 24 + 28 + 14 + 22
        pf = self.panel_font or self.font
        gh_w = pf.size(ABOUT_GITHUB)[0]
        gh_rect = pygame.Rect(ex + (ew - gh_w) // 2, gh_y, gh_w, 22)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._close_about()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if close_rect.collidepoint(event.pos):
                self._close_about()
                return True
            if gh_rect.collidepoint(event.pos):
                try:
                    webbrowser.open(ABOUT_GITHUB)
                except Exception:
                    pass
                return True
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return True
        return False
    
    def _draw_about(self):
        ld = LANG[self.lang]
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(235)
        overlay.fill((3, 12, 8))
        self.screen.blit(overlay, (0, 0))
        pf = self.panel_font or self.font
        try:
            title_font = pygame.font.SysFont("consolas", 22)
        except Exception:
            title_font = pf
        pad = 24
        ew, eh = min(420, self.width - 48), min(300, self.height - 48)
        ex, ey = (self.width - ew) // 2, (self.height - eh) // 2
        rect = pygame.Rect(ex, ey, ew, eh)
        mx, my = pygame.mouse.get_pos()
        pulse = 0.7 + 0.3 * math.sin(pygame.time.get_ticks() * 0.004)
        glow = (int(0 * pulse), int(180 * pulse), int(80 * pulse))
        pygame.draw.rect(self.screen, (12, 22, 18), rect)
        for i in range(3, 0, -1):
            pygame.draw.rect(self.screen, (int(glow[0]/i), int(glow[1]/i), int(glow[2]/i)), rect.inflate(i*4, i*4), 2)
        pygame.draw.rect(self.screen, (0, 100, 60), rect, 1)
        pygame.draw.rect(self.screen, (0, 200, 120), rect.inflate(-2, -2), 1)
        pygame.draw.line(self.screen, (0, 120, 70), (ex + 12, ey + 42), (ex + ew - 12, ey + 42), 1)
        header = title_font.render(ABOUT_NICK, True, (0, 255, 150))
        self.screen.blit(header, (ex + (ew - header.get_width()) // 2, ey + 12))
        close_rect = pygame.Rect(ex + ew - pad - 70, ey + pad - 2, 68, 28)
        close_col = (30, 70, 45) if close_rect.collidepoint(mx, my) else (18, 45, 28)
        pygame.draw.rect(self.screen, close_col, close_rect)
        pygame.draw.rect(self.screen, (0, 160, 90), close_rect, 1)
        close_txt = pf.render('× ' + ld['close'], True, (0, 220, 140))
        self.screen.blit(close_txt, (close_rect.centerx - close_txt.get_width()//2, close_rect.centery - close_txt.get_height()//2 - 1))
        y = ey + 58
        sect = pf.render(ld['author'], True, (0, 180, 110))
        self.screen.blit(sect, (ex + pad, y))
        y += 26
        self.screen.blit(pf.render(ld['nick'] + ' ' + ABOUT_NICK, True, (0, 255, 160)), (ex + pad, y))
        y += 24
        self.screen.blit(pf.render(ld['fio'] + ' ' + ABOUT_FIO, True, (0, 255, 160)), (ex + pad, y))
        y += 24
        self.screen.blit(pf.render(ld['email'] + ' ' + ABOUT_EMAIL, True, (0, 255, 160)), (ex + pad, y))
        y += 28
        pygame.draw.line(self.screen, (0, 90, 55), (ex + pad, y), (ex + ew - pad, y), 1)
        y += 14
        self.screen.blit(pf.render(ld['github'], True, (0, 180, 110)), (ex + pad, y))
        y += 22
        gh_rect = pygame.Rect(ex + (ew - pf.size(ABOUT_GITHUB)[0]) // 2, y, pf.size(ABOUT_GITHUB)[0], 20)
        gh_col = (0, 255, 180) if gh_rect.collidepoint(mx, my) else (0, 220, 140)
        gh = pf.render(ABOUT_GITHUB, True, gh_col)
        self.screen.blit(gh, (gh_rect.x, gh_rect.y))
        if gh_rect.collidepoint(mx, my):
            pygame.draw.line(self.screen, gh_col, (gh_rect.x, gh_rect.bottom - 2), (gh_rect.right, gh_rect.bottom - 2), 1)
    
    def _run_reset_command(self, cmd, label):
        self._reset_console_lines.append('> ' + label)
        try:
            enc = 'cp866' if sys.platform == 'win32' else 'utf-8'
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding=enc, errors='replace')
            out = (r.stdout or '') + (r.stderr or '')
            for line in out.strip().splitlines():
                self._reset_console_lines.append(line)
            self._reset_console_lines.append('--- Готово ---')
        except Exception as e:
            self._reset_console_lines.append('Ошибка: ' + str(e))
        self._reset_console_scroll = max(0, len(self._reset_console_lines) - 12)
    
    def _handle_reset_app_events(self, event):
        ld = LANG[self.lang]
        pad, line_h = 16, 20
        ew, eh = min(520, self.width - 32), min(420, self.height - 32)
        ex, ey = (self.width - ew) // 2, (self.height - eh) // 2
        btn_h, btn_w, btn_margin = 40, 110, 10
        total_btn_w = 4 * btn_w + 3 * btn_margin
        start_x = ex + (ew - total_btn_w) // 2
        btns = [
            ('full', ld['reset_full']),
            ('winsock', ld['reset_winsock']),
            ('ip', ld['reset_ip']),
            ('dns', ld['reset_dns']),
        ]
        btn_rects = []
        y_btns = ey + pad + 50
        for i, (bid, lbl) in enumerate(btns):
            bx = start_x + (i % 4) * (btn_w + btn_margin)
            by = y_btns + (i // 4) * (btn_h + btn_margin)
            btn_rects.append((bid, pygame.Rect(bx, by, btn_w, btn_h)))
        close_rect = pygame.Rect(ex + ew - pad - 90, ey + pad, 78, 26)
        console_rect = pygame.Rect(ex + pad, y_btns + 56, ew - 2*pad, eh - (y_btns - ey) - 76)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._close_reset_app()
            return True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if close_rect.collidepoint(mx, my):
                self._close_reset_app()
                return True
            for bid, r in btn_rects:
                if r.collidepoint(mx, my):
                    if bid == 'full':
                        self._run_reset_command('ipconfig /flushdns', 'Очистка DNS')
                        self._run_reset_command('netsh winsock reset', 'Сброс Winsock')
                        self._run_reset_command('netsh int ip reset', 'Сброс IP')
                        self._run_reset_command('ipconfig /release', 'Освобождение IP')
                        self._run_reset_command('ipconfig /renew', 'Обновление IP')
                    elif bid == 'winsock':
                        self._run_reset_command('netsh winsock reset', 'Сброс Winsock')
                    elif bid == 'ip':
                        self._run_reset_command('netsh int ip reset', 'Сброс IP')
                        self._run_reset_command('ipconfig /release', 'Освобождение IP')
                        self._run_reset_command('ipconfig /renew', 'Обновление IP')
                    elif bid == 'dns':
                        self._run_reset_command('ipconfig /flushdns', 'Очистка DNS')
                    return True
        if event.type == pygame.MOUSEWHEEL and console_rect.collidepoint(pygame.mouse.get_pos()):
            max_vis = max(1, console_rect.h // line_h)
            max_scroll = max(0, len(self._reset_console_lines) - max_vis)
            self._reset_console_scroll = max(0, min(max_scroll, self._reset_console_scroll - event.y))
            return True
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL):
            return True
        return False
    
    def _draw_reset_app(self):
        ld = LANG[self.lang]
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(230)
        overlay.fill((5, 15, 5))
        self.screen.blit(overlay, (0, 0))
        pf = self.panel_font or self.font
        pad, line_h = 16, 20
        ew, eh = min(520, self.width - 32), min(420, self.height - 32)
        ex, ey = (self.width - ew) // 2, (self.height - eh) // 2
        rect = pygame.Rect(ex, ey, ew, eh)
        pygame.draw.rect(self.screen, (25, 35, 45), rect)
        pygame.draw.rect(self.screen, (0, 150, 200), rect, 2)
        header_y = ey + pad
        self.screen.blit(pf.render(ld['reset_inet'], True, (0, 200, 255)), (ex + pad, header_y))
        close_rect = pygame.Rect(ex + ew - pad - 90, header_y, 78, 26)
        mx, my = pygame.mouse.get_pos()
        close_col = (45, 75, 95) if close_rect.collidepoint(mx, my) else (35, 55, 70)
        pygame.draw.rect(self.screen, close_col, close_rect)
        pygame.draw.rect(self.screen, (0, 140, 180), close_rect, 1)
        close_txt = pf.render('× ' + ld['close'], True, (180, 220, 255))
        self.screen.blit(close_txt, (close_rect.centerx - close_txt.get_width()//2, close_rect.centery - close_txt.get_height()//2 - 1))
        btn_h, btn_w, btn_margin = 40, 110, 10
        total_btn_w = 4 * btn_w + 3 * btn_margin
        start_x = ex + (ew - total_btn_w) // 2
        btns = [ld['reset_full'], ld['reset_winsock'], ld['reset_ip'], ld['reset_dns']]
        y_btns = ey + pad + 50
        for i, lbl in enumerate(btns):
            bx = start_x + (i % 4) * (btn_w + btn_margin)
            by = y_btns + (i // 4) * (btn_h + btn_margin)
            br = pygame.Rect(bx, by, btn_w, btn_h)
            hov = br.collidepoint(mx, my)
            col = (40, 120, 220) if hov else (0, 80, 180)
            pygame.draw.rect(self.screen, col, br)
            pygame.draw.rect(self.screen, (80, 160, 255), br, 1)
            lbl_short = lbl[:14] if len(lbl) > 14 else lbl
            self.screen.blit(pf.render(lbl_short, True, (255, 255, 255)), (br.centerx - pf.size(lbl_short)[0]//2, by + 10))
        console_rect = pygame.Rect(ex + pad, y_btns + 56, ew - 2*pad, eh - (y_btns - ey) - 76)
        pygame.draw.rect(self.screen, (15, 20, 25), console_rect)
        pygame.draw.rect(self.screen, (0, 100, 150), console_rect, 1)
        cw = pf.size('A')[0]
        max_chars = max(10, (console_rect.w - 8) // cw)
        max_vis = max(1, console_rect.h // line_h)
        vis = self._reset_console_lines[self._reset_console_scroll:self._reset_console_scroll + max_vis]
        self.screen.set_clip(console_rect)
        for i, ln in enumerate(vis):
            s = pf.render(ln[:max_chars], True, (200, 220, 255))
            self.screen.blit(s, (console_rect.x + 4, console_rect.y + 4 + i * line_h))
        self.screen.set_clip(None)
    
    def _open_inscription_editor(self):
        """Открыть редактор надписи (pygame overlay, без зависания)"""
        self._edit_mode = True
        pygame.key.start_text_input()
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
        lines = self.text_mask.strip('\n').split('\n')
        self._edit_lines = [l for l in lines if l is not None]
        if not self._edit_lines:
            self._edit_lines = ['']
        self._edit_cursor_row = min(self._edit_cursor_row, len(self._edit_lines) - 1)
        self._edit_cursor_col = min(self._edit_cursor_col, len(self._edit_lines[self._edit_cursor_row]))
        self._edit_scroll = 0
        self._edit_focus = None
        self._edit_num_buffers = {
            'appear': str(min(999999, self.appear_sec))[:6],
            'visible': str(min(999999, self.visible_sec))[:6],
            'disappear': str(min(999999, self.disappear_sec))[:6],
            'pause': str(min(999999, self.pause_sec))[:6],
            'persist': str(min(999999, self.persist_frames))[:6]
        }
        self._edit_av_value = self.always_visible
    
    def _close_inscription_editor(self, apply_changes=False):
        """Закрыть редактор, при apply_changes — применить настройки"""
        if apply_changes:
            self.text_mask = '\n'.join(self._edit_lines) + '\n'
            self.always_visible = self._edit_av_value
            for k, default in [('appear', 2), ('visible', 10), ('disappear', 2), ('pause', 2), ('persist', 200)]:
                try:
                    v = int((self._edit_num_buffers.get(k, str(default)) or '0')[:6])
                except ValueError:
                    v = default
                v = min(999999, max(0, v))
                if k == 'persist':
                    v = max(1, v)
                setattr(self, {'appear': 'appear_sec', 'visible': 'visible_sec', 'disappear': 'disappear_sec', 'pause': 'pause_sec', 'persist': 'persist_frames'}[k], v)
            self._build_niko_mask()
            self.frame = 0
        self._edit_mode = False
        pygame.key.stop_text_input()
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
    
    def _handle_edit_events(self, event):
        """Обработка событий в режиме редактора надписи"""
        ld = LANG[self.lang]
        pad, line_h = 16, 22
        fh = (self.panel_font or self.font).get_height()
        ew = min(500, self.width - 32)
        eh = min(16 + 26 + 8*22 + 12 + 32 + 42 + fh + 2 + 24 + 20 + 20 + 36 + 16, self.height - 32)
        ex, ey = (self.width - ew) // 2, (self.height - eh) // 2
        txt_h = 8 * line_h
        y1 = ey + pad + line_h + 4 + txt_h + 12
        cb_rect = pygame.Rect(ex + pad, y1, 20, 20)
        y2 = y1 + 32
        num_rects = {}
        for i in range(5):
            key = ['appear', 'visible', 'disappear', 'pause', 'persist'][i]
            fx = ex + pad + (i % 3) * (ew // 3)
            fy_label = y2 + (i // 3) * 42
            fy_inp = fy_label + fh + 2
            num_rects[key] = pygame.Rect(fx, fy_inp, 58, 24)
        y_btn = ey + eh - pad - 36
        ok_rect = pygame.Rect(ex + pad, y_btn, 80, 36)
        cancel_rect = pygame.Rect(ex + pad + 90, y_btn, 100, 36)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if ok_rect.collidepoint(mx, my):
                self._close_inscription_editor(apply_changes=True)
                return True
            if cancel_rect.collidepoint(mx, my):
                self._close_inscription_editor(apply_changes=False)
                return True
            txt_rect = pygame.Rect(ex + pad, ey + pad + line_h + 4, ew - 2 * pad, txt_h)
            if txt_rect.collidepoint(mx, my):
                click_row = min((my - txt_rect.y - 4) // line_h + self._edit_scroll, len(self._edit_lines) - 1)
                click_row = max(0, click_row)
                line = self._edit_lines[click_row]
                cw = (self.panel_font or self.font).size('A')[0]
                click_col = min(max(0, (mx - txt_rect.x - 4) // cw), len(line))
                click_col = max(0, click_col)
                self._edit_cursor_row = click_row
                self._edit_cursor_col = click_col
                self._edit_focus = None
                return True
            if cb_rect.collidepoint(mx, my):
                self._edit_av_value = not self._edit_av_value
                return True
            for key, r in num_rects.items():
                if r.collidepoint(mx, my):
                    self._edit_focus = key
                    return True
            self._edit_focus = None
            return True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mx, my = event.pos
            if ok_rect.collidepoint(mx, my):
                self._close_inscription_editor(apply_changes=True)
                return True
            if cancel_rect.collidepoint(mx, my):
                self._close_inscription_editor(apply_changes=False)
                return True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._close_inscription_editor(apply_changes=False)
                return True
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if self._edit_focus is None:
                    line = self._edit_lines[self._edit_cursor_row]
                    self._edit_lines[self._edit_cursor_row] = line[:self._edit_cursor_col]
                    self._edit_lines.insert(self._edit_cursor_row + 1, line[self._edit_cursor_col:])
                    self._edit_cursor_row += 1
                    self._edit_cursor_col = 0
                return True
            if event.key == pygame.K_BACKSPACE:
                if self._edit_focus:
                    s = self._edit_num_buffers[self._edit_focus]
                    self._edit_num_buffers[self._edit_focus] = s[:-1]
                elif self._edit_cursor_col > 0:
                    line = self._edit_lines[self._edit_cursor_row]
                    self._edit_lines[self._edit_cursor_row] = line[:self._edit_cursor_col-1] + line[self._edit_cursor_col:]
                    self._edit_cursor_col -= 1
                elif self._edit_cursor_row > 0:
                    prev_len = len(self._edit_lines[self._edit_cursor_row - 1])
                    self._edit_lines[self._edit_cursor_row - 1] += self._edit_lines[self._edit_cursor_row]
                    del self._edit_lines[self._edit_cursor_row]
                    self._edit_cursor_row -= 1
                    self._edit_cursor_col = prev_len
                return True
            if event.key == pygame.K_DELETE and self._edit_focus is None:
                line = self._edit_lines[self._edit_cursor_row]
                if self._edit_cursor_col < len(line):
                    self._edit_lines[self._edit_cursor_row] = line[:self._edit_cursor_col] + line[self._edit_cursor_col+1:]
                elif self._edit_cursor_row < len(self._edit_lines) - 1:
                    self._edit_lines[self._edit_cursor_row] += self._edit_lines.pop(self._edit_cursor_row + 1)
                return True
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT) and self._edit_focus is None:
                if event.key == pygame.K_UP and self._edit_cursor_row > 0:
                    self._edit_cursor_row -= 1
                    self._edit_cursor_col = min(self._edit_cursor_col, len(self._edit_lines[self._edit_cursor_row]))
                elif event.key == pygame.K_DOWN and self._edit_cursor_row < len(self._edit_lines) - 1:
                    self._edit_cursor_row += 1
                    self._edit_cursor_col = min(self._edit_cursor_col, len(self._edit_lines[self._edit_cursor_row]))
                elif event.key == pygame.K_LEFT and self._edit_cursor_col > 0:
                    self._edit_cursor_col -= 1
                elif event.key == pygame.K_RIGHT:
                    self._edit_cursor_col = min(self._edit_cursor_col + 1, len(self._edit_lines[self._edit_cursor_row]))
                return True
            if event.key == pygame.K_TAB:
                focus_order = ['appear', 'visible', 'disappear', 'pause', 'persist', None]
                idx = (focus_order.index(self._edit_focus) if self._edit_focus in focus_order else -1) + 1
                self._edit_focus = focus_order[idx % len(focus_order)]
                return True
            if self._edit_focus:
                digit = None
                if event.unicode and event.unicode.isdigit():
                    digit = event.unicode
                else:
                    kd = {pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3', pygame.K_4: '4',
                          pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8', pygame.K_9: '9',
                          pygame.K_KP0: '0', pygame.K_KP1: '1', pygame.K_KP2: '2', pygame.K_KP3: '3',
                          pygame.K_KP4: '4', pygame.K_KP5: '5', pygame.K_KP6: '6', pygame.K_KP7: '7',
                          pygame.K_KP8: '8', pygame.K_KP9: '9'}
                    digit = kd.get(event.key)
                if digit and len(self._edit_num_buffers[self._edit_focus]) < 6:
                    self._edit_num_buffers[self._edit_focus] += digit
                    return True
        if event.type == pygame.TEXTINPUT:
            if self._edit_focus:
                return True
            mods = pygame.key.get_mods()
            if mods & (pygame.KMOD_CTRL | pygame.KMOD_ALT):
                return True
            ch = event.text
            line = self._edit_lines[self._edit_cursor_row]
            self._edit_lines[self._edit_cursor_row] = line[:self._edit_cursor_col] + ch + line[self._edit_cursor_col:]
            self._edit_cursor_col += 1
            return True
        if event.type in (pygame.KEYDOWN, pygame.TEXTINPUT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return True
        return False
    
    def _draw_inscription_editor(self):
        """Отрисовка редактора надписи поверх матрицы"""
        ld = LANG[self.lang]
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(230)
        overlay.fill((5, 15, 5))
        self.screen.blit(overlay, (0, 0))
        pf = self.panel_font or self.font
        line_h = 22
        pad = 16
        ew = min(500, self.width - 2 * pad)
        fh = pf.get_height()
        eh = min(pad + 26 + 8*line_h + 12 + 32 + 42 + fh + 2 + 24 + 20 + 20 + 36 + pad, self.height - 2 * pad)
        ex = (self.width - ew) // 2
        ey = (self.height - eh) // 2
        rect = pygame.Rect(ex, ey, ew, eh)
        pygame.draw.rect(self.screen, (20, 40, 20), rect)
        pygame.draw.rect(self.screen, (0, 180, 0), rect, 2)
        y = ey + pad
        pf.render(ld['inscription'] + ' — ' + ld['mask_hint'], True, (0, 255, 0))
        self.screen.blit(pf.render(ld['inscription'] + ' — ' + ld['mask_hint'], True, (0, 255, 0)), (ex + pad, y))
        y += line_h + 4
        txt_h = 8 * line_h
        txt_rect = pygame.Rect(ex + pad, y, ew - 2 * pad, txt_h)
        pygame.draw.rect(self.screen, (10, 25, 10), txt_rect)
        pygame.draw.rect(self.screen, (0, 120, 0), txt_rect, 1)
        vis_lines = min(8, len(self._edit_lines))
        for i in range(vis_lines):
            idx = min(self._edit_scroll + i, len(self._edit_lines) - 1)
            line = self._edit_lines[idx]
            color = (0, 255, 0) if idx == self._edit_cursor_row else (0, 200, 0)
            surf = pf.render(line[:60] + ('…' if len(line) > 60 else ''), True, color)
            self.screen.blit(surf, (ex + pad + 4, y + 4 + i * line_h))
            if idx == self._edit_cursor_row:
                cx = ex + pad + 4 + pf.size(line[:self._edit_cursor_col])[0]
                cy = y + 4 + i * line_h
                pygame.draw.line(self.screen, (0, 255, 0), (cx, cy), (cx, cy + line_h - 2), 2)
        y += txt_h + 12
        cb_rect = pygame.Rect(ex + pad, y, 20, 20)
        pygame.draw.rect(self.screen, (0, 150, 0), cb_rect, 1)
        if self._edit_av_value:
            pygame.draw.rect(self.screen, (0, 255, 0), cb_rect.inflate(-6, -6))
        self.screen.blit(pf.render(ld['always_visible'], True, (0, 255, 0)), (ex + pad + 28, y - 2))
        y += 32
        num_labels = [(ld['appear_sec'], 'appear', 60), (ld['visible_sec'], 'visible', 120), (ld['disappear_sec'], 'disappear', 60), (ld['pause_sec'], 'pause', 60), (ld['persist_frames'], 'persist', 1000)]
        mx, my = pygame.mouse.get_pos()
        inp_rects_for_cursor = []
        for i, (label, key, _) in enumerate(num_labels):
            lw = label.find('(') if '(' in label else len(label)
            lbl = label[:lw].strip()
            fx = ex + pad + (i % 3) * (ew // 3)
            fy_label = y + (i // 3) * 42
            fy_inp = fy_label + fh + 2
            self.screen.blit(pf.render(lbl, True, (0, 200, 0)), (fx, fy_label))
            inp_rect = pygame.Rect(fx, fy_inp, 58, 24)
            inp_rects_for_cursor.append(inp_rect)
            is_focus = self._edit_focus == key
            pygame.draw.rect(self.screen, (0, 100, 0) if is_focus else (10, 30, 10), inp_rect)
            pygame.draw.rect(self.screen, (0, 200, 0) if is_focus else (0, 120, 0), inp_rect, 1)
            val = (self._edit_num_buffers.get(key, ''))[:6]
            txt_surf = pf.render(val, True, (0, 255, 0))
            ty = fy_inp + (24 - txt_surf.get_height()) // 2
            self.screen.blit(txt_surf, (fx + 4, ty))
            if is_focus and (pygame.time.get_ticks() // 400) % 2 == 0:
                cw = txt_surf.get_width()
                pygame.draw.line(self.screen, (0, 255, 0), (fx + 4 + cw + 1, ty), (fx + 4 + cw + 1, ty + txt_surf.get_height()), 2)
            if i == 4:
                y = fy_inp + 20
        y_btn = ey + eh - pad - 36
        ok_rect = pygame.Rect(ex + pad, y_btn, 80, 36)
        cancel_rect = pygame.Rect(ex + pad + 90, y_btn, 100, 36)
        mx, my = pygame.mouse.get_pos()
        for r, txt in [(ok_rect, ld['ok']), (cancel_rect, ld['cancel'])]:
            hov = r.collidepoint(mx, my)
            pygame.draw.rect(self.screen, (0, 80, 0) if hov else (20, 50, 20), r)
            pygame.draw.rect(self.screen, (0, 200, 0), r, 1)
            self.screen.blit(pf.render(txt, True, (0, 255, 0)), (r.x + (r.w - pf.size(txt)[0]) // 2, r.y + 8))
        try:
            show_ibeam = txt_rect.collidepoint(mx, my) or any(r.collidepoint(mx, my) for r in inp_rects_for_cursor)
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM if show_ibeam else pygame.SYSTEM_CURSOR_ARROW)
        except Exception:
            pass
        
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    continue
                if self._reset_app_open:
                    if self._handle_reset_app_events(event):
                        continue
                elif self._about_open:
                    if self._handle_about_events(event):
                        continue
                elif self._edit_mode:
                    if self._handle_edit_events(event):
                        continue
                if event.type == pygame.KEYDOWN:
                    mod = event.mod & (pygame.KMOD_ALT | pygame.KMOD_CTRL)
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if mod and event.key == pygame.K_RETURN:
                        self._fullscreen = not self._fullscreen
                        self._init_display()
                    if mod and event.key == pygame.K_t:
                        self.show_text = not self.show_text
                    if mod and event.key == pygame.K_o:
                        self._init_display(preserve_size=True)
                    if mod and event.key == pygame.K_n:
                        self._open_inscription_editor()
                    if mod and event.key == pygame.K_a:
                        self._open_about()
                    if event.key == pygame.K_l and not mod:
                        self.lang = 'en' if self.lang == 'ru' else 'ru'
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for aid, rect in self._dock_buttons:
                        if rect.collidepoint(event.pos):
                            if aid == 'reset_inet':
                                self._open_reset_app()
                            elif aid == 'cdpi':
                                try:
                                    webbrowser.open(CDPI_GITHUB)
                                except Exception:
                                    pass
                            elif aid == 'vpn':
                                try:
                                    webbrowser.open(VPN_URL)
                                except Exception:
                                    pass
                            elif aid == 'dns':
                                try:
                                    webbrowser.open(DNS_URL)
                                except Exception:
                                    pass
                            break
                    else:
                        for action, rect in self._panel_buttons:
                            if rect.collidepoint(event.pos):
                                if action == 'exit':
                                    running = False
                                elif action == 'text':
                                    self.show_text = not self.show_text
                                elif action == 'inscription':
                                    self._open_inscription_editor()
                                elif action == 'fullscreen':
                                    self._fullscreen = not self._fullscreen
                                    self._init_display()
                                elif action == 'refresh':
                                    self._refresh_pressed = True
                                    self._init_display(preserve_size=True)
                                elif action == 'about':
                                    self._open_about()
                                elif action == 'lang':
                                    self.lang = 'en' if self.lang == 'ru' else 'ru'
                                break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self._refresh_pressed = False  # отпустили ЛКМ — зелёный
                if event.type == pygame.VIDEORESIZE and not self._fullscreen:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.RESIZABLE)
                    self._on_resize()
                        
            self.screen.blit(self.fade_surface, (0, 0))
            
            self.frame += 1
            if not self.show_text:
                visible = 0
            elif self.always_visible:
                visible = 1.0
            else:
                cycle_len = (self.appear_sec + self.visible_sec + self.disappear_sec + self.pause_sec) * FPS
                cycle = self.frame % cycle_len
                sec = cycle / FPS
                if sec < self.appear_sec:
                    visible = sec / self.appear_sec if self.appear_sec > 0 else 1
                elif sec < self.appear_sec + self.visible_sec:
                    visible = 1.0
                elif sec < self.appear_sec + self.visible_sec + self.disappear_sec:
                    visible = 1 - (sec - self.appear_sec - self.visible_sec) / self.disappear_sec if self.disappear_sec > 0 else 0
                else:
                    visible = 0
            
            niko_hits = []
            for i in range(self.columns):
                char = random.choice(CHARS)
                x = i * self.font_size
                y = self.drops[i] * self.font_size
                
                self.screen.blit(self.font.render(char, True, BRIGHT_GREEN), (x, y))
                if (x, y) in self.niko_cells_set:
                    niko_hits.append((x, y, char, BRIGHT_GREEN))
                
                if self.drops[i] > 1:
                    trail_char = random.choice(CHARS)
                    trail_color = (0, 180, 80)
                    ty = (self.drops[i] - 1) * self.font_size
                    self.screen.blit(self.font.render(trail_char, True, trail_color), (x, ty))
                    if (x, ty) in self.niko_cells_set:
                        niko_hits.append((x, ty, trail_char, trail_color))
                
                if y > self.height and random.random() > 0.975:
                    self.drops[i] = 0
                self.drops[i] += 1
            
            if visible > 0:
                self.draw_niko(niko_hits, visible)
            
            self._panel_buttons = self._draw_panel() or []
            self._dock_buttons = self._draw_dock() or []
            if self._reset_app_open:
                self._draw_reset_app()
            elif self._about_open:
                self._draw_about()
            elif self._edit_mode:
                self._draw_inscription_editor()
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = MatrixRainNiko()
    app.run()
