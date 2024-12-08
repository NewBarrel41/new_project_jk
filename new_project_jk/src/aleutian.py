import pygame
import random
import sys
from copy import copy
from types import SimpleNamespace as sns

from utils.logger import get_logger
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, FPS

logger = get_logger(__name__)


class CellState:
    def __init__(self, index):
        self.index = index  # マスの採番
        self.num = 0  # マスの周りの地雷数、-1は地雷
        self.state = False  # マスの開閉


class MainGameLogic:
    def __init__(self):
        # self.map = {'stage': 1, 'area': 1, 'grid_size': 15}
        self.stage = 1
        self.area = 1
        self.grid_size = 15
        # self.grid = [[[(i*self.grid_size)+j, CellState()] for j in range(self.grid_size)] for i in range(self.grid_size)]
        self.grid = [CellState(index=i) * self.grid_size for i in range(self.grid_size)]
        self.path_route = self.create_safe_path_logic_1(stage=self.stage, area=self.area, size=self.grid_size)
        self.set_mine()  # 地雷生成

    def set_mine(self, max=10):
        # 地雷をランダムに配置
        grid_total = self.grid_size**2
        masu_list = list(range(grid_total))
        for _ in range(max):
            # 選択したインデックスの要素を取り出し、同時にリストから削除
            chosen_number = masu_list.pop(random.randrange(grid_total))
            row = chosen_number // self.grid_size
            col = chosen_number % self.grid_size
            self.grid[row][col][1] = -1  # 地雷を配置
            grid_total -= 1

            # 周囲の数字を更新 -> dは変化量(delta)
            for dy in list(range(-1, 2)):
                for dx in list(range(-1, 2)):
                    if dy == 0 and dx == 0:  # 地雷マス自体はスキップ
                        continue
                    row_dy = row + dy
                    col_dx = col + dx
                    # グリッド内かつ地雷でないマスの場合
                    if (0 <= row_dy < self.grid_size and
                            0 <= col_dx < self.grid_size and self.grid[row_dy][col_dx][1] != -1):
                        self.grid[row_dy][col_dx][1] += 1

    def create_safe_path_logic_1(self, stage, area, grid_size):
        # スタートからのルートとゴールからのルートが繋がるまで安全地帯ルートを生成する
        goal_axis = grid_size - 1 if grid_size % 2 == 1 else grid_size
        axis_x = goal_axis // 2  # グリッドの中間
        current_position = sns(y=0, x=random.randrange(axis_x-2, axis_x+3))
        safe_path = [copy(current_position)]  # copy()は浅いコピー、今回はこれで十分
        current_position_from_goal = sns(y=goal_axis, x=random.randrange(axis_x-1, axis_x+2))
        safe_path_from_goal = [copy(current_position_from_goal)]
        arrival_route = False

        # スタートから最終行までルート探索
        while current_position.y == goal_axis:
            # 前に進むか横に進むかをランダムに決定、Trueが前方、Falseが横
            if random.randrange(2) and current_position.y < goal_axis:
                current_position.y += 1  # 前方移動
                # さらに横移動で斜めに移動
                if current_position.x == 0 and random.randrange(2):
                    current_position.x += 1
                elif current_position.x == goal_axis and random.randrange(2):
                    current_position.x -= 1
                elif random.randrange(2):
                    current_position.x += random.choice([-1, 1])

            elif current_position.x == 0:
                current_position.x += 1
            elif current_position.x == goal_axis:
                current_position.x -= 1
            else:
                current_position.x += random.choice([-1, 1])

            # 元の位置に戻ってきた場合はスルーして重複排除
            if current_position not in safe_path:
                safe_path.append(copy(current_position))

            # 最終行で左右にゴールマスが存在する場合
            if current_position.y == goal_axis:
                for dx in list(range(-1, 2)):
                    if current_position.x + dx == current_position_from_goal.x:
                        arrival_route = True

        # ゴールから、スタートからのルートにぶつかるまでのルート探索
        if not arrival_route:
            while current_position_from_goal.y == current_position.y:
                # 前に進むか横に進むかをランダムに決定、Trueが前方、Falseが横
                if random.randrange(2):
                    current_position.y -= 1  # 前方移動
                    # さらに横移動で斜めに移動
                    if current_position.x == 0 and random.randrange(2):
                        current_position.x += 1
                    elif current_position.x == goal_axis and random.randrange(2):
                        current_position.x -= 1
                    elif random.randrange(2):
                        current_position.x += random.choice([-1, 1])

                elif current_position.x == 0:
                    current_position.x += 1
                elif current_position.x == goal_axis:
                    current_position.x -= 1
                else:
                    current_position.x += random.choice([-1, 1])

                safe_path_from_goal.append(copy(current_position_from_goal))

            # スタート行まで到達した場合
            if current_position_from_goal.y == 0:
                # 横串を差し込む
                pass

        # お店から安全地帯へのルート検索
        pass

    def select_screen(self):
        logger.info("Transitioning to game screen")

        # ゲーム画面を描画するループ
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Minesweeper Game')

        clock = pygame.time.Clock()
        running = True

        while running:
            screen.fill(BG_COLOR)
            self.draw_grid(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左クリックの場合
                        mouse_x, mouse_y = event.pos
                        grid_x = mouse_x // (SCREEN_WIDTH // self.grid_size)
                        grid_y = mouse_y // (SCREEN_HEIGHT // self.grid_size)
                        self.reveal_square(grid_x, grid_y)

            pygame.display.flip()
            clock.tick(FPS)

        return False

    def draw_grid(self, screen):
        cell_width = SCREEN_WIDTH // self.grid_size
        cell_height = SCREEN_HEIGHT // self.grid_size

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                if self.revealed[y][x]:
                    if self.grid[y][x] == -1:
                        pygame.draw.rect(screen, (255, 0, 0), rect)  # 地雷は赤色で表示
                    else:
                        pygame.draw.rect(screen, (200, 200, 200), rect)  # 開いたマスは灰色で表示
                        font = pygame.font.Font(None, 36)
                        text_surface = font.render(str(self.grid[y][x]), True, (0, 0, 0))
                        screen.blit(text_surface, rect.topleft)
                else:
                    pygame.draw.rect(screen, (100, 100, 100), rect)  # 未開封のマスは暗灰色

    def reveal_square(self, x, y):
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size) or self.revealed[y][x]:
            return

        self.revealed[y][x] = True

        if self.grid[y][x] == -1:
            logger.info("Game Over! Hit a mine.")
            # ゲームオーバー処理（ここでは簡単に終了）
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    MainGameLogic()
