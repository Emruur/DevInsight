import React from "react";
import { useState, useEffect } from "react";
import constants from "../constants";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import { useRouter } from "next/router";

const RepoBlock = ({ analysis, idx }) => {
  const router = useRouter();

  const [show, setShow] = useState(false);
  const [selectedDate, setSelectedDate] = useState(analysis.dates[0]); // Add this line in your component
  //TODO more things will be added if the date is in progress

  useEffect(() => {
    setSelectedDate(analysis.dates[0]);
  }, [analysis.dates]);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const handleGetAnalysis = (analysis, selectedDate) => {
    router.push(`docs/${analysis.repo_name}/${selectedDate}`);
  };

  const [bgColor, setbgColor] = useState(
    Object.values(constants.colors)[idx % 16]
  );
  const [fontColor, setFontColor] = useState(
    Object.values(constants.fonts)[idx % 16]
  );
  return (
    <>
      <Button
        className="repo-block"
        onClick={() => handleShow()}
        style={{ backgroundColor: bgColor, color: fontColor }}
      >
        {analysis.repo_name.charAt(0).toUpperCase()}
      </Button>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{analysis.repo_name}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <p>Select a date for this repository:</p>
          <Form.Select
            aria-label="Default select example"
            onChange={(e) => handleDateChange(e)}
            value={selectedDate} // Set the value of the Form.Select component to selectedDate
          >
            {analysis.dates.map((date, idx) => (
              <option key={idx} value={date}>
                {date}
              </option>
            ))}
          </Form.Select>
        </Modal.Body>
        <Modal.Footer>
          <Button className="btn-velvet" onClick={handleClose}>
            Close
          </Button>
          <Button
            className="btn-teal"
            onClick={() => handleGetAnalysis(analysis, selectedDate)}
          >
            Select
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default RepoBlock;
