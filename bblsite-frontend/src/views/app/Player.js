  import React, { useState, useEffect, Fragment } from 'react';
import { useParams, Link } from 'react-router-dom';

const Player = () => {
  const [loading, setLoading] = useState(true);
  const [teamName, setTeamName] = useState('');
  const [playerAvgScore, setPlayerAvgScore] = useState('');
  const [fullName, setFullName] = useState('');
  const [height, setHeight] = useState('');
  const [gamesPlayed, setGamesPlayed] = useState('');
  const { playerId } = useParams();

  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      window.location.replace('http://localhost:3000/login');
    } else {
      fetch(`http://127.0.0.1:8000/api/v1/player/${playerId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(data => {
          setTeamName(data.team)
          setFullName(data.full_name)
          setHeight(data.height)
          setGamesPlayed(data.games_played)
          setPlayerAvgScore(data.average_score)
          setLoading(false);
        });
    }
  }, []);

  return (
    <div>
      {loading === false && (
        <Fragment>
          <h1>{fullName}</h1>
          <div>Team: {teamName}</div>
          <div>Height: {height} cm</div>
          <div>Games Played: {gamesPlayed}</div>
          <div>Average Score: {playerAvgScore}</div>
        </Fragment>
      )}
    </div>
  );
};

export default Player;
