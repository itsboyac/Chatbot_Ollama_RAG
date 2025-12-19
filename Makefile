scrape_data:
	poetry run python src/scrape_data.py
parse_data:
	poetry run python src/parse_data.py
process_data:
	poetry run python src/clean_then_store.py
test:
	poetry run python test/query.py
app:
	poetry run python src/streamlit.py
all: scrape_data parse_data process_data app

