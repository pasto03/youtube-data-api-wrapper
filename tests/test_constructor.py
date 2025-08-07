import config
import json

from yt_pipeline.pipeline import Pipeline, PipelineStacksConstructor

devKey = open("devKey").read()

with open(r"D:\Python Projects\YouTube Data API Wrapper v1\youtube-data-api-wapper\tests\input.json", "rb") as f:
    input_json = json.load(f)

# print(input_json)

constructor = PipelineStacksConstructor()
stacks = constructor.invoke(input_json)
# print(stacks)
pipeline = Pipeline(stacks=stacks, developerKey=devKey)
import logging

# logging.getLogger().setLevel(logging.INFO)
dlv = pipeline.invoke()
dlv.to_json("./output.json")