import os
import uvicorn

DEFAULT_PORT = 8000

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=os.getenv("PORT", DEFAULT_PORT),
        reload=True
    )
