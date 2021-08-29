import React, { useState, useEffect, Fragment } from 'react';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  // const [userEmail, setUserEmail] = useState('');
  const [loading, setLoading] = useState(true);
  const [games, setGames] = useState('');

  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      window.location.replace('http://localhost:3000/login');
    } else {
      fetch('http://127.0.0.1:8000/api/v1/game/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(data => {
          setGames(data.results)
          setLoading(false);
        });
    }
  }, []);

  return (
    <div>
      {loading === false && (
        <Fragment>
          <h1>Tournament</h1>
          <div>{
            games.map(game => <div><strong>{game.round}</strong> 
            [<Link to={`/team/${game.home_team_id}`}>{game.home_team}</Link> {game.home_team_score}] vs
            [<Link to={`/team/${game.home_team_id}`}>{game.away_team}</Link> {game.away_team_score}] <strong>WINNER - {game.winner}</strong> </div>)
          }</div>
        </Fragment>
      )}
    </div>
  );
};

export default Dashboard;
