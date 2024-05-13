import React from "react";
import { useState, useEffect } from "react";

const IssueCard = ({ issueName, issueData }) => {
  const [user, setUser] = useState(issueName);

  const [avgIssueResolveTime, setAvgIssueResolveTime] = useState(
    issueData[0][0] + ": " + issueData[0][1]
  );
  const [issueAssigned, setIssuesAssigned] = useState(
    issueData[1][0] + ": " + issueData[1][1]
  );
  const [issuesCreated, setIssuesCreated] = useState(
    issueData[2][0] + ": " + issueData[2][1]
  );
  const [issuesResolved, setIssuesResolved] = useState(
    issueData[3][0] + ": " + issueData[3][1]
  );

  useEffect(() => {
    setAvgIssueResolveTime(issueData[0][0] + ": " + issueData[0][1]);
    setIssuesAssigned(issueData[1][0] + ": " + issueData[1][1]);
    setIssuesCreated(issueData[2][0] + ": " + issueData[2][1]);
    setIssuesResolved(issueData[3][0] + ": " + issueData[3][1]);
    setUser(issueName);
  }, [user, issueData[0], issueData[1], issueData[2], issueData[3]]);
  return (
    <div>
      <div>
        <div className="card my-2" style={{ width: "100%", backgroundColor: "#fff" }}>
          <div className="card-body">
            <h5 className="card-title">User: {user}</h5>
            <p className="card-text">{avgIssueResolveTime}</p>
            <p className="card-text">{issueAssigned}</p>
            <p className="card-text">{issuesCreated}</p>
            <p className="card-text">{issuesResolved}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IssueCard;
