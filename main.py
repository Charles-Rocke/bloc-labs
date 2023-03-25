from website.app import create_app
from website import api
import uvicorn
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import current_app

app = create_app()
api.mount("/", WSGIMiddleware(app))


if	__name__	==	"__main__":
		#	run	flask	application
		uvicorn.run(api, host="0.0.0.0", port=8000)