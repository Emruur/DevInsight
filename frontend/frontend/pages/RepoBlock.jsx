import React, { use } from "react";
import { useState, useEffect } from "react";
import constants from "../constants";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import { useRouter } from "next/router";

const RepoBlock = ({ analysis, idx, loading }) => {
  const router = useRouter();
  
  // Use the first available date or a default empty string
  const [selectedDate, setSelectedDate] = useState(analysis?.dates?.[0]);
  const [show, setShow] = useState(false);
  const [bgColor, setbgColor] = useState(Object.values(constants.colors)[idx % 16]);
  const [fontColor, setFontColor] = useState(Object.values(constants.fonts)[idx % 16]);
  const [loadingLocal, setLoadingLocal] = useState(false);

  // Update selectedDate only if dates are available
  useEffect(() => {
    if (analysis?.dates && analysis.dates.length > 0) {
      setSelectedDate(analysis.dates[0]);
    } else {
      setSelectedDate('');
    }
  }, [analysis]);

  useEffect(() => {
    if (analysis?.dates?.some(date => date === "in progress")) {
      setLoadingLocal(true);
    } else {
      setLoadingLocal(false);
    }
  }, [analysis]);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handleGetAnalysis = (analysis, selectedDate) => {
    router.push(`docs/${analysis.repo_name}/${selectedDate}`);
  };

  // Fallback to empty string if repo_name isn't available
  const repoInitial = analysis?.repo_name ? analysis.repo_name.charAt(0).toUpperCase() : "";

  return (
    <>
      <Button
        className="repo-block"
        onClick={() => handleShow()}
        style={{ backgroundColor: bgColor, color: fontColor }}
      >
        {!loadingLocal ? ( repoInitial
      ) : (
        // Spinner appears if not loading
        <div className="spinner-border" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      )}
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{analysis?.repo_name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Select a date for this repository:</p>
          <Form.Select
            aria-label="Default select example"
            onChange={(e) => handleDateChange(e)}
            value={selectedDate}
            disabled={!analysis?.dates || analysis.dates.length === 0}
          >
            {analysis?.dates && analysis.dates.length > 0 ? (
              analysis.dates.map((date, idx) => (
                <option key={idx} value={date}>
                  {date}
                </option>
              ))
            ) : (
              <option>No dates available</option>
            )}
          </Form.Select>
        </Modal.Body>
        <Modal.Footer>
          <Button className="btn-velvet" onClick={handleClose}>
            Close
          </Button>
          <Button
            className="btn-teal"
            onClick={() => handleGetAnalysis(analysis, selectedDate)}
            disabled={!selectedDate || selectedDate === "in progress"}
          >
            Select
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default RepoBlock;
