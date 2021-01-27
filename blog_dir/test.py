ss = '<p>123</p>'

import re
reg = re.compile(r'<.*?>')
reg.sub('', ss)