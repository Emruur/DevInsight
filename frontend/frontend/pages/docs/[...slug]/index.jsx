import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import { useRouter } from "next/router";
import Header from "../../Header";
import DeveloperCard from "../../DeveloperCard";
import Button from 'react-bootstrap/Button';


const Page = () => {
  const [repoData, setRepoData] = useState({});
  const [developerNames, setDeveloperNames] = useState([]);
  const [developerDataList, setDeveloperDataList] = useState([]);

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
                  <DeveloperCard key={idx} data={developerData} />
                ))}

                <Button
                  className="btn-teal"
                  onClick={() => handleBack()}
                >
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
