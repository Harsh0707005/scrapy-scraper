import os

with open("products.json", "a") as f:
    json_files = [f for f in os.listdir() if f.endswith(".json")]
    for file in json_files:
        if (file!="products.json"):
            with open(file, "r") as temp:
                f.write(temp.read())
            f.write("\n")