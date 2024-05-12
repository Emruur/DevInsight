import { useState, useEffect } from "react";
import RepoBlock from "./RepoBlock";
import Header from "./Header";

function IndexPage() {
  const [analyses, setAnalyses] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [repoUrl, setRepoUrl] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:5000/get_all_analysis")
      .then((response) => response.json())
      .then((data) => setAnalyses(data.map(analysis => ({...analysis, loading: false}))))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  const handleCreateAnalysis = () => {
    setAnalyses(prev => prev.map(analysis => analysis.repo_url === repoUrl ? {...analysis, loading: true} : analysis));
    fetch("http://127.0.0.1:5000/create_analysis", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          return response.json().then((data) => {
            throw new Error(data.error || "Unknown error occurred");
          });
        }
      })
      .then((data) => {
        setShowModal(false);
        setErrorMessage("");
        console.log("Analysis started:", data);
        // Add the new analysis with loading set to true
        setAnalyses(prevAnalyses => [...prevAnalyses, { ...data, loading: true }]);
      })
      .catch((error) => {
        setErrorMessage(error.message);
        console.error("Error creating analysis:", error);
        setAnalyses(prev => prev.map(analysis => analysis.repo_url === repoUrl ? {...analysis, loading: false} : analysis));
      }).finally(() => {
        //set loading to false
        console.log("finally");
        setAnalyses(prevAnalyses => prevAnalyses.map(analysis =>
          analysis.repo_url === repoUrl ? {...analysis, loading: false} : analysis
        ));
        setRepoUrl("");

      });
  };

  return (
    <>
      <Header />
      <div className="container pt-5">
        <div className="row d-flex justify-content-center">
          <div className="col-10 d-flex justify-content-center">
            <div className="col-12">
              <div className="row">
                <div className="repo-grid col-2 d-flex align-items-center">
                  <button
                    type="button"
                    className="create-btn btn btn-primary"
                    style={{ marginRight: "10px" }}
                    onClick={() => {
                      setRepoUrl("");
                      setErrorMessage("");
                      setShowModal(true);
                    }}
                  >
                    +
                  </button>
                </div>
                {analyses.map((analysis, idx) => (
                  <div className="repo-grid col-2 d-flex align-items-center" key={idx}>
                    <RepoBlock analysis={analysis} idx={idx} loading={analysis.loading} />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="modal show fade" id="exampleModal" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" style={{ display: 'block', backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-body">
                Enter the URL of the repository:
                <input type="text" className="form-control" placeholder="Enter URL" value={repoUrl} onChange={(e) => setRepoUrl(e.target.value)} />
                {errorMessage && (
                  <div className="alert alert-danger mt-2" role="alert">
                    {errorMessage}
                  </div>
                )}
              </div>
              <div className="modal-footer border-0 d-flex justify-content-center align-items-center">
                <button
                  type="button"
                  className="btn btn-primary"
                  style={{ backgroundColor: "#25b7ae", borderColor: "#25b7ae" }}
                  onClick={handleCreateAnalysis}
                >
                  Add Repository
                </button>
                <button
                  type="button"
                  className="btn btn-secondary"
                  style={{ backgroundColor: "#ff6262", borderColor: "#ff6262" }}
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default IndexPage;
