import factories
import random
import uuid
from expects import expect, equal
from expects.matchers.built_in import be_above
from expects.matchers.built_in.have_keys import have_key
from datetime import datetime
import pytest
from requests import *
import json
import conftest

from pprint import pprint

"""
for the test_create_person_with_content() method, you should log into the receptiviti account and click the button
"generate key" to get your apikey and apisecret.
Copy and paste them into the liwc method or you could not run the code
"""


def get_content_data(content,**kwargs):
    attribs = {
        "language_content": content,
        "content_source": random.randint(1, 2),
        "content_handle": uuid.uuid4().hex,
        "content_date": datetime.now().isoformat(),
        "recipient_id": None,
        "content_tags": ['tag1', 'tag2', 'tag3'],
        'language': 'english'
        }
    attribs.update(kwargs)
    return attribs


def get_person_data(content=None):
    person_data = {'name': "John {0} Doe".format(uuid.uuid4().hex), 'person_handle': uuid.uuid4().hex, 'gender': 1}
    if content:
        person_data["content"] = content
    return person_data

def test_create_person_with_content(baseurl, apikey, apisecret,content):
    content_data = get_content_data(content)
    person_data = get_person_data(content_data)
    print(content_data)

    person_api_url = conftest.person_api_url(baseurl)
    auth_headers = conftest.auth_headers(apikey, apisecret)

    response = post(person_api_url, json=person_data, headers=auth_headers)

    response_json = json.loads(response.content)
    expect(response.status_code).to(equal(200))
    expect(response_json["name"]).to(equal(person_data["name"]))
    expect(response_json["contents"][0]).to(have_key("receptiviti_scores"))
    expect(response_json["contents"][0]).to(have_key("liwc_scores"))
    return response_json["contents"][0]["liwc_scores"]['categories']

def liwc(tweet):
    a = test_create_person_with_content("https://app.receptiviti.com","5a7c6db7f49b0e04f008db0c", "zAyNNw5iqfZ7p8dmpiu8EXgrQcyFPzs5o1Gzmhmqc3c",tweet["text"])
    
    return(a["article"],a["auxverb"],a["conj"],a["adverb"],a["i"]+a["we"],a["you"],a["they"],a["prep"],a["function"],a["assent"],a["negate"],a["certain"],a["quant"])

#def main():
#    a = liwc("I had a happy day but you are super angry, I think it is because of him")
#    print(a)
#main()


