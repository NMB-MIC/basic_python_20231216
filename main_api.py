# %% [markdown]
# #### FastAPI

# %%
#!pip install fastapi
from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
def test():
    """print hello world"""
    return {"result": "hello world"}


@app.get("/test2")
def test2():
    """print hello world"""
    return {"result": "hello world2"}

@app.get("/cp")
def process_cap():
    """return image process cap"""
    from process_cap import process_capability
    from fastapi.responses import StreamingResponse
    from io import BytesIO

    import numpy as np

    data = np.random.normal(loc=5,scale=1,size=100)
    filtered_image = BytesIO()
    fig = process_capability(data)
    fig.savefig(filtered_image, format="JPEG")
    filtered_image.seek(0)
    return StreamingResponse(filtered_image, media_type="image/jpeg")
