#! /usr/bin/env python
#
# Mixpanel, Inc. -- http://mixpanel.com/
#
# Python API client library to consume mixpanel.com analytics data.
#
# Copyright 2010-2013 Mixpanel, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import csv
import base64
import json
import urllib
import urllib2

class Mixpanel(object):

    ENDPOINT = 'https://mixpanel.com/api'
    VERSION = '2.0'

    def __init__(self, api_secret):
        self.api_secret = api_secret

    def request(self, methods, params, http_method='GET', format='json'):
        """
            methods - List of methods to be joined, e.g. ['events', 'properties', 'values']
                      will give us http://mixpanel.com/api/2.0/events/properties/values/
            params - Extra parameters associated with method
        """
        # print methods, params
        params['format'] = format

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods)
        # print request_url,"urllllllllll"
        if http_method == 'GET':
            data = None
            request_url = request_url + '/?' + self.unicode_urlencode(params)
            # print request_url,"inisde if url"
        else:
            data = self.unicode_urlencode(params)
            # print data,"data"
        headers = {'Authorization': 'Basic {encoded_secret}'.format(encoded_secret=base64.b64encode(self.api_secret))}
        request = urllib2.Request(request_url, data, headers)
        # print request,"request1"
        response = urllib2.urlopen(request, timeout=120)
        return json.loads(response.read())

    def unicode_urlencode(self, params):
        """
            Convert lists to JSON encoded strings, and correctly handle any
            unicode URL parameters.
        """
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
            if isinstance(param[1], list):
                params[i] = (param[0], json.dumps(param[1]),)

        return urllib.urlencode(
            [(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params]
        )

    def request_segment(self, methods, params, http_method='GET', format='json' ):
            # --------------------------------------------------------------------------------------
        # print methods, params
        # params['format'] = format

        request_url = '/'.join([self.ENDPOINT, str(self.VERSION)] + methods)
        # print request_url,"urllllllllll"
       
        if http_method == 'GET':
            data = None
            request_url = request_url + '/?' + self.unicode_urlencode(params)
            # print request_url,"inisde if url"
        else:
            data = self.unicode_urlencode(params)
            # print data,"data"
        
        headers = {'Authorization': 'Basic {encoded_secret}'.format(encoded_secret=base64.b64encode(self.api_secret))}
        request = urllib2.Request(request_url, data, headers)
        # print request,"request1"
        response = urllib2.urlopen(request, timeout=120)
        return json.loads(response.read())

# -------------------------------------------------------------------------------------------


if __name__ == '__main__':
    api = Mixpanel(api_secret='dde2d9b88cb4e1d216ab005cd53a2665')
   
    # print data for CC Claim Center Selection
    data_dict = {}
    data1 = api.request_segment(['segmentation'], {
        'event': "CC Claim Center Selection",
        'unit':'day',
        'from_date': '2018-03-01',
        'to_date': '2018-03-31',
        'on': 'properties["CC Claim Center Selection"]'

    })

    # print (data1['data']['values'])
    # print data1
    sum = 0

    for k,v in (data1['data']['values']['undefined']).iteritems():
        sum += v
    print "CC Claim Center Selection:",sum 
    data_dict ["CC Claim Center Selection"] = sum
    #print data for Fl Clm Conf
    data2 = api.request_segment(['segmentation'], {
        'event': "FL Clm Conf",
        'unit':'day',
        'from_date': '2018-03-01',
        'to_date': '2018-03-31',
        'on': 'properties["FL Clm Conf"]'

    })  
    # print (data2['data']['values'])
    # print data2
    sum = 0

    for k,v in (data2['data']['values']['undefined']).iteritems():
        sum += v
    print "Fl Clm Conf:",sum 
    data_dict ["Fl Clm Conf"] = sum
    print data_dict



     
    coloumns = []
    for i in data_dict:
        coloumns.append(i)
    print coloumns
    myFile = open('Export_report.csv', 'w')


    with myFile:
        writer = csv.DictWriter(myFile, fieldnames=coloumns)
        writer.writeheader()
        # writer = csv.writer(myFile)
        writer.writerows([data_dict])
         
    print("Writing complete")


    # writing the data on csv file

# {
#     u 'legend_size': 1, u 'data': {
#         u 'series': [u '2018-03-02', u '2018-03-03', u '2018-03-04', u '2018-03-05', u '2018-03-06', u '2018-03-07', u '2018-03-08', u '2018-03-09', u '2018-03-10', u '2018-03-11', u '2018-03-12', u '2018-03-13', u '2018-03-14', u '2018-03-15', u '2018-03-16', u '2018-03-17', u '2018-03-18', u '2018-03-19', u '2018-03-20', u '2018-03-21', u '2018-03-22', u '2018-03-23', u '2018-03-24', u '2018-03-25', u '2018-03-26', u '2018-03-27', u '2018-03-28', u '2018-03-29', u '2018-03-30', u '2018-03-31', u '2018-04-01'],
#         u 'values': {
#             u 'undefined': {
#                 u '2018-03-08': 34,
#                 u '2018-03-28': 41,
#                 u '2018-03-29': 20,
#                 u '2018-03-17': 23,
#                 u '2018-03-16': 22,
#                 u '2018-03-15': 51,
#                 u '2018-03-14': 47,
#                 u '2018-03-13': 31,
#                 u '2018-03-12': 41,
#                 u '2018-03-11': 10,
#                 u '2018-03-10': 18,
#                 u '2018-03-31': 31,
#                 u '2018-03-30': 44,
#                 u '2018-03-19': 23,
#                 u '2018-03-18': 18,
#                 u '2018-04-01': 26,
#                 u '2018-03-02': 40,
#                 u '2018-03-03': 39,
#                 u '2018-03-04': 31,
#                 u '2018-03-05': 59,
#                 u '2018-03-06': 36,
#                 u '2018-03-07': 35,
#                 u '2018-03-26': 36,
#                 u '2018-03-09': 13,
#                 u '2018-03-24': 24,
#                 u '2018-03-25': 18,
#                 u '2018-03-22': 35,
#                 u '2018-03-23': 36,
#                 u '2018-03-20': 43,
#                 u '2018-03-21': 47,
#                 u '2018-03-27': 39
#             }
#         }
#     }
# }