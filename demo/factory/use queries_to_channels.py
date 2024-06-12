"""
demo -- use QueriesToChannelDetailsFactory to obtain channel details by specific keywords
Note: Only 1 channel will be obtained for each keywords currently

*This is a developing Factory module, huge cost wastage will occur
"""

import sys_config
from src.factory import QueriesToChannelDetailsFactory


channel_names = ['worship and praise']
factory = QueriesToChannelDetailsFactory(queries=channel_names)
recorder = factory.manufacture()