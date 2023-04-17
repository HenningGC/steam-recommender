import React from 'react';
import styles from './SteamyBubble.module.css';

const SteamyBubble = ({ onClick }) => {
  return (
    <div className={styles.chatbotBubbleContainer} onClick={onClick}>
      <div className={styles.chatbotBubble}>
        <img src="./steamy.jpg" alt="Chat" />
      </div>
    </div>
  );
};

export default SteamyBubble;
