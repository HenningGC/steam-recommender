import React, { useState } from 'react';
import SteamyBubble from './SteamyBubble';
import RecommendationForm from './RecommendationForm';
import styles from './SteamyContainer.module.css';
import Chatbox from './ChatBox';

const SteamyContainer = () => {
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [recommendations, setRecommendations] = useState([]);

  const handleBubbleClick = () => {
    setIsFormVisible(!isFormVisible);
  };

  const handleChildData = (data) => {
    setRecommendations(data);
    console.log(data)
  };


  return (  
    <div className={styles.chatBotContainer}>
      <SteamyBubble onClick={handleBubbleClick} />
      {isFormVisible && (
        <div className={styles.formContainer}>
          <h1>Recommender</h1>
          <RecommendationForm onReceiveData={handleChildData}/>
          {recommendations.length > 0 && (<Chatbox/>)}
        </div>
      )}
    </div>
  );
};

export default SteamyContainer;
