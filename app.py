import os
import importlib
from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

# Auto-discover and register all Blueprints inside modules/
MODULES_DIR = os.path.join(os.path.dirname(__file__), "modules")
for filename in sorted(os.listdir(MODULES_DIR)):
    if filename.endswith(".py") and not filename.startswith("_"):
        module_name = f"modules.{filename[:-3]}"
        mod = importlib.import_module(module_name)
        if hasattr(mod, "bp"):
            app.register_blueprint(mod.bp)

@app.get("/")
def serve_ui():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)