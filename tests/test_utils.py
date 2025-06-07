import sys
import os
import types

# Ensure the project root is on sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

class DummyTranslator:
    def __init__(self, *args, **kwargs):
        pass
    def translate(self, text):
        return text

# Stub external dependencies before importing bot
stubs = {
    'deep_translator': types.ModuleType('deep_translator'),
    'telegram': types.ModuleType('telegram'),
    'telegram.ext': types.ModuleType('telegram.ext'),
    'telegram.constants': types.ModuleType('telegram.constants'),
    'pytz': types.ModuleType('pytz'),
    'requests': types.ModuleType('requests'),
}
for name, module in stubs.items():
    sys.modules.setdefault(name, module)

stubs['deep_translator'].GoogleTranslator = DummyTranslator
stubs['telegram'].Update = object
stubs['telegram'].Bot = object
stubs['telegram.ext'].Application = object
stubs['telegram.ext'].CommandHandler = object
stubs['telegram.ext'].filters = object
stubs['telegram.constants'].ParseMode = object
stubs['pytz'].timezone = lambda name: None

import bot


def test_escape_markdown():
    text = "Special _*[]~`>#+=|{} characters"
    expected = "Special \\_\\*\\[\\]\\~\\`\\>\\#\\+\\=\\|\\{\\} characters"
    assert bot.escape_markdown(text) == expected


def test_calculate_tahajjud_time():
    assert bot.calculate_tahajjud_time('22:00', '04:00') == '01:00'
