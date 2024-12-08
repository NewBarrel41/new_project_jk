import pygame
import sys

from src.aleutian import MainGameLogic
from utils.logger import get_logger
from config.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, TEXT_COLOR, FPS
from config.settings import BGM


logger = get_logger(__name__)


def main():
    """
    ゲームのメイン関数。初期化、メインループ、終了処理を行う。
    """
    logger.info("Game Start")

    try:
        # Pygameの初期化
        pygame.init()

        # ゲーム画面の設定
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Game Title Screen')

        # BGMの読み込みと再生（無限ループ再生）
        # pygame.mixer.music.load(BGM.TITLE)
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

        # フォントとテキストの設定
        font = pygame.font.Font(None, 74)
        text = font.render('Press Any Key to Start', True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        # FPS制御用のクロックオブジェクト
        clock = pygame.time.Clock()

        # ゲームメインオブジェクトの作成
        game_main = MainGameLogic()

        # メインゲームループ
        running = True
        while running:
            # 背景色の塗りつぶし
            screen.fill(BG_COLOR)

            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    # キー入力があれば画面遷移
                    running = game_main.select_screen()

            # テキストの描画
            screen.blit(text, text_rect)

            # 画面の更新
            pygame.display.flip()

            # FPSの制御
            clock.tick(FPS)

    except Exception as e:
        # エラーログの出力
        logger.error(f"An error occurred: {e}")
    finally:
        # Pygameの終了処理
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
