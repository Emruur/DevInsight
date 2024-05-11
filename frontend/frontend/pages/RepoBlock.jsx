import React from "react";
import { useState } from "react";
import constants from "../constants";
import Button from "react-bootstrap/Button";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";

const RepoBlock = ({ analysis, idx }) => {
  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

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
          <Form.Select aria-label="Default select example">
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
          <Button className="btn-teal" onClick={handleClose}>
            Select
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
};

export default RepoBlock;
