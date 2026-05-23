from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="短剧互动系统后端")


# 把 D:\episode content 这个本地文件夹挂载到 /videos 路径
app.mount(
    "/videos",
    StaticFiles(directory=r"D:\upload\videos"),
    name="videos"
)


@app.get("/")
def root():
    return {
        "message": "FastAPI 启动成功"
    }