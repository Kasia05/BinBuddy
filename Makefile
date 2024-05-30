default:
	pip install -r requirements.txt
	python -c 'from binbuddy.interface.main import main; main()'

load_model:
	python -c 'from binbuddy.ml_logic.registry import load_model; load_model()'
