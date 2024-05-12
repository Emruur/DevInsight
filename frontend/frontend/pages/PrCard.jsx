import React from "react";
import { useState, useEffect } from "react";

const PrCard = ({ prName, prData }) => {
  const [contributor, setContributor] = useState(prName);

  const [prsContributed, setPrsContributes] = useState(
    prData[0][0] + ": " + prData[0][1]
  );
  const [sentimentScore, setSentimentScore] = useState(
    prData[1][0] + ": " + prData[1][1]
  );

  useEffect(() => {
    setPrsContributes(prData[0][0] + ": " + prData[0][1]);
    setSentimentScore(prData[1][0] + ": " + prData[1][1]);
    setContributor(prName);
  }, [prData, prData, prName]);

  return (
    <div>
      <div>
        <div className="card my-2" style={{ width: "100%", backgroundColor: "#fff" }}>
          <div className="card-body">
            <h5 className="card-title">Contributor: {contributor}</h5>
            <p className="card-text">{prsContributed}</p>
            <p className="card-text">{sentimentScore}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrCard;
