# アプリケーション設定(更新するときはpyproject.tomlも一緒に更新する)
PROJECT_NAME = 'new_project_jk'
APP_NAME = 'new_project_jk'
VERSION = '0.0.2'
DEBUG = True
ENCODING = 'utf-8'


# ゲーム設定
class BG:
    FPS = 60
    WIDTH = 800        # ゲーム画面の横幅
    HEIGHT = 600       # ゲーム画面の縦幅
    COLOR = (0, 0, 0)  # ゲーム画面の背景色


class MAP:
    TEXT_COLOR = (255, 255, 255)
    GRID_SIZE = 15  # マップ中の地雷配置グリッドのサイズ
    CELL_SIZE = 40  # セルの大きさ (ピクセル)


class MARGIN:
    TOP = 80     # マップ上端からのマージン
    BOTTOM = 80  # マップ下端からのマージン
    LEFT = 60    # マップ左端からのマージン
    RIGHT = 60    # マップ右端からのマージン


class SOUND:
    TITLE = 'media/sound/001.mp3'
    OPPOSITION = ''
    AURORA = ''
    ASTEROID = ''
    NOVA = ''
    SUPERNOVA = ''


class IMAGE:
    BACKGROUND = 'media/image/background.png'
    COVERED = 'media/image/covered.png'
    MINE = 'media/image/mine.png'
    PERA = 'media/image/pera.png'
    ITEM = 'media/image/item.png'
    CALM = 'media/image/0.png'
    MIST = 'media/image/1.png'
    THUNDER = 'media/image/2.png'
    MIRAGE = 'media/image/3.png'
    TORNADO = 'media/image/4.png'
    EARTHQUAKE = 'media/image/5.png'
    TSUNAMI = 'media/image/6.png'
    ERUPTION = 'media/image/7.png'
