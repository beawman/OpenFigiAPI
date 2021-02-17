# Copyright 2017 Bloomberg Finance L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import urllib2

'''
See https://www.openfigi.com/api for more information.
'''

openfigi_apikey = ''  # Put API Key here
jobs = {"query":"HK","exchCode":"HK","securityType":"Common Stock"}

def map_jobs(jobs):
    '''
    Send an collection of mapping jobs to the API in order to obtain the
    associated FIGI(s).
    Parameters
    ----------
    jobs : list(dict)
        A list of dicts that conform to the OpenFIGI API request structure. See
        https://www.openfigi.com/api#request-format for more information. Note
        rate-limiting requirements when considering length of `jobs`.
    Returns
    -------
    list(dict)
        One dict per item in `jobs` list that conform to the OpenFIGI API
        response structure.  See https://www.openfigi.com/api#response-fomats
        for more information.
    '''
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)    
    openfigi_url = 'https://api.openfigi.com/v2/search'    
    print(json.dumps(jobs))
    request = urllib2.Request(openfigi_url, data=json.dumps(jobs))    
    
    request.add_header('Content-Type','application/json')
    if openfigi_apikey:
        request.add_header('X-OPENFIGI-APIKEY', openfigi_apikey)
    request.get_method = lambda: 'POST'
    connection = opener.open(request)
    if connection.code != 200:
        raise Exception('Bad response code {}'.format(str(response.status_code)))
    return json.loads(connection.read())


def job_results_handler(jobs, job_results):
    '''
    Handle the `map_jobs` results.  See `map_jobs` definition for more info.
    Parameters
    ----------
    jobs : list(dict)
        The original list of mapping jobs to perform.
    job_results : list(dict)
        The results of the mapping job.
    Returns
    -------
        None
    '''
    print(job_results)
    '''
    for job, result in zip(jobs, job_results):
        job_str = '|'.join(job.values())
        figis_str = ','.join([d['figi'] for d in result.get('data', [])])
        result_str = figis_str or result.get('error')
        output = '%s maps to FIGI(s) ->\n%s\n---' % (job_str, result_str)
        print(output)
'''

def main():
    '''
    Map the defined `jobs` and handle the results.
    Returns
    -------
        None
    '''
    job_results = map_jobs(jobs)
    job_results_handler(jobs, job_results)

main()
