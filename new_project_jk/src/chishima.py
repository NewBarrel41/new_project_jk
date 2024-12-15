import pygame
import random
import sys
from copy import copy
from types import SimpleNamespace as sns

from utils.logger import get_logger
from config.settings import BG, GRID_SIZE, CELL_SIZE, MARGIN, BGM, IMAGE

class CellState:
    def __init__(self):
        self.is_mine = False      # 地雷があるかどうか
        self.is_revealed = False  # マスが開かれているかどうか
        self.neighbor_mines = 0   # 周囲の地雷数
        self.is_wall = False      # プレイ不可能な壁エリアかどうか


class MainGameLogic:
    def __init__(self):
        # 基本設定
        self.grid_size = GRID_SIZE
        self.cell_size = CELL_SIZE

        # 画面サイズは背景画像のサイズに合わせる
        self.bg_width = BG.WIDTH
        self.bg_height = BG.HEIGHT

        # マップ設定
        self.map = sns(

            playable_width=60,    # 画面サイズから左右端のマージンを引いた操作可能エリア
        )

        # プレイ可能エリアのグリッドサイズを計算
        self.playable_width = (self.bg_width - self.playable_margin.left - self.playable_margin['right']) // self.cell_size
        self.playable_height = (self.bg_height - self.playable_margin['top'] - self.playable_margin['bottom']) // self.cell_size

        # グリッドの初期化
        self.grid = [[CellState() for _ in range(self.playable_width)] 
                    for _ in range(self.playable_height)]

        # 画像の読み込み
        self.load_images()

        # 初期設定
        self.initialize_grid()

    def load_images(self):
        assets_dir = Path("assets")
        self.images = {
            'background': pygame.image.load(assets_dir / "background.png"),
            'numbers': [],
            'mine': pygame.image.load(assets_dir / "mine.png"),
            'unopened': pygame.image.load(assets_dir / "unopened.png"),
        }

        # 数字の画像を読み込み (1-8)
        for i in range(1, 9):
            self.images['numbers'].append(
                pygame.transform.scale(
                    pygame.image.load(assets_dir / f"number{i}.png"),
                    (self.cell_size, self.cell_size)
                )
            )

        # その他の画像もリサイズ
        self.images['mine'] = pygame.transform.scale(
            self.images['mine'], 
            (self.cell_size, self.cell_size)
        )
        self.images['unopened'] = pygame.transform.scale(
            self.images['unopened'], 
            (self.cell_size, self.cell_size)
        )

        # 背景画像は画面サイズに合わせる
        self.images['background'] = pygame.transform.scale(
            self.images['background'],
            (self.bg_width, self.bg_height)
        )

    def initialize_grid(self):
        # 地雷を配置（プレイ可能エリア内にランダムに配置）
        mine_count = (self.playable_width * self.playable_height) // 6  # 全マスの1/6程度を地雷に
        self.place_mines(mine_count)

        # 周辺の地雷数を計算
        self.calculate_neighbor_mines()

    def place_mines(self, mine_count):
        placed_mines = 0
        while placed_mines < mine_count:
            x = random.randint(0, self.playable_width - 1)
            y = random.randint(0, self.playable_height - 1)

            if not self.grid[y][x].is_mine:
                self.grid[y][x].is_mine = True
                placed_mines += 1

    def calculate_neighbor_mines(self):
        for y in range(self.playable_height):
            for x in range(self.playable_width):
                if not self.grid[y][x].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            new_y, new_x = y + dy, x + dx
                            if (0 <= new_x < self.playable_width and 
                                0 <= new_y < self.playable_height and 
                                self.grid[new_y][new_x].is_mine):
                                count += 1
                    self.grid[y][x].neighbor_mines = count

    def screen_to_grid(self, screen_x, screen_y):
        # スクリーン座標をグリッド座標に変換
        grid_x = (screen_x - self.playable_margin['left']) // self.cell_size
        grid_y = (screen_y - self.playable_margin['top']) // self.cell_size

        if (0 <= grid_x < self.playable_width and 
            0 <= grid_y < self.playable_height):
            return grid_x, grid_y
        return None, None

    def reveal_square(self, x, y):
        if not (0 <= x < self.playable_width and 0 <= y < self.playable_height):
            return True

        cell = self.grid[y][x]
        if cell.is_revealed:
            return True

        cell.is_revealed = True

        if cell.is_mine:
            return False  # ゲームオーバー

        # 周囲に地雷がない場合は周囲のマスも開く
        if cell.neighbor_mines == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    if not self.reveal_square(x + dx, y + dy):
                        return False
        return True

    def draw_grid(self, screen):
        # 背景描画
        screen.blit(self.images['background'], (0, 0))

        # グリッド描画
        for y in range(self.playable_height):
            for x in range(self.playable_width):
                cell = self.grid[y][x]
                screen_x = x * self.cell_size + self.playable_margin['left']
                screen_y = y * self.cell_size + self.playable_margin['top']

                if not cell.is_revealed:
                    screen.blit(self.images['unopened'], (screen_x, screen_y))
                elif cell.is_mine:
                    screen.blit(self.images['mine'], (screen_x, screen_y))
                else:
                    # 数字マスの描画
                    if cell.neighbor_mines > 0:
                        screen.blit(self.images['numbers'][cell.neighbor_mines - 1], 
                                  (screen_x, screen_y))

    def select_screen(self):
        screen = pygame.display.set_mode((self.bg_width, self.bg_height))
        pygame.display.set_caption('Minesweeper Game')
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリック
                        mouse_x, mouse_y = event.pos
                        grid_x, grid_y = self.screen_to_grid(mouse_x, mouse_y)
                        if grid_x is not None and grid_y is not None:
                            if not self.reveal_square(grid_x, grid_y):
                                print("Game Over!")
                                running = False

            self.draw_grid(screen)
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        return False


if __name__ == "__main__":
    game_main = MainGameLogic()
    game_main.select_screen()
