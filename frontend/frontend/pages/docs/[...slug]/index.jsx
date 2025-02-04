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
import { Pagination } from 'react-bootstrap';

const Page = () => {
  const [repoData, setRepoData] = useState({});

  const [selectedCommitFilter, setSelectedCommitFilter] = useState(0);
  const [selectedPrFilter, setSelectedPrFilter] = useState(0);
  const [selectedIssueFilter, setSelectedIssueFilter] = useState(0);

  const handleCommitFilterChange = (e) => {
    const value = Number(e.target.value);
    setSelectedCommitFilter(value);
  };

  const handlePRFilterChange = (e) => {
    const value = Number(e.target.value);
    setSelectedPrFilter(value);
  };

  const handleIssuesFilterChange = (e) => {
    const value = Number(e.target.value);
    setSelectedIssueFilter(value);
  };

  useEffect(() => {
    applyCommitFilter();
  }, [selectedCommitFilter]);

  useEffect(() => {
    applyPRFilter();
  }, [selectedPrFilter]);

  useEffect(() => {
    applyIssuesFilter();
  }, [selectedIssueFilter]);

  const applyCommitFilter = () => {
    let sortedList;
    setCurrentCommitPage(1)
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

  const applyPRFilter = () => {
    setCurrentPRPage(1)
    let combinedList = prDataList.map((data, index) => ({
      data,
      name: prNames[index],
    }));

    switch (selectedPrFilter) {
      case 1:
        combinedList.sort((a, b) => {
          const aValue = a.data[0][1];
          const bValue = b.data[0][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      case 2:
        combinedList.sort((a, b) => {
          const aValue = a.data[1][1];
          const bValue = b.data[1][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      default:
      // Handle other cases
    }

    const sortedPrDataList = combinedList.map((item) => item.data);
    const sortedPrNames = combinedList.map((item) => item.name);

    setPrDataList(sortedPrDataList);
    setPrNames(sortedPrNames);
  };

  const applyIssuesFilter = () => {
    setCurrentIssuePage(1)
    let combinedList = issueDataList.map((data, index) => ({
      data,
      name: issueNames[index],
    }));

    switch (selectedIssueFilter) {
      case 1:
        combinedList.sort((a, b) => {
          const aValue = a.data[2][1];
          const bValue = b.data[2][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      case 2:
        combinedList.sort((a, b) => {
          const aValue = a.data[1][1];
          const bValue = b.data[1][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      case 3:
        combinedList.sort((a, b) => {
          const aValue = a.data[3][1];
          const bValue = b.data[3][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      case 4:
        combinedList.sort((a, b) => {
          const aValue = a.data[0][1];
          const bValue = b.data[0][1];

          if (aValue > bValue) {
            return -1;
          } else if (aValue < bValue) {
            return 1;
          } else {
            return 0;
          }
        });
        break;
      default:
      // Handle other cases
    }

    const sortedIssueList = combinedList.map((item) => item.data);
    const sortedIssueName = combinedList.map((item) => item.name);

    setIssueDataList(sortedIssueList);
    setIssueNames(sortedIssueName);
  };

  const [developerNames, setDeveloperNames] = useState([]);
  const [developerDataList, setDeveloperDataList] = useState([]);

  const [issueNames, setIssueNames] = useState([]);
  const [issueDataList, setIssueDataList] = useState([]);

  const [prNames, setPrNames] = useState([]);
  const [prDataList, setPrDataList] = useState([]);

  const router = useRouter();
  const { slug } = router.query;

  //COMMIT PAGINATOION
  const [currentCommitPage, setCurrentCommitPage] = useState(1);
  const itemsPerPage = 5; // Number of items per page

  // Calculate the index of the first and last item to display on the current page
  const indexOfLastCommitItem = currentCommitPage * itemsPerPage;
  const indexOfFirstCommitItem = indexOfLastCommitItem - itemsPerPage;
  const currentDeveloperCommitList = developerDataList ? developerDataList.slice(indexOfFirstCommitItem, indexOfLastCommitItem): [];

  //ISSUE PAGINATOION
  const [currentIssuePage, setCurrentIssuePage] = useState(1);

  // Calculate the index of the first and last item to display on the current page
  const indexOfLastIssueItem = currentIssuePage * itemsPerPage;
  const indexOfFirstIssueItem = indexOfLastIssueItem - itemsPerPage;
  const currentIssueList = issueDataList ? issueDataList.slice(indexOfFirstIssueItem, indexOfLastIssueItem): [];

  //PR PAGINATION
  const [currentPRPage, setCurrentPRPage] = useState(1);

  // Calculate the index of the first and last item to display on the current page
  const indexOfLastPRItem = currentPRPage * itemsPerPage;
  const indexOfFirstPRItem = indexOfLastPRItem - itemsPerPage;
  const currentPRList = prDataList ? prDataList.slice(indexOfFirstPRItem, indexOfLastPRItem): [];


  // Change page
  const handleCommitPageChange = (pageNumber) => {
    setCurrentCommitPage(pageNumber);
  };

  const handleIssuePageChange = (pageNumber) => {
    setCurrentIssuePage(pageNumber);
  };

  const handlePRPageChange = (pageNumber) => {
    setCurrentPRPage(pageNumber);
  };

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
                          Sort by:
                        </option>
                        <option value="1">Developer Name</option>
                        <option value="2">GitHub Username</option>
                        <option value="3">Additions</option>
                        <option value="4">Deletions</option>
                        <option value="5">Number of Commits</option>
                      </Form.Select>
                    </div>
                    <>
                    {!developerDataList || developerDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      <>
                        {currentDeveloperCommitList.map((developerData, idx) => (
                          <DeveloperCard
                            key={idx} // Use a unique identifier here
                            devName={developerNames[indexOfFirstCommitItem + idx]} // Adjust index based on pagination
                            devData={developerData}
                          />
                        ))}
                        <Pagination>
                          <Pagination.Prev
                            onClick={() => handleCommitPageChange(currentCommitPage - 1)}
                            disabled={currentCommitPage === 1}
                          />
                          <p className="p-2 d-flex align-center justify-center">
                          {currentCommitPage}
                          </p>
                          
                          <Pagination.Next
                            onClick={() => handleCommitPageChange(currentCommitPage + 1)}
                            disabled={indexOfLastCommitItem >= developerDataList.length}
                          />
                        </Pagination>
                      </>
                    )}
                  </>
                  </Tab>
                  <Tab eventKey="prs" title="PRs">
                    <div className="d-flex align-items-center">
                      <Button
                        className="btn-teal go-back-btn mb-2"
                        onClick={() => handleBack()}
                      >
                        <IoMdArrowRoundBack />
                        Back
                      </Button>
                      <Form.Select
                        onChange={(e) => handlePRFilterChange(e)}
                        defaultValue={selectedPrFilter}
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
                          Sort by:
                        </option>
                        <option value="1">PRs Contributed</option>
                        <option value="2">Sentiment Score</option>
                      </Form.Select>
                    </div>
                    

                    {!prDataList || prDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      <>
                        {currentPRList.map((prData, idx) => (
                          <PrCard
                          key={idx}
                          prName={prNames[idx]}
                          prData={prData}
                        />
                      ))}
                        <Pagination>
                          <Pagination.Prev
                            onClick={() => handlePRPageChange(currentPRPage - 1)}
                            disabled={currentPRPage === 1}
                          />
                          <p className="p-2 d-flex align-center justify-center">
                          {currentPRPage}
                          </p>
                          
                          <Pagination.Next
                            onClick={() => handlePRPageChange(currentPRPage + 1)}
                            disabled={indexOfLastPRItem >= prDataList.length}
                          />
                        </Pagination>
                      </>
                    )}
                  </Tab>
                  <Tab eventKey="issues" title="Issues">
                    <div className="d-flex align-items-center">
                      <Button
                        className="btn-teal go-back-btn mb-2"
                        onClick={() => handleBack()}
                      >
                        <IoMdArrowRoundBack />
                        Back
                      </Button>
                      <Form.Select
                        onChange={(e) => handleIssuesFilterChange(e)}
                        defaultValue={selectedIssueFilter}
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
                          Sort by:
                        </option>
                        <option value="1">Number of Issues Created</option>
                        <option value="2">Number of Issues Assigned</option>
                        <option value="3">Number of Issues Resolved</option>
                        <option value="4">Average Issue Resolution Time</option>
                      </Form.Select>
                    </div>

                    {!issueDataList || issueDataList.length === 0 ? (
                      <Spinner animation="border" />
                    ) : (
                      <>
                        {currentIssueList.map((issueData, idx) => (
                        <IssueCard
                          key={idx}
                          issueName={issueNames[indexOfFirstIssueItem + idx]}
                          issueData={issueData}
                        />
                      ))}
                        <Pagination>
                          <Pagination.Prev
                            onClick={() => handleIssuePageChange(currentIssuePage - 1)}
                            disabled={currentIssuePage === 1}
                          />
                          <p className="p-2 d-flex align-center justify-center">
                          {currentIssuePage}
                          </p>
                          
                          <Pagination.Next
                            onClick={() => handleIssuePageChange(currentIssuePage + 1)}
                            disabled={indexOfLastIssueItem >= issueDataList.length}
                          />
                        </Pagination>
                      </>
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
