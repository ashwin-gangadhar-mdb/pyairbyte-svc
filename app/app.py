from typing import Generator, List 
from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
import airbyte as ab
import json
import pandas as pd
# Write a flask api with uvicorn to read all supported sources with pyairbyte
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

@app.route('/sources', methods=['GET'])
def get_sources():
    sources = list(filter(lambda x: x.split("-")[0]=="source", ab.get_available_connectors()))
    return jsonify(sources)

def fetch_data(source, config, streams: List[str]= None):
    data_obj = ab.get_source(source, config=config, install_if_missing=True)
    data_obj.check()
    if streams:
        print(">>>>>>>>>>>>>>>>>>>Streams>>>>>>>>>>>>>>>>>>>>>>>>>",streams)
        data_obj.select_streams(streams)
    else:
        data_obj.select_all_streams()
    result: ab.ReadResult = data_obj.read()
    lst = []
    for stream in streams:
        df = result[stream].to_pandas()
        df["source"] = stream
        json_res = df.to_dict("records")        
        lst += json_res
    return lst
    # for item in result.streams.items():
    #     res = str(item[1].to_pandas().to_dict())
    #     print(item[0], res)
    #     yield jsonify({item[0]: res})



@app.route('/ab/source', methods=['POST'])
def get_data():
    data = request.json
    source = None
    config = None
    streams = None
    if "source" in data:
        source = data["source"]
    if "config" in data:
        config = data["config"]
    if "streams" in data:
        foo = data["streams"].split(",")
        streams = list(map(str.strip, foo))
    if source and config:
        # def generate_data():
        #     for chunk in fetch_data(source, config, streams):
        #         yield jsonify(chunk)
        # return Response(
        #     stream_with_context(generate_data())
        # )
        return jsonify({"data": fetch_data(source, config, streams), "source": source, "stream": streams})
    else:
        return jsonify({"error": "Invalid input, 'source' and 'config' are required"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

# print(fetch_data("source-faker", {"count": 100}, ["products"]))