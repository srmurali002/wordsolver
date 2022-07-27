The application uses word net to solve for missing letter words based on the given definition.

Open project path in terminal

First run "pip install -r requirements.txt"

Run the app using "streamlit run app.py"

For samples check samples.csv.


Docker build:

"docker build -f Dockerfile -t app:latest ."

Running docker image:

"docker run -p 8501:8501 app:latest"

once started the application can be acessed at : "localhost:8501"
