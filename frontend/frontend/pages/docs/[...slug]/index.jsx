import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/router";
import Header from "../../Header";
import DeveloperCard from "../../DeveloperCard";
import Button from "react-bootstrap/Button";
import IssueCard from "../../IssueCard";
import PrCard from "../../PrCard";
import { IoMdArrowRoundBack } from "react-icons/io";
import { FaFilter } from "react-icons/fa";
import Tab from "react-bootstrap/Tab";
import Tabs from "react-bootstrap/Tabs";
import Spinner from "react-bootstrap/Spinner";
import Form from "react-bootstrap/Form";

const Page = () => {
  const [repoData, setRepoData] = useState({});

  const [selectedCommitFilter, setSelectedCommitFilter] = useState(1);
  const [selectedIssueFilter, setSelectedIssueFilter] = useState(7);
  const [selectedPrFilter, setSelectedPrFilter] = useState(19);

  const handleCommitFilterChange = (e) => {
    const value = Number(e.target.value);
    setSelectedCommitFilter(value);
  };

  useEffect(() => {
    applyFilter();
  }, [selectedCommitFilter]);

  const applyFilter = () => {
    let sortedList;
    switch (selectedCommitFilter) {
      case 1:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[2][1];
          const bValue = b[2][1];

          if (aValue > bValue) {
            return 1;
          } else if (aValue < bValue) {
            return -1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      case 2:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[4][1];
          const bValue = b[4][1];

          if (aValue > bValue) {
            return 1;
          } else if (aValue < bValue) {
            return -1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      case 3:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[0][1];
          const bValue = b[0][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      case 4:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[1][1];
          const bValue = b[1][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      case 5:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[3][1];
          const bValue = b[3][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      case 6:
        sortedList = [...developerDataList].sort((a, b) => {
          const aValue = a[5][1];
          const bValue = b[5][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        setDeveloperDataList(sortedList);
        break;
      default:
      // Handle other cases
    }
  };

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
                <Tabs
                  defaultActiveKey="commits"
                  id="fill-tab-example"
                  className="mb-3"
                  fill
                >
                  <Tab eventKey="commits" title="Commits">
                    <div className="d-flex align-items-center">
                      <Button
                        className="btn-teal go-back-btn mb-2"
                        onClick={() => handleBack()}
                      >
                        <IoMdArrowRoundBack />
                        Back
                      </Button>
                      <Form.Select
                        onChange={(e) => handleCommitFilterChange(e)}
                        defaultValue={selectedCommitFilter}
                        style={{
                          width: "20rem",
                          marginLeft: "1rem",
                          padding: "8px",
                          textAlign: "center",
                          fontSize: "16px",
                        }}
                        aria-label="Default select example"
                      >
                        <option disabled value="0">
                          Filter by:
                        </option>
                        <option value="1">Developer Name</option>
                        <option value="2">GitHub Username</option>
                        <option value="3">Additions</option>
                        <option value="4">Deletions</option>
                        <option value="5">Files Changed</option>
                        <option value="6">Number of Commits</option>
                      </Form.Select>
                    </div>
                    {!developerDataList || developerDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      developerDataList.map((developerData, idx) => (
                        <DeveloperCard
                          key={idx}
                          devName={developerNames[idx]}
                          devData={developerData}
                        />
                      ))
                    )}
                  </Tab>
                  <Tab eventKey="prs" title="PRs">
                    {!issueDataList || issueDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      issueDataList.map((issueData, idx) => (
                        <IssueCard
                          key={idx}
                          issueName={issueNames[idx]}
                          issueData={issueData}
                        />
                      ))
                    )}
                  </Tab>
                  <Tab eventKey="issues" title="Issues">
                    {!prDataList || prDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      prDataList.map((prData, idx) => (
                        <PrCard
                          key={idx}
                          prName={prNames[idx]}
                          prData={prData}
                        />
                      ))
                    )}
                  </Tab>
                </Tabs>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Page;
