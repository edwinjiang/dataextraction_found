#!/usr/bin/python
#encoding:utf8

import pymongo

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$group":{"_id":"$source","count":{"$sum":1}}},{"$sort":{"count":-1}}]
    return pipeline

def tweet_sources(db, pipeline):
    return [doc for doc in db.tweets.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('twitter')
    pipeline = make_pipeline()
    result = tweet_sources(db, pipeline)
    import pprint
    pprint.pprint(result[0])
    assert result[0] == {u'count': 868, u'_id': u'web'}

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [{"$match":{"user.time_zone":{"$regex":"Brasilia"},
                           "user.statuses_count":{"$gt":100}}},
                {"$project":{"followers":"$user.followers_count","screen_name":"$user.screen_name","tweets":"$user.statuses_count"}},
                {"$sort":{"followers":-1}},
                {"$limit":1}]

    # # pipipeline = [{"$match":{"country":{"$regex":"India"}}},
    #             {"$unwind":"$isPartOf"},
    #             {"$group":{"_id":"$isPartOf",
    #             "count":{"$sum":1}}},
    #             {"$sort":{"count":-1}},
    #             {"$limit":1}]
    # # return pipeline
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.tweets.aggregate(pipeline)]


if __name__ == '__main__':
    db = get_db('twitter')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result)
    assert len(result) == 1
    assert result[0]["followers"] == 17209