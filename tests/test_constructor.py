import config
import json

from yt_pipeline.pipeline import Pipeline, PipelineStacksConstructor, PipelineEstimator

devKey = open("devKey").read()

with open(r"D:\Python Projects\YouTube Data API Wrapper v1\youtube-data-api-wapper\tests\input.json", "rb") as f:
    input_json = json.load(f)

# print(input_json)

constructor = PipelineStacksConstructor()
stacks = constructor.invoke(input_json, verbose=0)
# print(stacks)
pipeline = Pipeline(stacks=stacks, developerKey=devKey)
import logging

estimator = PipelineEstimator(pipeline)
report = estimator.estimate(verbose=0)
print(report)

# logging.getLogger().setLevel(logging.INFO)
# dlv = pipeline.invoke()
# dlv.to_json("./output.json")