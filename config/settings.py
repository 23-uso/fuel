import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# .envファイルを読み込む設定（開発環境用）
load_dotenv()

# プロジェクトのルートディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# --- セキュリティ設定 ---
# 直接書かず、環境変数（.env または Renderの設定）から取得する
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-fallback-key')

# 環境変数の DEBUG が 'True' の時だけ True になる
DEBUG = os.environ.get('DEBUG') == 'True'

# 全てのホストを許可（RenderのURLで動かすために必要）
ALLOWED_HOSTS = ['*']


# --- アプリケーション定義 ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fuel',           # 燃費計算アプリ
    'rest_framework', # API用
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # 静的ファイル用（本番で必要）
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# --- データベース設定 ---
# 開発環境では SQLite、本番環境（Render）では外部DB（PostgreSQLなど）を使う設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Renderなどの環境変数 DATABASE_URL がある場合はそちらを優先する
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


# --- パスワードバリデーション ---
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# --- 国際化設定 ---
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# --- 静的ファイル設定 (CSS, JavaScript, Images) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles' # 本番環境で画像などを集める場所

# 本番環境で静的ファイルを効率よく配信するための設定
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# デフォルトのプライマリキーの型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'