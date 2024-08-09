from Rutas import create_app
app = create_app()

if __name__=='__main__':
    ## El valor True indica que la app se deja en modo debug
    app.run(debug=True)

