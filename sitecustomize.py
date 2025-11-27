import os

if os.environ.get("CI") == "true" and os.name == "nt":
    os.environ["COLORAMA_DISABLE"] = "1"