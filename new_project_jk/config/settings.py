# ログ設定
LOG_FILE = 'logs/app.log'
LOG_TEST_FILE = 'logs/app_test.log'
LOG_FORMAT = '[%(asctime)s.%(msecs)03d][%(levelname)s][%(pathname)s] %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# デバッグ設定
DEBUG = True

# アプリケーション設定(更新するときはpyproject.tomlも一緒に更新する)
APP_NAME = 'new_project_jk'
VERSION = '0.0.1'

# 汎用設定
ENCODING = 'utf-8'
