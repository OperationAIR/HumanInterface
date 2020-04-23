import gettext
import os
from pathlib import Path

from utils.config import ConfigValues


'''
How to use Internationalization.

Surround all the strings that you want to be translated with '_()' (underscore and brackets).

In the beginnin of the file import the Internationalization class:
from utils.internationalization import Internationalization

and in the init function (or somewhere before any _(strings) are used) add:
Internationalization()

Use xgettext to extract all these text items, from scr folder run:
find . -name "*.py" > POTFILES
xgettext --files-from=POTFILES -o operationAIR.pot

After this POTFILES can be deleted

Than use a program like poedit (https://poedit.net) to generate translations for each python file 
and language. Save (in this example for English use folder 'en') in ROOT_DIR/locale/en/LC_MESSAGES/
In the save popup use the name 'operationAIR'. This will generate two files. 

In the config.yml file the language can be selected. The translations for this language obviously need
to be in the locale folder.

To update these files generate an updated operationAIR.pot file with xgettext explained above,
then open the operationAIR.po (NOT pot!!) in Poedit en select the option from the menu to update from POT-file.
And update your translations accordingly. Don't forget to save. :)

'''

class Internationalization():
    def __init__(self):
        self.domain = 'operationAIR'

        ROOT_DIR = str(Path(os.path.dirname(os.path.abspath(__file__))).parent.parent)

        self.localedir = ROOT_DIR + '/locale'

        self.config = ConfigValues()

        self.lang = self.config.values['defaultSettings']['language']

        translate = gettext.translation(self.domain, self.localedir, [self.lang], fallback=True)
        translate.install()
