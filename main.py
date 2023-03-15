from website.app import create_app
import uvicorn
web_app = create_app()

if	__name__	==	"__main__":
		#	run	flask	application
		web_app.run(debug=True, host="0.0.0.0", port=8080)