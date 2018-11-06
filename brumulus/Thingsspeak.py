import requests
from queuelib import FifoDiskQueue
import time


class Thingsspeak(object):
    """docstring for Thingsspeak"""
    def __init__(self):
        super(Thingsspeak, self).__init__()
        self.retry_queue = FifoDiskQueue("/var/thingsspeak.queue")

    def send(self, values):
        print('Thingspeak.send: {}'.format(values))
        data = {'created_at': values['created_at'],
                  'key': 'MYA8R6YDMDQNM9M9',
                  'field1': values['target_temp'],
                  'field2': values['current_temp'],
                  'field3': values['control_value'],
                  'field4': values['chiller_raw'],
                  'field5': values['heater_raw'],
                  'field6': values['current_temp_2']
                  }
        print values

        r = requests.post("https://api.thingspeak.com/update", data=payload)
        print(r)

#         if response_html != '0':
#             self.retry()
#
#     def retry(self):
#         if (len(self.retry_queue) > 0):
#             time.sleep(15)
#             postdata = self.retry_queue.pop()
#             print "retrying: ", postdata
#             if self.post_data(postdata) == 0:
#                 return
# #
# # 'created_at': self.time,
# #           'target_temp': str(self.target_temp),
# #           'current_temp': '{0:.3f}'.format(self.current_temp),
# #           'control_value': '{0:.0f}'.format(self.control_value),
# #           'chiller': self.chiller.get_state_str(),
# #           'chiller_info': self.chiller.get_info(),
# #           'heater': self.heater.get_state_str(),
# #           'heater_info': self.heater.get_info()
#
#     def post_data(self, postdata):
#         target_url = 'https://api.thingspeak.com/update'
#
#         request = urllib2.Request(target_url, postdata)
#         response_html = None
#         try:
#             response = urllib2.urlopen(request, None, 5)
#             response_html = response.read()
#
#             response.close()
#             print response_html
#
#         except urllib2.HTTPError, e:
#             print 'Server could not fulfill the request. Error code: ' + str(e.code)
#         except urllib2.URLError, e:
#             print 'Failed to reach server. Reason: ' + str(e.reason)
#         except e:
#             print 'Unknown error ' + str(e)
#
#         if response_html == '0' or response_html is None:
#             print "Enquing for retry:", postdata
#             self.retry_queue.push(postdata)
#             return 0
#         return response_html
