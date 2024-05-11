import { useState, useEffect } from "react";
import RepoBlock from "./RepoBlock";
import Header from "./Header";

function IndexPage() {
  const [analyses, setAnalyses] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [repoUrl, setRepoUrl] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_all_analysis")
      .then((response) => response.json())
      .then((data) => setAnalyses(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleCreateAnalysis = () => {
    fetch("http://127.0.0.1:5000/create_analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    })
      .then((response) => response.json())
      .then((data) => {
        setShowModal(false);
        // Update local state or re-fetch analysis list
        console.log("Analysis started:", data);
      })
      .catch((error) => console.error("Error creating analysis:", error));
  };

  return (
    <>
      <Header />
      <div className="container py-5">
        <div className="row d-flex justify-content-center">
          <div className="col-10 d-flex justify-content-center">
            <div className="col-12">
              <div className="row">
                <div className="repo-grid col-2 d-flex align-items-center">
                  <button
                    type="button"
                    className="create-btn btn btn-primary"
                    style={{ marginRight: "10px" }}
                    data-bs-toggle="modal"
                    data-bs-target="#exampleModal"
                    onClick={() => setShowModal(true)}
                  >
                    +
                  </button>
                </div>
                {analyses.map((analysis, idx) => (
                  <div
                    className="repo-grid col-2 d-flex align-items-center"
                    key={idx}
                  >
                    <RepoBlock analysis={analysis} idx={idx} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div
        className="modal fade"
        id="exampleModal"
        tabIndex="-1"
        aria-labelledby="exampleModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="exampleModalLabel">
                Modal title
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">...</div>
          </div>
        </div>
      </div>
    </>
  );
}

export default IndexPage;
