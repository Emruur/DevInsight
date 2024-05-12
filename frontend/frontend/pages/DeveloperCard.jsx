import React from 'react'

const DeveloperCard = ({devName, devData}) => {
  console.log(devName);
  console.log(devData);
   // Additions10  Deletions10  Developer NameBenjamin Stürz   Files Changed9   GitHub Usernameriscygeek   Number of Commits3
   //TODO card view will be fixed, currently it is just showing the data. data is a 2d array, i.e. data[0] is Addition, data[0][0] 10.
  return (
    <div>DeveloperCard {devData}</div>
  )
}

export default DeveloperCard