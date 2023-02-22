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

@app.get("/cp_result")
def process_cap():
    """return image process cap"""
    from process_cap import process_capability
    import numpy as np

    data = np.random.normal(loc=5,scale=1,size=100)

    result,cp,cpk,z,sample_mean,sample_std,sample_max,sample_min,sample_median,pct_below_LSL,pct_above_USL = process_capability(data,pic=False)

    return {"result":result,"cp":cp,"cpk":cpk,"z":z,
    "sample_mean":sample_mean,"sample_std":sample_std,"sample_max":sample_max,
    "sample_min":sample_min,"sample_median":sample_median,"pct_below_LSL":pct_below_LSL,"pct_above_USL":pct_above_USL}

@app.post("/test_post")
def test_post(input_1):
    return {"result":input_1}
    
# %%


@app.post("/pareto")
def test_post(mc_no):
    from pareto import pareto_chart
    from io import BytesIO
    from fastapi.responses import StreamingResponse
    filtered_image = BytesIO()
    result = pareto_chart(mc_no)

    if result == None:
        return {"result":f"{mc_no} is no machine data"}
    else:
        result.savefig(filtered_image, format="JPEG")
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type="image/jpeg")


#result -> "no data machine"
    
@app.post("/oee")
def oee(date,machine_no):
    from oee import oee_chart
    from io import BytesIO
    from fastapi.responses import StreamingResponse
    filtered_image = BytesIO()
    result = oee_chart(date,machine_no)
    
    if type(result) == str:
        return {"error":result}
    else:
        result.savefig(filtered_image, format="JPEG")
        filtered_image.seek(0)
        return StreamingResponse(filtered_image, media_type="image/jpeg")