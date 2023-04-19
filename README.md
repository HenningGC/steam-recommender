# Steam Recommendation Engine
This project provides a recommendation engine for Steam games. It uses various machine learning models and techniques to predict and recommend games that a user may be interested in playing.

## Features
An API to extract the data.
<p>
Data preparation
<p>
Data preprocessing
<p>
Data modeling (using LightFM with BPR Loss and Warp Loss, and SVD)
<p>
A frontend for users to input their user ID and receive game recommendations
<p>
A backend to deploy the model and fetch recommendations
<p>
Frontend integration with the OpenAI API.
<p>
## Table of Contents
Installation
<p>
Usage
<p>
API
<p>
Data Preparation
<p>
Data Preprocessing
<p>
Data Modeling
<p>
Frontend
<p>
Backend
<p>
OpenAI API Integration

## Installation
To run this project on your local machine, please follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/HenningGC/steam-recommendation-engine.git
Navigate to the project directory:

bash
Copy code
cd steam-recommendation-engine
Create a virtual environment and activate it (optional but recommended):

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required packages:

Copy code
pip install -r requirements.txt
## Usage
After installing the required packages, follow these steps:

Run the data extraction, preparation, and preprocessing scripts:

Copy code
python data_extraction.py
python data_preparation.py
python data_preprocessing.py
Train the recommendation model:

Copy code
python train_model.py
Start the backend server:

bash
Copy code
python backend/app.py
In a new terminal, navigate to the frontend directory and start the frontend server:

bash
Copy code
cd frontend
yarn
yarn dev
Open your browser and navigate to http://localhost:3000 to start using the recommendation engine.

## API
The project uses the Steam API to extract user data, game details, and user-game interactions.

## Data Preparation
The data_preparation.py script is responsible for downloading and processing raw data from the Steam API. This includes fetching game and user information, as well as user-game interactions such as playtime and user ratings.

## Data Preprocessing
The data_preprocessing.py script performs various data cleaning and transformation tasks, such as removing duplicates, filtering out irrelevant data, and normalizing the data.

## Data Modeling
The train_model.py script trains the recommendation model using the LightFM library with BPR Loss and Warp Loss, as well as Singular Value Decomposition (SVD).

## Frontend
The frontend is built using React and allows users to input their user ID and receive game recommendations. The frontend communicates with the backend to fetch recommendations and displays them to the user.

## Backend
The backend is built using Flask and is responsible for serving the trained model and providing an API for the frontend to fetch recommendations.

## OpenAI API Integration
The frontend is integrated with the OpenAI API to provide additional information and insights about the recommended games. This includes generating game descriptions, reviews, and other relevant information.

## Preview
### Homepage
![image](https://user-images.githubusercontent.com/55255975/231901447-8607f96e-e1d6-42bd-bb31-8f2a4d7659cd.png)

### Recommenders + Chatbot
![image](https://user-images.githubusercontent.com/55255975/231901145-5acc5d4b-1ce4-4e07-a61b-02f72a900900.png)


## Sources:
· https://github.com/nadinezab/video-game-recs
<p>
· https://github.com/haohe1113/Steam-Game-Rcmd-Engine
<p>
· https://github.com/abvnithish/Steam_Game_Recommendation_System
<p>
· https://python.plainenglish.io/recommendation-engine-with-steam-video-games-dataset-98582c11af69
<p>
· https://audreygermain.github.io/Game-Recommendation-System/
<p>
· https://towardsdatascience.com/building-a-game-recommendation-engine-870a1ccd11c4
<p>
· https://towardsdatascience.com/steam-recommendation-systems-4358917288eb
