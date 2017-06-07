import os
import pymongo
import ssl
from bson.objectid import ObjectId

# Build an aggregation pipeline that populates connections and vpnConnections
pipeline = [
    {
        "$unwind": "$activityList"
    },
    {
        "$lookup": {
            "from": "connectionConfigs",
            "localField": "activityList.connection",
            "foreignField": "_id",
            "as": "activityList.config.connection"
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "name": {"$first": "$name"},
            "path": {"$first": "$path"},
            "schedule": {"$first": "$schedule"},
            "pokeInterval": {"$first": "$pokeInterval"},
            "timeout": {"$first": "$timeout"},
            "accountId": {"$first": "$accountId"},
            "activityList": {"$push": "$activityList"}
        }
    },
    {
        "$unwind": '$activityList'
    },
    {
        "$unwind": {
            "path": "$activityList.config.connection",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "connectionConfigs",
            "localField": "activityList.config.connection.vpnConnection",
            "foreignField": "_id",
            "as": "activityList.config.connection.vpnConnection"
        }
    },
    {
        "$unwind": '$activityList'
    },
    {
        "$unwind": {
            "path": "$activityList.config.connection.vpnConnection",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$group": {
            "_id": '$_id',
            "name": {"$first": "$name"},
            "path": {"$first": "$path"},
            "schedule": {"$first": "$schedule"},
            "pokeInterval": {"$first": "$pokeInterval"},
            "timeout": {"$first": "$timeout"},
            "accountId": {"$first": "$accountId"},
            "activityList": {"$push": "$activityList"}
        }
    }
]


class MongoClient:
    def __init__(self):
        # Get mongo url.
        mongo_url = os.getenv('MONGO_URL', '')

        # Connect to mongo.
        print('Connecting to mongodb.')
        self.client = pymongo.MongoClient(mongo_url, ssl_cert_reqs=ssl.CERT_NONE)
        self.db = self.client.get_default_database()

    def workflow_configs(self):
        return self.db.workflows.aggregate(pipeline)

    def webhook_configs(self):
        return self.db.webhookConfigs.aggregate(pipeline)

    def ftp_configs(self):
        return self.db.ftpConfigs.aggregate(pipeline)

    def close(self):
        self.client.close()