"""
Default configuration file
Reads environment variables and defaults to a value suitable for dev/test environment if not set
"""

from os.path import abspath, dirname, realpath
from os import environ
# from typing import Dict, Any

_basedir = abspath(dirname(__file__))

# General
THREADS_PER_PAGE = environ.get("THREADS_PER_PAGE", 8)
CORS = environ.get("CORS", True)
DEBUG = environ.get("DEBUG", True)
LEMUR_HOSTNAME = environ.get("LEMUR_HOSTNAME", "localhost")

# Logging
LOG_LEVEL = environ.get("LOG_LEVEL", "DEBUG")
LOG_FILE = environ.get("LOG_FILE", "lemur.log")
LOG_UPGRADE_FILE = environ.get("LOG_UPGRADE_FILE", "db_upgrade.log")
LOG_REQUEST_HEADERS = environ.get("LOG_REQUEST_HEADERS", "False")
LOG_SANITIZE_REQUEST_HEADERS = environ.get("LOG_SANITIZE_REQUEST_HEADERS", "True")
LOG_REQUEST_HEADERS_SKIP_ENDPOINT = ["/metrics", "/healthcheck"]  # These endpoints are noisy so skip them by default

# This is the secret key used by flask session management
SECRET_KEY = "e89dc56e5fa4214f52bfe4d8c84256209c559022da562fd5b1d1a70798923518"

# You should consider storing these separately from your config
LEMUR_TOKEN_SECRET = "EO5vLI6sBXBLKDJr_2AYYq"
LEMUR_TOKEN_SECRETS = [LEMUR_TOKEN_SECRET]
LEMUR_ENCRYPTION_KEYS = ['Q7AzDsZHJRaKdS4Obeb4bLw6tYRdTqQD24xHQqJbA4A=']

# REQUIRED
# Certificate Defaults
LEMUR_DEFAULT_COUNTRY = ""
LEMUR_DEFAULT_STATE = ""
LEMUR_DEFAULT_LOCATION = ""
LEMUR_DEFAULT_ORGANIZATION = ""
LEMUR_DEFAULT_ORGANIZATIONAL_UNIT = ""
LEMUR_SECURITY_TEAM_EMAIL = ["admin@localhost"]

# Database settings
SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI', 'postgresql://lemur:lemur@localhost:5432/lemur')
# SQLALCHEMY_ENABLE_FLASK_REPLICATED = False
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
# SQLALCHEMY_ENGINE_OPTIONS = {
#     'pool_recycle': 499,
#     'pool_timeout': 20,
# }

# LEMUR_DEFAULT_ISSUER_PLUGIN=cryptography-issuer
# LEMUR_DEFAULT_AUTHORITY=cryptography

# List of domain regular expressions that non-admin users can issue
LEMUR_ALLOWED_DOMAINS = []

# Authentication Providers
ACTIVE_PROVIDERS = []

# Metrics Providers
METRIC_PROVIDERS = []

# AWS

# LEMUR_INSTANCE_PROFILE = "Lemur"

# Issuers

# These will be dependent on which 3rd party that Lemur is
# configured to use.

# VERISIGN_URL = ""
# VERISIGN_PEM_PATH = ""
# VERISIGN_FIRST_NAME = ""
# VERISIGN_LAST_NAME = ""
# VERSIGN_EMAIL = ""

IDP_GROUPS_KEYS = ["googleGroups"]  # a list of keys used by IDP(s) to return user groups (profile[IDP_GROUPS_KEY])
# Note that prefix/suffix can be commented out or set to "" if no filtering against naming convention is desired
# IDP_ROLES_PREFIX = "PREFIX-"  # prefix for all IDP-defined roles, used to match naming conventions
# IDP_ROLES_SUFFIX = "_SUFFIX"  # suffix for all IDP-defined roles, used to match naming conventions
# IDP_ROLES_DESCRIPTION = "Automatically generated role"  # Description to attach to automatically generated roles
# IDP_ROLES_MAPPING = {}  # Dictionary that matches the IDP group name to the Lemur role. The Lemur role must exist.
# Example: IDP_ROLES_MAPPING = {"security": "admin", "engineering": "operator", "jane_from_accounting": "read-only"}
IDP_ASSIGN_ROLES_FROM_USER_GROUPS = True  # Assigns a Lemur role for each group found attached to the user
IDP_CREATE_ROLES_FROM_USER_GROUPS = True  # Creates a Lemur role for each group found attached to the user if missing
# Protects the built-in groups and prevents dynamically assigning users to them. Prevents IDP admin from becoming
# Lemur admin. Use IDP_ROLES_MAPPING to create a mapping to assign these groups if desired. eg {"admin": "admin"}
IDP_PROTECT_BUILTINS = True
IDP_CREATE_PER_USER_ROLE = True  # Generates Lemur role for each user (allows cert assignment to a single user)

