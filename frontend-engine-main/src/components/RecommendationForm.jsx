import React, { useState } from 'react';

function RecommendationForm({onReceiveData}) {
  const [input, setInput] = useState('');
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [user, setUser] = useState([]);

  const sendDataToParent = (data) => {
    onReceiveData(data);
  };

  const fetchRecommendations = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:5000/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input }),
      });
      const data = await response.json();

      if (data.error) {
        setError(data.error);
        setRecommendations([]);
      } else {
        setError('');
        setRecommendations(data.recommendations);
        sendDataToParent(data.recommendations);
        //onReceiveData(data.recommendations);
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    }
    setIsLoading(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetchRecommendations();
    setUser(input);
    setInput(''); 
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Enter game preferences, genre, etc."
          required
        />
        <button type="submit">Get Recommendations</button>
      </form>

      <div className="recommendations">
        {isLoading ? (
        <p className="loading">Looking for user with id {user}...</p>
        ) : error ? (
            <p className="error">{error}</p>
          ) : recommendations.length > 0 ? (
            <ul>
              {recommendations.map((game, index) => (
                <li key={index} className="recommended-game">{game}</li>
              ))}
            </ul>
          ) : (
            <p>No recommendations yet. Enter your preferences and submit the form.</p>
          )}
      </div>
      <div>
      </div>

    </div>
  );
}

export default RecommendationForm;