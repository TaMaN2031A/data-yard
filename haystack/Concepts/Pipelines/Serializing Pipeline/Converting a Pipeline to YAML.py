from haystack import Pipeline

pipe = Pipeline()
print(pipe.dumps())

with open("test.yml", "w") as f:
    pipe.dump(f)