# # this is the secret used to generate oauth state tokens
# OAUTH_STATE_TOKEN_SECRET = repr(environ.get('OAUTH_STATE_TOKEN_SECRET', '')

# REDIS_HOST = 'redis'
# REDIS_PORT = 6379
# REDIS_DB = 0
# CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'
# CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
# CELERY_IMPORTS = ('lemur.common.celery')
# CELERYBEAT_SCHEDULE: Dict[str, Any] = {
#     All tasks are disabled by default. Enable any tasks you wish to run.
#     'fetch_all_pending_acme_certs': {
#         'task': 'lemur.common.celery.fetch_all_pending_acme_certs',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(minute="*"),
#     },
#     'remove_old_acme_certs': {
#         'task': 'lemur.common.celery.remove_old_acme_certs',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=8, minute=0, day_of_week=5),
#     },
#     'clean_all_sources': {
#         'task': 'lemur.common.celery.clean_all_sources',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=5, minute=0, day_of_week=5),
#     },
#     'sync_all_sources': {
#         'task': 'lemur.common.celery.sync_all_sources',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour="*/2", minute=0),
#     },
#     'report_celery_last_success_metrics': {
#         'task': 'lemur.common.celery.report_celery_last_success_metrics',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(minute="*"),
#     },
#     'certificate_reissue': {
#         'task': 'lemur.common.celery.certificate_reissue',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=9, minute=0),
#     },
#     'certificate_rotate': {
#         'task': 'lemur.common.celery.certificate_rotate',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#     },
#     'get_all_zones': {
#         'task': 'lemur.common.celery.get_all_zones',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(minute="*/30"),
#     },
#     'check_revoked': {
#         'task': 'lemur.common.celery.check_revoked',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#     }
#     'enable_autorotate_for_certs_attached_to_destination': {
#         'task': 'lemur.common.celery.enable_autorotate_for_certs_attached_to_destination',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#     }
#     'enable_autorotate_for_certs_attached_to_endpoint': {
#         'task': 'lemur.common.celery.enable_autorotate_for_certs_attached_to_endpoint',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#     }
#     'notify_expirations': {
#         'task': 'lemur.common.celery.notify_expirations',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#      },
#     'notify_authority_expirations': {
#         'task': 'lemur.common.celery.notify_authority_expirations',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0),
#     },
#     'send_security_expiration_summary': {
#         'task': 'lemur.common.celery.send_security_expiration_summary',
#         'options': {
#             'expires': 180
#         },
#         'schedule': crontab(hour=10, minute=0, day_of_week='mon-fri'),
#     }
# }
# CELERY_TIMEZONE = 'UTC'
#
# LEMUR_EMAIL = 'lemur@example.com'
# LEMUR_SECURITY_TEAM_EMAIL_INTERVALS = [15, 2]
# LEMUR_DEFAULT_EXPIRATION_NOTIFICATION_INTERVALS = [30, 15, 2]
# LEMUR_EMAIL_SENDER = 'smtp'
# # Mail configuration
# MAIL_SERVER = 'mail.example.com'
#
# PUBLIC_CA_DEFAULT_VALIDITY_DAYS = 397
# PUBLIC_CA_MAX_VALIDITY_DAYS = 397
# DEFAULT_VALIDITY_DAYS = 365
#
# LEMUR_OWNER_EMAIL_IN_SUBJECT = False
# LEMUR_DEFAULT_AUTHORITY = str(environ.get('LEMUR_DEFAULT_AUTHORITY', 'ExampleCa'))
# LEMUR_DEFAULT_ROLE = 'operator'

# Authority Settings - These will change depending on which authorities you are using
# current_path = dirname(realpath(__file__))

# DNS Settings

# exclude logging missing SAN, since we can have certs from private CAs with only cn, prod parity
# LOG_SSL_SUBJ_ALT_NAME_ERRORS = False
#
# ACME_DNS_PROVIDER_TYPES = {"items": [
#     {
#         'name': 'route53',
#         'requirements': [
#             {
#                 'name': 'account_id',
#                 'type': 'int',
#                 'required': True,
#                 'helpMessage': 'AWS Account number'
#             },
#         ]
#     },
#     {
#         'name': 'cloudflare',
#         'requirements': [
#             {
#                 'name': 'email',
#                 'type': 'str',
#                 'required': True,
#                 'helpMessage': 'Cloudflare Email'
#             },
#             {
#                 'name': 'key',
#                 'type': 'str',
#                 'required': True,
#                 'helpMessage': 'Cloudflare Key'
#             },
#         ]
#     },
#     {
#         'name': 'dyn',
#     },
#     {
#         'name': 'ultradns',
#     },
# ]}

# # Authority plugins which support revocation
# SUPPORTED_REVOCATION_AUTHORITY_PLUGINS = ['acme-issuer']
