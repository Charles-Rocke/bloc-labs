from website import create_app

app = create_app()

if	__name__	==	"__main__":
		#	run	flask	application
		app.run(debug=True,	use_reloader=False,	host="0.0.0.0")