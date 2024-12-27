from flask import Flask, render_template, redirect, request
#flask wtf forms #ver qq é isso

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oValim'

class Calcular:
    def __init__(self, valor):
        self.valor = float(valor)

    def pace_kmH(self):  # Pace em min/km a partir de km/h
        return 60 / self.valor

    def pace_mS(self):  # Pace em min/km a partir de m/s
        return 60 / (self.valor * 3.6)

    def kmH_pace(self):  # Km/h a partir do pace (min/km)
        return 60 / self.valor

    def mS_pace(self):  # m/s a partir do pace (min/km)
        return (60 / self.valor) / 3.6

    def kmH_mS(self):  # Km/h para m/s
        return self.valor / 3.6

    def mS_kmH(self):  # m/s para km/h
        return self.valor * 3.6
    
@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/calcular", methods=['POST', "GET"])
    
def calc():
    if request.method != "POST":
        return "Método não permitido. Use POST para enviar os dados.", 405
    
    tipo = request.form.get("tipo")
    valor = request.form.get("valor")

    try:
        valor = float(valor)
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero.")
    except ValueError as e:
        return render_template("resultado.html", resultado=f"Erro: {e}")
    
    calc = Calcular(valor)
    
    if tipo == "pace":
        resultado = f"{calc.kmH_pace():.2f} km/h\n{calc.mS_pace():.2f} m/s"
    elif tipo == "km/h":
        resultado = f"{calc.pace_kmH():.2f} min/km (pace)\n{calc.kmH_mS():.2f} m/s"
    elif tipo == "m/s":
        resultado = f"{calc.mS_kmH():.2f} km/h\n{calc.pace_mS():.2f} min/km (pace)"
    else:
        resultado = "Tipo de medida inválido."
    
    return render_template("resultado.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)    