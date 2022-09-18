from datetime import datetime
from elasticsearch import Elasticsearch

# Connect to 'http://localhost:9200'
es = Elasticsearch(
    "http://elasticsearch:9200",
    # ca_certs="/spark-driver/http_ca.crt",
    # basic_auth=("elastic", "_=-wvIq_=A_2LjIP14Zm"),
)

# Datetimes will be serialized:
es.index(
    index="my-index-000001",
    id=42,
    document={"any": "data", "timestamp": datetime.now()},
)
# {'_id': '42', '_index': 'my-index-000001', '_type': 'test-type', '_version': 1, 'ok': True}

# ...but not deserialized
es.get(index="my-index-000001", id=42)["_source"]
# {'any': 'data', 'timestamp': '2013-05-12T19:45:31.804229'}
