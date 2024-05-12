import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/router";
import Header from "../../Header";
import DeveloperCard from "../../DeveloperCard";
import Button from "react-bootstrap/Button";
import IssueCard from "../../IssueCard";
import PrCard from "../../PrCard";

const Page = () => {
  const [repoData, setRepoData] = useState({});

  const [developerData, setDeveloperData] = useState({});

  const [developerNames, setDeveloperNames] = useState([]);
  const [developerDataList, setDeveloperDataList] = useState([]);

  const [issueNames, setIssueNames] = useState([]);
  const [issueDataList, setIssueDataList] = useState([]);

  const [prNames, setPrNames] = useState([]);
  const [prDataList, setPrDataList] = useState([]);

  const router = useRouter();
  const { slug } = router.query;

  useEffect(() => {
    if (slug) {
      fetch(`http://127.0.0.1:5000/get_analysis/${slug[0]}/${slug[1]}`)
        .then((response) => response.json())
        .then((data) => {
          setRepoData(data);

          if (data.commits) {
            const names = [];
            const dataList = [];
            //TODO only the commits are being fetched, other types of data (i.e. issue created) will be fetched later
            for (let developerName in data.commits) {
              names.push(developerName);
              dataList.push(Object.entries(data.commits[developerName]));
            }
            setDeveloperNames(names);
            setDeveloperDataList(dataList);
          }

          if (data.issues) {
            const issue_names = [];
            const issue_dataList = [];
            for (let issueName in data.issues) {
              issue_names.push(issueName);
              issue_dataList.push(Object.entries(data.issues[issueName]));
            }
            setIssueNames(issue_names);
            setIssueDataList(issue_dataList);
          }

          if (data.prs) {
            const pr_names = [];
            const pr_dataList = [];
            for (let prName in data.prs) {
              pr_names.push(prName);
              pr_dataList.push(Object.entries(data.prs[prName]));
            }
            setPrNames(pr_names);
            setPrDataList(pr_dataList);
          }
        })
        .catch((error) => console.error("Error fetching data:", error));
    }
  }, [slug]);

  const handleBack = () => {
    router.push("/");
  };

  return (
    <>
      <Header header_name={repoData.repo_name} />
      <div className="container pt-5">
        <div className="row d-flex justify-content-center align-items-center">
          <div className="col-10 d-flex justify-content-center">
            <div className="col-12">
              <div className="row">
                {developerDataList.map((developerData, idx) => (
                  <DeveloperCard
                    key={idx}
                    devName={developerNames[idx]}
                    devData={developerData}
                  />
                ))}
                
                {issueDataList.map((issueData, idx) => (
                  <IssueCard
                    key={idx}
                    issueName={issueNames[idx]}
                    issueData={issueData}
                  />
                ))}

                {prDataList.map((prData, idx) => (
                  <PrCard
                    key={idx}
                    prName={prNames[idx]}
                    prData={prData}
                  />
                ))}

                <Button className="btn-teal" onClick={() => handleBack()}>
                  Back
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Page;
