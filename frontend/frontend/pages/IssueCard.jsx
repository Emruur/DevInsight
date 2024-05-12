import React from 'react'

const IssueCard = ({issueName, issueData}) => {
   console.log(issueName);
   console.log(issueData);
  return (
    <div>IssueCard {issueData}</div>
  )
}

export default IssueCard