from flask import Flask, jsonify, request, render_template, session, abort
from turing_machine import TuringMachine
from yaml_loader import load_yaml
import os


app = Flask(__name__)

# Configuraciones disponibles
machine_configs = {
    "recognition": load_yaml('machines/recognitionconfig.yaml'),
    "altering": load_yaml('machines/alteringconfig.yaml')
}

@app.route('/')
def index():
    return render_template('index.html')  # Interfaz de usuario

@app.route('/machines', methods=['GET'])
def get_machines():
    """Devuelve las opciones disponibles de máquinas."""
    return jsonify({
        "machines": [
            {"id": "recognition", "name": "Máquina de Reconocimiento (Palíndromos)"},
            {"id": "altering", "name": "Máquina de Transformación (Invertir y Complementar)"}
        ]
    })

@app.route('/simulate', methods=['POST'])
def simulate():
    """Simula la máquina de Turing seleccionada."""
    data = request.json
    machine_id = data.get("machine_id", "")
    input_string = data.get("input_string", "")

    if machine_id not in machine_configs:
        return jsonify({"error": "Máquina no encontrada"}), 400

    config = machine_configs[machine_id]
    tm = TuringMachine(config)

    tm.load_tape(input_string)
    initial_desc = "⊢["+tm.current_state + ", null]" + input_string
    initial_desc = {"starting_state":tm.current_state, "cache": None, "string":input_string}

    steps = []
    while tm.current_state not in ['qaccept', 'qreject']:
        step_data = tm.execute_step()
        steps.append(step_data["description"])


    # Agregar el último paso para incluir el estado final
    steps.append(tm.execute_step()["description"])


    result = "aceptada" if tm.current_state == 'qaccept' else "rechazada"
    return jsonify({"initial_desc": initial_desc, "steps": steps, "result": result})


@app.route('/simulate_step', methods=['POST'])
def simulate_step():
    machine_id = session.get('machine_id')
    if not machine_id or machine_id not in machine_configs:
        return jsonify({"error": "Máquina no encontrada"}), 400

    tm = session.get('turing_machine')
    if not tm:
        return jsonify({"error": "La máquina no está inicializada"}), 400

    # Leer el string enviado desde el frontend
    data = request.get_json()
    input_string = data.get('input_string')
    if not input_string:
        return jsonify({"error": "No se proporcionó un string para simular."}), 400

    # Reiniciar la máquina con el nuevo string
    tm.load_tape(input_string)
    session['turing_machine'] = tm  # Actualizar sesión

    return jsonify({"message": "Máquina preparada para simular", "input": input_string})


@app.route('/get_machine_strings/<machine_id>', methods=['GET'])
def get_machine_strings(machine_id):
    """Devuelve las cadenas de simulación disponibles para una máquina específica."""

    # Ruta a la configuración de la máquina
    config_path = os.path.join("machines", f"{machine_id}config.yaml")

    if not os.path.exists(config_path):
        return abort(404, description="Máquina no encontrada")

    try:
        config = load_yaml(config_path)
        simulation_strings = config.get("simulation_strings", [])
        return jsonify({
            "machine_id": machine_id,
            "strings": simulation_strings
        })
    except Exception as e:
        return abort(500, description=f"Error al cargar la configuración: {e}")



if __name__ == "__main__":
    app.run(debug=True)
