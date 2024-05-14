import React, { useEffect } from "react";
import { useState } from "react";

const DeveloperCard = ({ devName, devData }) => {
  

  const [additions, setAdditions] = useState(
    devData[0][0] + ": " + devData[0][1]
  );
  const [deletions, setDeletions] = useState(
    devData[1][0] + ": " + devData[1][1]
  );
  const [developerName, setDeveloperName] = useState(
    devData[2][0] + ": " + devData[2][1]
  );
  const [filesChanged, setFilesChanged] = useState(
    devData[3][0] + ": " + devData[3][1]
  );
  const [githubUsername, setGithubUsername] = useState(
    devData[4][0] + ": " + devData[4][1]
  );
  const [numberOfCommits, setNumberOfCommits] = useState(
    devData[5][0] + ": " + devData[5][1]
  );

  useEffect(() => {
    setAdditions(devData[0][0] + ": " + devData[0][1]);
    setDeletions(devData[1][0] + ": " + devData[1][1]);
    setDeveloperName(devData[2][0] + ": " + devData[2][1]);
    setFilesChanged(devData[3][0] + ": " + devData[3][1]);
    setGithubUsername(devData[4][0] + ": " + devData[4][1]);
    setNumberOfCommits(devData[5][0] + ": " + devData[5][1]);
  }, [devData[0], devData[1], devData[2], devData[3], devData[4], devData[5]]);
  // Additions10  Deletions10  Developer NameBenjamin Stürz   Files Changed9   GitHub Usernameriscygeek   Number of Commits3
  return (
    <div>
      <div>
        <div className="card my-2" style={{ width: "100%", backgroundColor: "#fff" }}>
          <div className="card-body">
            <h5 className="card-title">{developerName}</h5>
            <h6 className="card-subtitle mb-2 text-muted">{githubUsername}</h6>
            <p className="card-text">{additions}</p>
            <p className="card-text">{deletions}</p>
            <p className="card-text">{numberOfCommits}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeveloperCard;
