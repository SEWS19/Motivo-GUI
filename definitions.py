# vim:set ts=2 sts=2 sw=2 et:
import os
ROOT_DIR  = os.path.dirname(os.path.abspath(__file__))
UI_DIR  = os.path.join(ROOT_DIR, 'UI')
MOTIVO_DIR = os.getenv('motivo', '') + '/scripts/'
