from ast import arg
import pandas as pd
from happytransformer import HappyGeneration, GENSettings
from server.text2sql.gpt_model import GPTModel

model = GPTModel(model_path="./API/server/pretrain-model/train_model2")


model_dict = {
    "baseline": model,
}


def generate_code(schema, question, settings):
    model_ver = settings["model_ver"]
    model = model_dict[model_ver]
    sql = model.generate(schema, question)

    return sql


if __name__ == "__main__":
    print(generate_code(schema="a", question="b", settings={"model_ver": "baseline"}))
