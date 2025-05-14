import asyncio
import uvicorn
from new_api.app import create_api_app

async def main():
    app = await create_api_app()
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
