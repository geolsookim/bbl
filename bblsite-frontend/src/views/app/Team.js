import React, { useState, useEffect, Fragment } from 'react';
import { useParams, Link } from 'react-router-dom';

const Team = () => {
  const [loading, setLoading] = useState(true);
  const [team, setTeam] = useState('');
  const [teamName, setTeamName] = useState('');
  const [teamAvgScore, setTeamAvgScore] = useState('');
  const { teamId } = useParams();
  
  useEffect(() => {
    if (localStorage.getItem('token') === null) {
      window.location.replace('http://localhost:3000/login');
    } else {
      fetch(`http://127.0.0.1:8000/api/v1/team/${teamId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Token ${localStorage.getItem('token')}`
        }
      })
        .then(res => res.json())
        .then(data => {
          setTeam(data.members)
          setTeamName(data.name)
          setTeamAvgScore(data.average_score)
          setLoading(false);
        });
    }
  }, []);

  return (
    <div>
      {loading === false && (
        <Fragment>
          <h1>Team: {teamName}</h1>
          <div><h2>Average Score: {teamAvgScore}</h2></div>
          <div>{ 
           team.map(member => <div><strong>
             <Link to={`/player/${member.id}`}>{member.full_name}</Link>
             </strong></div>) 
          }</div>
        </Fragment>
      )}
    </div>
  );
};

export default Team;
